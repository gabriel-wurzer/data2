# Einheit 5: Einen Grundriss erfinden

259.075 VU Data-integrated Algorithmic Design Processes II
Fünfte von sieben Einheiten, Freitag 09:00 bis 11:00, EDV-Labor PC5, rund 20 Studierende

## Wo wir herkommen

Einheit 4 endete mit einer Frage: wenn man in der Karte der Formen spazieren gehen kann, kann
man dann auch an einer Stelle stehenbleiben und sagen, hier soll ein Haus sein? Die Antwort
lautet: mit dem Autoencoder von letzter Woche nicht, und der Grund dafür ist die eigentliche
Lektion dieser Einheit.

## Lernziele

Am Ende der Einheit können die Studierenden

- vorführen, dass ein gewöhnlicher Autoencoder an einer selbst gewählten Stelle seines
  Codeaums Unsinn ausgibt, und erklären, warum,
- den Unterschied zwischen einem Punkt und einer Verteilung im Code benennen und sagen, was
  der variational autoencoder daran ändert,
- aus dem trainierten Modell neue Grundrisse ziehen und die Temperatur der Ziehung verstellen,
- an zehn selbst erzeugten Formen beurteilen, welche davon ein Entwurf sein könnten und welche
  nicht, und das Urteil begründen,
- sagen, was "das Modell hat einen neuen Grundriss erfunden" heißt und was es nicht heißt.

## Ablauf

0 bis 15: Der Gegenbeweis zuerst. Zwei Codes aus Einheit 4 nehmen, einen Punkt genau dazwischen
wählen, decodieren. Manchmal kommt etwas Brauchbares, oft ein grauer Fleck. Dann dasselbe an
einer zufälligen Stelle des Raums: fast immer Unsinn. Der Autoencoder hat nie gelernt, was
zwischen den Trainingshäusern liegt, er hat nur gelernt, sie einzeln wieder auszugeben.

15 bis 35: Die Reparatur, und sie ist klein. Statt eines Punktes gibt der Encoder einen
Mittelwert und eine Streuung aus; gezogen wird daraus, und ein zweiter Term im Verlust hält die
Wolken beieinander. Das ist der *variational autoencoder*. Vorgeführt wird der Effekt, nicht
die Herleitung: dieselbe Karte, einmal mit Löchern, einmal ohne, und dieselbe Strecke zwischen
denselben zwei Häusern, einmal mit Aussetzern, einmal durchgehend.

Der zweite Term wird benannt und in einem Satz erklärt, die Formel steht als Fußnote da. Wer
sie will, findet sie; geprüft wird sie nicht.

35 bis 50: Ziehen. Zwanzig Grundrisse aus dem Nichts, als Bildraster. Dann der Regler für die
Temperatur: eng gezogen kommen brave Durchschnittshäuser, weit gezogen kommt Unfug mit
gelegentlich etwas Interessantem. Das ist dieselbe Wahl, die später bei Bildern und bei Sprache
wieder auftaucht, und sie wird hier zum ersten Mal benannt.

50 bis 60: Pause.

60 bis 80: Bedingt ziehen. Die Bauperiode kommt als zusätzlicher Eingang dazu, und dann lässt
sich ziehen mit Vorgabe: gib mir einen Gründerzeitgrundriss, gib mir einen aus der
Zwischenkriegszeit. Ob die Unterschiede echt sind oder eingebildet, wird an der Gruppe geprüft:
zehn Formen, ohne Beschriftung, zuordnen lassen. Wenn es nicht funktioniert, ist auch das ein
Ergebnis.

80 bis 95: Der ehrliche Teil. Was hier entsteht, sind Rasterbilder von Umrissen, keine
Grundrisse: keine Wände, keine Räume, keine Türen, keine Statik. Ein erzeugter Umriss ist ein
Vorschlag für eine Form, nicht ein Entwurf, und der Weg von hier zu einem Gebäude ist die
Arbeit, für die es die Studierenden gibt. Das wird ausgesprochen, weil es sonst jemand anderer
ausspricht, und zwar in der Prüfung.

95 bis 105: Kurztest.

105 bis 120: Hausübung, Fragen, Puffer. Ausblick: die Formen kamen aus Zahlen. Was passiert,
wenn der Eingang Text ist?

## Was man sieht

**Das Loch im Raum.** Links die Karte aus Einheit 4 mit den Codes der Trainingshäuser, rechts
dieselbe Karte, eingefärbt danach, wie brauchbar die Decodierung an dieser Stelle ist. Die
weißen Flecken sind das Argument.

**Die Strecke zwischen zwei Häusern.** Dieselben zwei Häuser, zweimal: mit dem Autoencoder
ruckelt es, mit dem VAE läuft es durch. Als Bildreihe nebeneinander, nicht als Animation, damit
man vergleichen kann.

**Das Raster der Gezogenen.** Fünf mal vier erzeugte Umrisse, mit Regler für die Temperatur.
Bei jedem Rutsch neu gezogen, mit festem Startwert, damit alle dasselbe sehen.

**Die Blindprobe.** Zehn Formen ohne Beschriftung, die Gruppe ordnet sie zwei Bauperioden zu,
danach wird aufgedeckt. Das ist der einzige Programmpunkt, bei dem die Einheit auch scheitern
darf.

Alle Modelle sind vorher trainiert und liegen als Gewichtsdateien bereit. In der Stunde wird
gezogen und decodiert, nicht trainiert.

## Was zählt

Kurztest drei Punkte, Hausübung zehn Punkte, davon sechs auf die Interpretation. Aufgabe: zehn
Formen ziehen, abbilden, und für jede in einem Satz sagen, ob sie als Ausgangspunkt für einen
Entwurf taugt. Dazu die beiden Fragen: an welcher Temperatur hört Vielfalt auf und fängt
Unfug an, und was fehlt einem erzeugten Umriss auf einen Grundriss.

"Keine der zehn taugt, und zwar aus diesem Grund" ist eine vollwertige Antwort.

## Offene Punkte

- Der VAE muss vorher trainiert und als Datei mitgeliefert werden, ebenso das bedingte Modell.
  Auf CPU geht das über Nacht, in der Stunde nicht.
- Ob die Bauperiode als Bedingung überhaupt sichtbare Unterschiede erzeugt, ist offen. Vor der
  Freigabe die Blindprobe selbst machen. Wenn niemand die Perioden auseinanderhält, wird der
  Programmpunkt zur offenen Frage umgebaut und nicht schöngerechnet.
- Temperatur und Startwert so festlegen, dass bei zwanzig Kerneln dasselbe herauskommt.
