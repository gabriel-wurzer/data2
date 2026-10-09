# data2, Arbeitsverzeichnis

Material für **259.075 VU Data-integrated Algorithmic Design Processes II**, TU Wien.
Sieben Einheiten, Freitag 09:00 bis 11:00, EDV-Labor PC5, rund 20 Studierende. Die
Notebooks laufen auf CPU, auf dem JupyterHub der TU Wien steht zusätzlich eine GPU zur
Verfügung. Daten sind offene Daten der Stadt Wien. Gebaut wurde das Material Ende
September 2026 aus einer anderen Sitzung heraus; diese Datei ersetzt deren Gedächtnis.

## Wo was liegt

- `notebooks/` — je Einheit ein Aufgaben- und ein Lösungsnotebook. **Der Lehrtext steht im
  Notebook**, nicht daneben. Beide Fassungen haben dieselbe Zellenfolge, das Lösungsnotebook
  füllt nur die Lücke im Abschnitt "Your part".
- `sessions/` — Stundenplanung, Zeitraster, Bewertung. **Nur für Gabriel, nie austeilen.**
- `data/` — Daten, die Skripte, die sie erzeugen, und die vortrainierten Modelle.
- `webapps/` — eigenständige Apps, derzeit die Lernkarten.

## Konventionen

Das Material ist **englisch**, auch die Oberflächen der Apps, unabhängig davon, in welcher
Sprache der Auftrag kam. Die Planung in `sessions/` ist deutsch.

Jede Einheit endet mit "Tests" und "Where you stand now". Die Tests rechnen nach, sie
prüfen nicht nur auf Vorhandensein. Die Begriffe am Schluss stehen auch in den Lernkarten.

Die Spalte `hwb` in `gebaeude_wien.csv` ist **nicht gemessen**, sondern aus U-Wert und
Kompaktheit gerechnet. Das steht in jedem Notebook, das sie verwendet, und ist der Grund,
warum ab Einheit 3 Rauschen aufgelegt wird. Ein Modell, das sie exakt trifft, hat eine
Rechenvorschrift rückwärts ausgefischt und nichts über Häuser gelernt. Das wird im Material
auch so benannt.

## Bewertung

Je Einheit Kurztest 3 Punkte, Hausübung 10 Punkte, davon 6 auf die Interpretation nach
sechs Kriterien: Größenordnung, Vorzeichen und Plausibilität, Einheiten, Gültigkeitsbereich,
eine Fehlerquelle, eine Entwurfsfolgerung. Je Kriterium ein Punkt, keine halben. Es gilt
`sessions/kursregeln.md`.

## Offen, Stand 08.10.2026

Die Hausübung steht in jedem Notebook am Ende unter "Homework", in beiden Fassungen gleich.
Kurztests mit Lösung, Bewertungshinweise je Hausübung und der Bewertungslauf für Einheit 3
liegen in `sessions/privat/`, das in `.gitignore` steht. **Der Rest von `sessions/` und die
Lösungsnotebooks sind auf GitHub öffentlich lesbar**, sobald sie gepusht sind. Hausübungen und
Kurztests sind je Einheit durch Codex-Reviews gegangen, bis keine blockierenden Befunde mehr kamen
(Stand 09.10.2026).

Am 08.10.2026 neu erzeugt: `data/raster.py` rechnete Höfe auf den falschen Ursprung (183
Grundrisse betroffen); Raster, Autoencoder, VAEs, Diffusion und LoRA sind neu gerechnet, der
Sampler in `data/diffusion.py` rechnet das Rauschen nach dem Begrenzen nach. Die Bilder der
Einheiten 4 bis 7 sehen dadurch etwas anders aus als vorher.

Die Listen "Offene Punkte" in `sessions/einheit-0X.md` sind großteils überholt: Modelle,
Straßennamen und Datensätze liegen vor.

Betrieblich offen: PyTorch im Hub-Image prüfen, Generalprobe mit zwanzig gleichzeitigen
Kerneln. Beides misst `sessions/lastmessung.ipynb` auf dem Hub, CPU und GPU; der GPU-Zweig ist
ungetestet, weil lokal keine Karte da ist. Lokal auf CPU kostet die längste Rechnung (Einheit 3)
elf Sekunden je Kernel, Einheit 7 zieht 200 Schritte mal zwölf Bilder in unter einer Zehntelsekunde.

## Veröffentlichung

Repo `git@github.com:gabriel-wurzer/data2.git`, die Lernkarten laufen über GitHub Pages
unter `gabriel-wurzer.github.io/data2/webapps/lernkarten/`. Was nicht committet und
gepusht ist, sehen die Studierenden nicht. Vor jeder Einheit den Stand prüfen.
