# Einheit 4: Wie ein Grundriss zur Zahl wird

259.075 VU Data-integrated Algorithmic Design Processes II
Freitag, 27.11.2026, 09:00 bis 11:00, EDV-Labor PC5, rund 20 Studierende

## Wo wir herkommen

Drei Einheiten lang waren die Eingänge Zahlen, die jemand ausgesucht hat: Kompaktheit,
U-Wert. Jede dieser Zahlen ist eine Entscheidung darüber, was das Modell überhaupt sehen
darf. Heute geht es um diese Entscheidung selbst, und der Eingang ist ab jetzt der Grundriss.

Gerechnet wird auf den Grundrisspolygonen selbst. Die lagen bis heute nicht im Datensatz:
`fetch_ogd.py` hat aus jedem Polygon Fläche und Umfang gerechnet und die Form danach
weggeworfen. Das Skript schreibt jetzt zusätzlich `gebaeude_wien.geojson`, mit Außenring,
Höfen und mehrteiligen Bauwerken, über die Gebäude-Nummer mit der Tabelle verbunden.

## Lernziele

Am Ende der Einheit können die Studierenden

- drei Arten benennen, eine Grundrissform in Zahlen zu fassen, und sagen, was jede davon
  wegwirft: Kennwerte, Raster, Folge von Kanten,
- einen Autoencoder erklären, also die Verengung auf wenige Zahlen und den Weg zurück,
- an eigenen Rekonstruktionen zeigen, was bei kleiner werdendem Flaschenhals zuerst
  verschwindet,
- in der Karte der Codes benachbarte Häuser finden, prüfen, ob sie einander ähnlich sehen,
  und ein Urteil darüber begründen,
- erklären, was eine Projektion von acht auf zwei Zahlen macht und was sie dabei verliert.

## Ablauf

0 bis 15: Drei Wege in die Zahl. Derselbe Grundriss als zwei Kennwerte, als Schwarzweißraster
und als Folge von Kanten mit Länge und Winkel. Nebeneinander gezeigt, mit der Frage, was
jeweils verlorengeht. Die zwei Kennwerte aus Einheit 1 sehen danach aus, was sie sind: eine
sehr grobe Zusammenfassung.

15 bis 30: Rastern, selbst gemacht. Das Polygon in ein Gitter von 32 mal 32 legen, drehen und
verschieben, bis es mittig und größenbereinigt sitzt. Hier entscheidet sich, ob das Modell
später Form erkennt oder Lage, und genau das wird ausprobiert: einmal ohne Ausrichtung, einmal
mit, und der Unterschied ist sofort sichtbar.

30 bis 50: Der Flaschenhals. Ein kleiner Autoencoder, vorher trainiert und als fertiges
Modell mitgeliefert, wird aufgemacht: 1024 Bildpunkte hinein, acht Zahlen in der Mitte, 1024
wieder hinaus. Die Rekonstruktionen neben den Originalen.

Dann der Vergleich über die Größe der Mitte, mit 32, 8 und 2 Zahlen. Das sind drei getrennt
trainierte Modelle, nicht ein Regler an einem Modell, und das wird auch so gesagt: man kann
einen Flaschenhals nicht im Betrieb enger drehen. Alle drei laufen über dieselben fünf
Häuser, darunter ein Hofhaus und ein Eckhaus.

Was dabei zuerst verlorengeht, wird nicht behauptet, sondern gefragt. Die Vermutung im Raum
ist: zuerst die Ecken, dann die Höfe. Ob das stimmt, steht am Ende der Einheit an der Tafel,
und es kann auch anders ausgehen.

50 bis 60: Pause.

60 bis 95: Die Karte, und wie sie zustande kommt. Erst die Frage, wie aus acht Zahlen zwei
werden: der Schatten eines Gegenstands ist auch zweidimensional und trotzdem erkennt man ihn,
und genau das macht die Projektion, sie wirft die acht Zahlen so auf eine Ebene, dass
möglichst viel Unterschied erhalten bleibt. Zwei Minuten, an einer gedrehten Punktwolke
gezeigt, keine Formel.

Dann die Karte selbst: jeder Punkt ein Haus, beim Überfahren sein Grundriss, Farbe nach
Bauperiode. Ob benachbarte Punkte wirklich ähnliche Formen sind, wird nachgesehen und nicht
versprochen: fünf zufällig gezogene Häuser, daneben ihre nächsten Nachbarn, und die Gruppe
urteilt selbst. Wenn es nicht funktioniert, ist auch das ein Ergebnis, und die Frage lautet
dann, woran es liegt.

