"""Variational autoencoder auf den Grundrissrastern, einmal frei und einmal auf die Bauperiode
bedingt.

Der Unterschied zum gewoehnlichen Autoencoder ist klein und folgenreich: der Encoder gibt nicht
einen Punkt aus, sondern Mittelwert und Streuung, gezogen wird daraus, und ein zweiter Term im
Verlust haelt die Wolken beieinander. Erst dadurch ist der Raum zwischen den Trainingsbeispielen
kein Niemandsland mehr.

    uv run --with numpy --with torch python data/vae.py
"""
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

HIER = Path(__file__).resolve().parent
ENGE = 8
EPOCHEN = 600
STAPEL = 64
BETA = 1.0                      # Gewicht des zweiten Terms; 1.0 ist die Lehrbuchfassung

# Die Bauperioden, zu Gruppen zusammengefasst. "Nach 1976" haben in diesem Ausschnitt nur 19
# Gebaeude, zu wenige fuer eine eigene Gruppe; sie laufen unter "ab 1946".
GRUPPEN = ["bis 1918", "1919-1945", "ab 1946"]


def gruppe(startjahr):
    jahr = int(startjahr)
    if jahr <= 1918:
        return 0
    if jahr <= 1945:
        return 1
    return 2


class VAE(nn.Module):
    def __init__(self, enge=ENGE, klassen=0):
        super().__init__()
        self.klassen = klassen
        self.encoder = nn.Sequential(
            nn.Linear(1024 + klassen, 256), nn.ReLU(),
            nn.Linear(256, 64), nn.ReLU())
        self.mittel = nn.Linear(64, enge)
        self.log_streuung = nn.Linear(64, enge)
        self.decoder = nn.Sequential(
            nn.Linear(enge + klassen, 64), nn.ReLU(),
            nn.Linear(64, 256), nn.ReLU(),
            nn.Linear(256, 1024))

    def codiere(self, x, c=None):
        eingang = x if c is None else torch.cat([x, c], dim=1)
        h = self.encoder(eingang)
        return self.mittel(h), self.log_streuung(h)

    def ziehe(self, mittel, log_streuung):
        streuung = torch.exp(0.5 * log_streuung)
        return mittel + streuung * torch.randn_like(streuung)

    def decodiere(self, z, c=None):
        return self.decoder(z if c is None else torch.cat([z, c], dim=1))

    def forward(self, x, c=None):
        mittel, log_streuung = self.codiere(x, c)
        z = self.ziehe(mittel, log_streuung)
        return self.decodiere(z, c), mittel, log_streuung


def verlust_fn(roh, ziel, mittel, log_streuung):
    treue = nn.functional.binary_cross_entropy_with_logits(roh, ziel, reduction="sum") / len(ziel)
    # Kullback-Leibler gegen die Standardnormalverteilung, geschlossen loesbar
    beisammen = -0.5 * torch.sum(1 + log_streuung - mittel ** 2 - log_streuung.exp()) / len(ziel)
    return treue + BETA * beisammen, treue, beisammen


def trainiere(X, C, klassen, i_tr, i_va, samen=0):
    torch.manual_seed(samen)
    modell = VAE(klassen=klassen)
    optimierer = torch.optim.Adam(modell.parameters(), lr=1e-3)
    bester, beste_gewichte = float("inf"), None
    for epoche in range(EPOCHEN):
        reihe = i_tr[torch.randperm(len(i_tr))]
        for anfang in range(0, len(reihe), STAPEL):
            wahl = reihe[anfang:anfang + STAPEL]
            x = X[wahl]
            c = C[wahl] if klassen else None
            roh, mittel, log_streuung = modell(x, c)
            fehler, _, _ = verlust_fn(roh, x, mittel, log_streuung)
            optimierer.zero_grad()
            fehler.backward()
            optimierer.step()
        if epoche % 5 == 0 or epoche == EPOCHEN - 1:
            with torch.no_grad():
                x = X[i_va]
                c = C[i_va] if klassen else None
                roh, mittel, log_streuung = modell(x, c)
                f_va, treue, beisammen = verlust_fn(roh, x, mittel, log_streuung)
            if float(f_va) < bester:
                bester = float(f_va)
                beste_gewichte = {n: t.detach().clone()
                                  for n, t in modell.state_dict().items()}
            if epoche % 100 == 0:
                print(f"  epoche {epoche:3d}: validierung {float(f_va):.1f} "
                      f"(treue {float(treue):.1f}, beisammen {float(beisammen):.2f})")
    modell.load_state_dict(beste_gewichte)
    print(f"  bester validierungswert {bester:.1f}")
    return modell


def main():
    bilder = np.load(HIER / "grundrisse.npy")
    X = torch.tensor(bilder.reshape(len(bilder), -1), dtype=torch.float32)

    tabelle = np.genfromtxt(HIER / "grundrisse.csv", delimiter=",", names=True,
                            dtype=None, encoding="utf-8")
    gruppen = np.array([gruppe(j) for j in tabelle["startjahr"]])
    C = torch.zeros(len(X), len(GRUPPEN))
    C[torch.arange(len(X)), torch.tensor(gruppen)] = 1.0
    print("buildings per group:", {GRUPPEN[g]: int((gruppen == g).sum())
                                   for g in range(len(GRUPPEN))})

    # dieselbe Aufteilung wie beim gewoehnlichen Autoencoder, damit die Bilder vergleichbar sind
    zufall = np.random.default_rng(11)
    i = np.arange(len(X))
    zufall.shuffle(i)
    i_tr, i_va = torch.tensor(i[:850]), torch.tensor(i[850:])

    print("free vae:")
    frei = trainiere(X, C, 0, i_tr, i_va)
    torch.save(frei.state_dict(), HIER / "vae_8.pt")

    print("conditional vae:")
    bedingt = trainiere(X, C, len(GRUPPEN), i_tr, i_va)
    torch.save(bedingt.state_dict(), HIER / "cvae_8.pt")

    with torch.no_grad():
        mittel, _ = frei.codiere(X)
    np.savez(HIER / "vae_codes.npz", code=mittel.numpy(), gruppe=gruppen)
    print("written: vae_8.pt, cvae_8.pt, vae_codes.npz")


if __name__ == "__main__":
    main()
