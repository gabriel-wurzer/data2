"""Drei Autoencoder auf den Grundrissrastern trainieren, mit 32, 8 und 2 Zahlen in der Mitte.

Die Modelle werden vor der Lehrveranstaltung gerechnet und als Gewichtsdateien mitgeliefert;
in der Stunde wird nur codiert und decodiert. Ausgabe: `ae_32.pt`, `ae_8.pt`, `ae_2.pt` und
`codes.npz` mit den Codes aller Grundrisse und der Aufteilung.

    uv run --with numpy --with torch python data/autoencoder.py
"""
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

HIER = Path(__file__).resolve().parent
BILDER = HIER / "grundrisse.npy"
ENGEN = (32, 8, 2)
EPOCHEN = 400
STAPEL = 64


class Autoencoder(nn.Module):
    """1024 Bildpunkte auf wenige Zahlen und zurueck. Zwei Schichten je Richtung."""

    def __init__(self, enge):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(1024, 256), nn.ReLU(),
            nn.Linear(256, 64), nn.ReLU(),
            nn.Linear(64, enge))
        self.decoder = nn.Sequential(
            nn.Linear(enge, 64), nn.ReLU(),
            nn.Linear(64, 256), nn.ReLU(),
            nn.Linear(256, 1024))

    def forward(self, x):
        return self.decoder(self.encoder(x))


def trainiere(enge, X_tr, X_va, samen=0):
    torch.manual_seed(samen)
    modell = Autoencoder(enge)
    verlust = nn.BCEWithLogitsLoss()
    optimierer = torch.optim.Adam(modell.parameters(), lr=1e-3)
    bester, beste_gewichte = float("inf"), None
    for epoche in range(EPOCHEN):
        reihe = torch.randperm(len(X_tr))
        for anfang in range(0, len(X_tr), STAPEL):
            stapel = X_tr[reihe[anfang:anfang + STAPEL]]
            fehler = verlust(modell(stapel), stapel)
            optimierer.zero_grad()
            fehler.backward()
            optimierer.step()
        if epoche % 10 == 0 or epoche == EPOCHEN - 1:
            with torch.no_grad():
                f_va = float(verlust(modell(X_va), X_va))
            if f_va < bester:
                bester = f_va
                beste_gewichte = {n: t.detach().clone() for n, t in modell.state_dict().items()}
            if epoche % 100 == 0:
                print(f"  enge {enge:2d}, epoche {epoche:3d}, validierung {f_va:.4f}")
    modell.load_state_dict(beste_gewichte)
    return modell, bester


def main():
    bilder = np.load(BILDER)
    X = torch.tensor(bilder.reshape(len(bilder), -1), dtype=torch.float32)

    zufall = np.random.default_rng(11)
    i = np.arange(len(X))
    zufall.shuffle(i)
    i_tr, i_va = i[:850], i[850:]
    X_tr, X_va = X[i_tr], X[i_va]

    codes = {}
    for enge in ENGEN:
        modell, f_va = trainiere(enge, X_tr, X_va)
        torch.save(modell.state_dict(), HIER / f"ae_{enge}.pt")
        with torch.no_grad():
            codes[f"code_{enge}"] = modell.encoder(X).numpy()
            rueck = torch.sigmoid(modell(X)).numpy().reshape(-1, 32, 32)
        treffer = float(np.mean((rueck > 0.5) == (bilder > 0.5)))
        print(f"enge {enge:2d}: validierung {f_va:.4f}, pixel richtig {treffer:.3f}")

    np.savez(HIER / "codes.npz", i_tr=i_tr, i_va=i_va, **codes)
    print("geschrieben:", ", ".join(f"ae_{e}.pt" for e in ENGEN), "und codes.npz")


if __name__ == "__main__":
    main()