Zum Schluss die Reise: zwei Häuser auswählen und die Zwischenschritte zeichnen lassen, eine
Form, die sich in die andere verwandelt. Das ist der erste Moment im Semester, in dem etwas
entsteht, das nicht in den Daten stand, und der Einstieg in alles, was danach kommt.

95 bis 105: Kurztest.

105 bis 120: Hausübung, Fragen, Puffer. Ausblick: wenn man in dieser Karte spazieren gehen
kann, kann man dann auch an einer Stelle stehenbleiben und sagen, hier soll ein Haus sein?

## Was man sieht

**Drei Darstellungen nebeneinander.** Ein Haus, dreimal: zwei Zahlen, ein Raster, eine
Kantenfolge. Darunter jeweils, wie viele Zahlen das sind. Der Sprung von 2 auf 1024 ist der
Punkt.

**Das Rasterbild live.** Regler für die Auflösung, von 8 über 32 auf 128, daneben das
Originalpolygon. Man sieht, ab wann ein Hof verschwindet.

**Rekonstruktion gegen Original.** Fünf echte Grundrisse, darunter drei Reihen mit den
Rückgaben der Modelle mit 32, 8 und 2 Zahlen, darunter die Unterschiede als Karte. Von oben
nach unten wird es unschärfer, und man sieht an denselben Häusern, was jeweils zuerst geht.

**Die Karte der Formen.** Punktwolke der Codes, Grundriss im Hover, Farbe nach Bauperiode.
Daneben die Nachbarschaftsprobe: fünf Häuser mit ihren je drei nächsten Nachbarn als
Bildreihe. Dazu der Weg zwischen zwei ausgewählten Häusern als Animation, Schritt für
Schritt, mit den erzeugten Zwischenformen.

Alle Bilder liegen vorgerechnet bereit, Codes, Vorschaubilder und Projektion. In der Stunde
wird nichts trainiert und nichts neu projiziert, sonst steht der Hub.

Dazu der Vorbereitungsclip und ein Merkbild: ein Regal voller Grundrisse, sortiert nicht nach
Adresse, sondern nach Ähnlichkeit, mit fließenden Übergängen zwischen den Fächern.

## Was zählt

Kurztest drei Punkte, Hausübung zehn Punkte, davon sechs auf die Interpretation. Aufgabe:
ein selbst gewähltes Haus durch alle drei Modelle schicken, die Rekonstruktionen abbilden,
und danach das Werkzeug benutzen, das dabei entsteht: den eigenen Grundriss in die Karte
legen und die zehn ähnlichsten Wiener Häuser ausgeben lassen. In fünf Sätzen: welche
Eigenschaft der Form bei welcher Flaschenhalsgröße verlorengeht, und ob die zehn Nachbarn
für einen Entwurf brauchbar wären oder nicht.

Die sechs Kriterien stehen in der Angabe, und "die Nachbarn taugen nichts, und zwar aus
diesem Grund" ist eine vollwertige Antwort.

Es gilt `kursregeln.md`: die Auflösung der Codezeilen kommt nach zehn Minuten, der Code ist
nie der Grund für eine fehlende Abgabe.

## Offene Punkte

- Der Autoencoder wird vorher trainiert und als Gewichtsdatei mitgeliefert. Training in der
  Stunde ist nicht drin, und auf CPU auch nicht nötig.
- Ausrichtung der Polygone: Schwerpunkt aus der Fläche, nicht aus den Eckpunkten, Hauptachse
  waagrecht, gleichmäßig skaliert mit Rand statt in beide Richtungen gestreckt, Höfe erhalten.
  Zwei Fallen: bei fast quadratischen Blöcken ist die Hauptachse instabil, und die Richtung
  kann um 180 Grad kippen. Beides vorher ansehen und die Regel festschreiben.
- Ob 1073 Grundrisse für eine brauchbare Karte reichen, ist offen. Das Skript kann mehr
  Ausschnitte ziehen, mehrere tausend sind kein Problem. Vor der Freigabe ein Pilot: Lernkurve
  ansehen, Nachbarn von Hand prüfen, Zwischenformen auf Löcher und zerfallene Teile ansehen.
  Wenn die Karte klumpt, wird die Einheit umgebaut, nicht die Aussage weichgespült.
- Die drei Modelle mit 32, 8 und 2 Zahlen müssen separat trainiert und als Dateien mitgeliefert
  werden.