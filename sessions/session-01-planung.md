# Session 1, Planung für mich

Erste von sieben Einheiten, Freitag 09:00 bis 11:00, EDV-Labor PC5, rund 20 Studierende.
Der Lehrtext steht im Notebook `notebooks/01_neuron.ipynb`, hier steht nur, was ich brauche.

## Zeitraster

- 0 bis 10: Anmeldung, Notebook öffnen, erste Zelle. Wer nicht hineinkommt, arbeitet zu zweit.
- 10 bis 25: Punktwolke und Karte, eigene Gerade am Regler, Fehler aufschreiben lassen.
- 25 bis 50: Neuron, Fehlerlandschaft, 3D-Fläche drehen.
- 50 bis 60: Pause.
- 60 bis 85: Lücke ausfüllen, stabiler Lauf, dann Divergenz bei Lernrate 0.04.
  Zeitnot: zuerst fällt der Zusatz mit den Kleinstquadraten weg, dann wandert der zweite Lauf
  in die Hausübung.
- 85 bis 95: Residuenkarte, das eigene Haus wiederfinden, die Ansage zur Rechenvorschrift.
- 95 bis 105: Kurztest.
- 105 bis 120: Hausübung, Fragen, Puffer.

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

Optimum auf dem aktuellen Datensatz: w = 8,5, b = 109, Fehler 50,3. Divergenz ab Lernrate
0,0299 (nachgerechnet), deshalb 0,04 für das Gegenbeispiel. Datensatz: 1073 Gebäude.
