"""Ein Diffusionsmodell im Codeaum des VAE, plus ein LoRA dazu. Grundlage fuer Einheit 7.

Nicht auf den 1024 Bildpunkten, sondern auf den acht Zahlen aus Einheit 5. Das ist genau der
Kunstgriff, mit dem die bekannten Bildmodelle arbeiten: erst ein Autoencoder, der ein Bild auf
wenige Zahlen bringt, dann die Diffusion in diesem kleinen Raum, dann der Decoder. Auf einem
Rechner ohne Grafikkarte ist es der Unterschied zwischen einer halben Stunde und drei Sekunden.

Das Modell lernt eine Sache: aus einem verrauschten Code und der Angabe, wie stark er
verrauscht ist, das Rauschen zu schaetzen. Erzeugt wird in einer Schleife, die das geschaetzte
Rauschen schrittweise abzieht.

    uv run --with numpy --with torch python data/diffusion.py
"""
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

HIER = Path(__file__).resolve().parent
ENGE = 8
SCHRITTE = 200                  # Laenge der Rauschleiter
EPOCHEN = 4000
STAPEL = 128
LERNRATE = 2e-3


def plan(schritte=SCHRITTE):
    """Cosinus-Plan: wie viel Signal nach t Schritten uebrig ist."""
    t = torch.linspace(0, 1, schritte + 1)
    f = torch.cos((t + 0.008) / 1.008 * torch.pi / 2) ** 2
    return (f / f[0]).clamp(1e-4, 1.0)


