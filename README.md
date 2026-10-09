# data2

Material für **259.075 Data-integrated Algorithmic Design Processes II**, TU Wien.
Sieben Einheiten, von einem Neuron bis zu Diffusion und LoRA, gerechnet auf offenen Daten
der Stadt Wien. Alles läuft auf einer CPU.

- `notebooks/` — je Einheit ein Aufgaben- und ein Lösungsnotebook, der Lehrtext steht darin
- `data/` — Daten und die Skripte, die sie erzeugen, samt der vortrainierten Modelle
- `sessions/` — Stundenplanung, Zeitraster und Bewertung; nur für mich, nicht für die Studierenden
- `webapps/` — eigenständige Web-Apps, derzeit die Lernkarten zu den Begriffen

## Die sieben Einheiten

| | Notebook | Thema | Aufgabe im Notebook |
|---|---|---|---|
| 1 | `01_neuron` | Neuron, Fehlerlandschaft, Gradientenabstieg | die Schrittregel |
| 2 | `02_netz` | mehrere Eingänge, Normieren, ReLU, Matrixform | Rückrechnung der Gewichte |
| 3 | `03_ueberanpassung` | Rauschen, Aufteilung, Überanpassung, Extrapolation | die Trainingsschleife |
| 4 | `04_grundriss` | Grundriss als Zahl, Autoencoder, Karte der Formen | nächste Nachbarn, Interpolation |
| 5 | `05_erzeugen` | warum ein Autoencoder nicht zieht, VAE, Temperatur | das Ziehen |
| 6 | `06_sprache` | Token, Kreuzentropie, Zeichenmodell, Halluzination | das Ziehen eines Zeichens |
| 7 | `07_diffusion` | Diffusion im Codeaum, Schrittzahl, LoRA, Surrogat | der Entrauschungsschritt |

## Daten

`fetch_ogd.py` holt die Gebäudetypologie aus dem offenen Datenportal (Layer
`ogdwien:GEBAEUDETYPOGD`) und schreibt `gebaeude_wien.csv` und `.geojson`. Die Spalte `hwb`
ist **nicht gemessen**, sondern aus U-Wert und Kompaktheit gerechnet; das steht in jedem
Notebook, das sie verwendet, und ist der Grund, warum ab Einheit 3 Rauschen aufgelegt wird.

`raster.py` legt die Grundrisspolygone ausgerichtet in ein 32-mal-32-Raster.
`strassen.py` holt die Straßennamen für Einheit 6.

## Vortrainierte Modelle

Die Modelle werden vor der Lehrveranstaltung gerechnet und liegen als Gewichtsdateien bei, in
der Stunde wird nur codiert, decodiert und gezogen.

```
uv run --with numpy python data/raster.py
uv run --with numpy --with torch python data/autoencoder.py    # ae_32.pt, ae_8.pt, ae_2.pt
uv run --with numpy --with torch python data/vae.py            # vae_8.pt, cvae_8.pt
uv run --with numpy --with torch python data/diffusion.py      # diffusion.pt, lora_schlank.pt
```

Zusammen etwa zehn Minuten auf einer CPU.
