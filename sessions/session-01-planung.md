# Session 1, Planung für mich

Erste von sieben Einheiten, Freitag 09:00 bis 11:00, EDV-Labor PC5, rund 20 Studierende.
Der Lehrtext steht im Notebook `notebooks/01_neuron.ipynb`, hier steht nur, was ich brauche.

## Zeitraster

Schritte wie im Notebook. Die Zeiten sind knapp; die Kastenzeiten bei Schritt 3 und 7 ansagen.

- 0 bis 10: Anmeldung, Repo klonen, Schritt 1. Wer nicht hineinkommt, arbeitet zu zweit.
- 10 bis 25: Schritt 2 (Punktwolke, Kompaktheit) und Schritt 3 (eigenes Haus auf der Karte,
  höchstens fünf Minuten suchen, dann irgendeines nehmen).
- 25 bis 45: Schritt 4 bis 6: Gerade als Modell, MSE an drei Häusern, Regler.
- 45 bis 55: Pause.
- 55 bis 65: Schritt 7: Gradient, eigenes w eintippen, höchstens zehn Minuten.
- 65 bis 80: Schritt 8: Lücke im Lernloop, Etappentabelle. Die Animation nur, wenn Zeit ist.
- 80 bis 90: Schritt 9: Residuenkarte, das eigene Haus, die Ansage zur Rechenvorschrift; Tests.
- 90 bis 95: Puffer.
- 95 bis 105: Kurztest.
- 105 bis 120: Hausübung vorstellen (dort jetzt auch die zu große Lernrate), Fragen, Puffer.

Zeitnot: Etappenzelle nach der Animation nur zeigen, nicht besprechen.

## Vorher zu erledigen

- Vorabcheck `00_check.ipynb` bis Mittwoch vor der Einheit, 12:00. Fehlermeldungen vor der Stunde lösen.
- Generalprobe im Labor: zwanzig gleichzeitige Kernel, Plotly-Animationen, Kernel-Neustart mit
  Durchlauf aller Zellen.
- Lösungsnotebook nach der Abgabefrist freischalten.

## Bewertung

Kurztest 3 Punkte. Hausübung 10 Punkte, davon 6 auf die Interpretation nach den sechs
Kriterien der Angabe: Größenordnung, Vorzeichen und Plausibilität, Einheiten, Gültigkeitsbereich,
eine Fehlerquelle, eine Entwurfsfolgerung. Je Kriterium ein Punkt, keine halben.

Es gilt `kursregeln.md`: Auflösung nach zehn Minuten, ohne Abzug, und ohne Abgabe null Punkte.

## Zahlen, die in der Stunde fallen

Optimum auf dem aktuellen Datensatz: w = 8,5, b = 109, MSE 50,3; mit b = 110 fest bester ganzzahliger Regler w = 8, MSE 53. Divergenz ab Lernrate
0,0299 (nachgerechnet), deshalb 0,04 für das Gegenbeispiel. Datensatz: 1073 Gebäude.