def zeitkodierung(t, breite=64):
    """Sinus und Cosinus in vielen Frequenzen. Eine einzelne Zahl als Zeit reicht nicht:
    das Netz muss den Schritt scharf unterscheiden, nicht nur grob einordnen."""
    frequenzen = torch.exp(torch.linspace(0, -7, breite // 2, device=t.device))
    winkel = t.float().unsqueeze(1) * frequenzen.unsqueeze(0)
    return torch.cat([winkel.sin(), winkel.cos()], dim=1)


class Rauschschaetzer(nn.Module):
    def __init__(self, enge=ENGE, breite=256, zeitbreite=64):
        super().__init__()
        self.zeitbreite = zeitbreite
        self.zeit = nn.Sequential(nn.Linear(zeitbreite, zeitbreite), nn.SiLU(),
                                  nn.Linear(zeitbreite, zeitbreite))
        self.ein = nn.Linear(enge + zeitbreite, breite)
        self.mitte = nn.Sequential(nn.SiLU(), nn.Linear(breite, breite), nn.SiLU(),
                                   nn.Linear(breite, breite))
        self.aus = nn.Sequential(nn.SiLU(), nn.Linear(breite, enge))

    def forward(self, z, t):
        e = self.zeit(zeitkodierung(t, self.zeitbreite))
        h = self.ein(torch.cat([z, e], dim=1))
        return self.aus(h + self.mitte(h))


def verrausche(z0, t, alpha_quer, rauschen=None):
    """Der Vorwaerts-Weg. Braucht kein Modell, nur einen Wuerfel."""
    if rauschen is None:
        rauschen = torch.randn_like(z0)
    a = alpha_quer[t].unsqueeze(1)
    return a.sqrt() * z0 + (1 - a).sqrt() * rauschen, rauschen


@torch.no_grad()
def ziehe(modell, alpha_quer, n=8, schritte=SCHRITTE, wuerfel=None, grenze=4.0):
    """Rueckwaerts: Rauschen hinlegen, schaetzen, abziehen, wiederholen.

    Deterministisch (DDIM mit eta = 0), damit in der Stunde alle dasselbe sehen und der
    Regler fuer die Schrittzahl vergleichbar bleibt.
    """
    z = torch.randn(n, ENGE, generator=wuerfel)
    stellen = torch.linspace(SCHRITTE, 1, schritte).long().tolist()
    z0 = z
    for i, t in enumerate(stellen):
        geschaetzt = modell(z, torch.full((n,), t, dtype=torch.long))
        a = alpha_quer[t]
        z0 = ((z - (1 - a).sqrt() * geschaetzt) / a.sqrt()).clamp(-grenze, grenze)
        # das Rauschen passend zum begrenzten z0 nachrechnen, sonst schaukelt sich die
        # Schaetzung oben auf der Leiter auf, wo kaum Signal uebrig ist
        geschaetzt = (z - a.sqrt() * z0) / (1 - a).sqrt()
        t_vor = stellen[i + 1] if i + 1 < len(stellen) else 0
        a_vor = alpha_quer[t_vor]
        z = a_vor.sqrt() * z0 + (1 - a_vor).sqrt() * geschaetzt
    return z0


def trainiere(Z, alpha_quer, samen=0, epochen=EPOCHEN, modell=None, nur=None, lernrate=LERNRATE):
    torch.manual_seed(samen)
    modell = modell or Rauschschaetzer()
    teile = nur if nur is not None else list(modell.parameters())
    optimierer = torch.optim.Adam(teile, lr=lernrate)
    for epoche in range(epochen):
        reihe = torch.randperm(len(Z))
        summe = 0.0
        for anfang in range(0, len(Z), STAPEL):
            z0 = Z[reihe[anfang:anfang + STAPEL]]
            t = torch.randint(1, SCHRITTE + 1, (len(z0),))
            zt, rauschen = verrausche(z0, t, alpha_quer)
            fehler = nn.functional.mse_loss(modell(zt, t), rauschen)
            optimierer.zero_grad()
            fehler.backward()
            optimierer.step()
            summe += float(fehler.detach()) * len(z0)
        if epoche % 500 == 0:
            print(f"  epoche {epoche:4d}: {summe / len(Z):.4f}")
    return modell


class LoRA(nn.Module):
    """Zwei schmale Matrizen neben einer eingefrorenen. Ihr Produkt hat deren Form.

    b startet auf null, das Zusatzstueck aendert am Anfang also nichts. Trainiert werden nur
    a und b; die urspruengliche Schicht bleibt, wie sie ist, und laesst sich abstecken.
    """

    def __init__(self, schicht, rang=4):
        super().__init__()
        self.schicht = schicht
        self.a = nn.Parameter(torch.randn(schicht.in_features, rang) * 0.02)
        self.b = nn.Parameter(torch.zeros(rang, schicht.out_features))
        self.staerke = 1.0

    def forward(self, x):
        return self.schicht(x) + self.staerke * (x @ self.a) @ self.b


def main():
    codes = np.load(HIER / "vae_codes.npz")["code"]
    Z = torch.tensor(codes, dtype=torch.float32)
    print(f"{len(Z)} codes, spread {float(Z.std()):.2f}")
    alpha_quer = plan()

    print("diffusion in the code space:")
    modell = trainiere(Z, alpha_quer)
    torch.save(modell.state_dict(), HIER / "diffusion.pt")

    # LoRA auf die schlanksten Grundrisse: das untere Viertel nach Fuellgrad
    tabelle = np.genfromtxt(HIER / "grundrisse.csv", delimiter=",", names=True,
                            dtype=None, encoding="utf-8")
    fuell = tabelle["fuellgrad"].astype(float)
    schlank = fuell < np.quantile(fuell, 0.25)
    print(f"lora subset: {int(schlank.sum())} of {len(Z)} buildings, fill below "
          f"{np.quantile(fuell, 0.25):.3f}")

    for p in modell.parameters():
        p.requires_grad_(False)
    modell.ein = LoRA(modell.ein)
    modell.aus[1] = LoRA(modell.aus[1])
    zusatz = [p for p in modell.parameters() if p.requires_grad]
    print(f"lora parameters: {sum(p.numel() for p in zusatz):,} of "
          f"{sum(p.numel() for p in modell.parameters()):,}")
    trainiere(Z[torch.tensor(schlank)], alpha_quer, epochen=1500, modell=modell, nur=zusatz,
              lernrate=1e-3)

    torch.save({n: t for n, t in modell.state_dict().items()
                if n.endswith(".a") or n.endswith(".b")}, HIER / "lora_schlank.pt")
    np.save(HIER / "lora_auswahl.npy", schlank)
    print("written: diffusion.pt, lora_schlank.pt, lora_auswahl.npy")


if __name__ == "__main__":
    main()
