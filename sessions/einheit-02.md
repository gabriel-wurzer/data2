# Einheit 2: Vom Neuron zum Netz

259.075 VU Data-integrated Algorithmic Design Processes II
Freitag, 23.10.2026, 09:00 bis 11:00, EDV-Labor PC5, rund 20 Studierende

## Wo wir herkommen

Einheit 1 endete mit einem Modell, das bei einem Fehler von 50 stehenbleibt, und mit der
Diagnose: dem Modell fehlt der U-Wert. Diese Einheit gibt ihm den U-Wert, zeigt, warum das
mit den Einstellungen der letzten Woche trotzdem nicht funktioniert, und endet bei etwas, das
keine Gerade mehr ist.

## Lernziele

Am Ende der Einheit können die Studierenden

- ein Modell mit mehreren Eingangsgrößen aufschreiben,
- erklären, warum Eingangsgrößen mit verschiedenen Größenordnungen normiert werden, und die
  gefundenen Gewichte wieder in die ursprünglichen Einheiten zurückrechnen,
- die Matrixform lesen, wenn mehrere Neuronen gleichzeitig rechnen,
- zeigen, dass zwei hintereinandergeschaltete lineare Schichten wieder eine lineare Schicht
  sind, und sagen, was daraus folgt,
- erklären, wie mehrere ReLU-Neuronen nebeneinander eine gekrümmte Kurve zusammensetzen,
- sagen, was ein Fehler von null über die Güte eines Modells aussagt und was nicht.

## Ablauf

0 bis 15: Die zweite Eingangsgröße. `hwb = w1 * kompaktheit + w2 * u_wert + b`, dieselbe
Schleife wie letzte Woche, nur ein Gewicht mehr. Sie läuft, und sie kommt nicht an: nach
dreitausend Schritten steht der Fehler bei 43, nicht bei null. Das ist kein Unfall, das ist
der Einstieg. Die beiden Eingänge haben verschiedene Größenordnungen, der U-Wert liegt um
1,4, die Kompaktheit um 7, und der Abstieg kriecht durch ein schiefes Tal.

15 bis 35: Normieren. Beide Eingänge auf Mittelwert null und Streuung eins, dieselbe
Lernrate, zweihundert Schritte statt dreitausend, Fehler praktisch null. Dann die Rückrechnung
in die ursprünglichen Einheiten, und dort stehen 9, 62 und 18: die Zahlen aus der Formel, mit
der die Zielgröße erzeugt wurde.

Das ist kein Triumph, sondern ein Taschenspielertrick, und er wird auch so benannt. Das
Modell hat eine Rechenvorschrift rückwärts ausgefischt, die vorher jemand hineingesteckt hat.
Über Häuser hat es nichts gelernt, und bei gemessenen Verbräuchen sähe es nie so aus. Der
praktische Ertrag der zwanzig Minuten ist das Normieren, und das braucht man den Rest des
Semesters, sobald Geometrie, Material und Nutzung im selben Modell stehen.

35 bis 50: Die Grenze. Ein zweiter Datensatz, dessen Zielgröße nach einer bewusst krummen
Vorschrift erzeugt ist, offen im Notebook abgedruckt und nicht als Physik verkauft. Das beste
gerade Modell liegt systematisch daneben, sichtbar an den Residuen, die auf einer Seite
sammeln. Ab hier hilft kein besserer Abstieg mehr, es fehlt dem Modell an Form.

50 bis 60: Pause.

60 bis 75: Der naheliegende Versuch: zwei lineare Schichten stapeln. Das Ergebnis ist wieder
eine Gerade, mit Reglern vorgeführt und in zwei Zeilen nachgerechnet. Der Frust ist der
Lerneffekt, und er stellt die Frage, was zwischen die Schichten gehört.

75 bis 95: Der Knick. ReLU, an einer Stelle abgeknickt, mehr ist es nicht. Vier solche
Neuronen nebeneinander, jedes mit eigenem Knick, darunter ihre gewichtete Summe: daraus wird
die Kurve. Weil jetzt vier Neuronen gleichzeitig rechnen, wird hier auch die Matrixform
gebraucht und deshalb hier eingeführt, nicht vorher: die vier Gewichtsvektoren stehen als
Zeilen einer Matrix, und der ganze Vorwärtsdurchlauf ist eine Multiplikation. Das läuft als
vorgeführtes, kommentiertes Notebook mit Reglern, nicht als Tippübung. Zum Schluss dieselben
vier Neuronen in zehn Zeilen PyTorch, damit man gesehen hat, dass es dasselbe ist; geschrieben
wird darin erst in Einheit 3. Diese zehn Zeilen bleiben als benannte Merkkarte im Notebook
stehen, mit denselben Namen und in derselben Reihenfolge, in der sie in Einheit 3 wieder
auftauchen. Wird die Vorführung hier hudelig, fällt nächste Woche die erste halbe Stunde um.

95 bis 105: Kurztest.

105 bis 120: Hausübung, Fragen, Puffer. Dazu der Ausblick auf nächste Woche, als Frage
gestellt: was passiert, wenn ein Netz mit genug Knicken durch jeden einzelnen Punkt geht?
Wer darauf antwortet, dass das gut ist, bekommt in Einheit 3 das Gegenteil gezeigt.

## Was man sieht

**Die Ebene statt der Geraden.** Die Punktwolke wird dreidimensional: Kompaktheit, U-Wert,
Bedarf. Das Modell ist eine Ebene, drehbar, und die Punkte liegen nach dem Normieren fast
exakt darauf. Das macht die Rekonstruktion der Formel sichtbar, statt sie zu behaupten.

**Warum es vorher nicht ging.** Zwei Schnitte durch die Fehlerlandschaft nebeneinander, mit
festem Achsenabschnitt und beschrifteten Achsen: links die Rohdaten mit dem langen,
zickzackenden Weg, rechts die normierten mit dem kurzen. Gleiche Lernrate, gleiche
Schrittzahl, unterschiedliches Ende.

**Zwei Geraden bleiben eine Gerade.** Je ein Regler für die beiden Schichten und daneben die
Kurve, die herauskommt. Egal wie man schiebt, sie bleibt gerade. Der Frust ist der
Lerneffekt.

**Vom Knick zur Kurve.** Oben die vier ReLU-Neuronen einzeln, jedes mit eigenem Knickpunkt,
darunter ihre gewichtete Summe gegen die Zielkurve. Ein Regler für die Anzahl der Neuronen,
von einem bis acht. Die Neuronen stehen nebeneinander, nicht hintereinander, und genau das
soll man sehen.

Dazu der Vorbereitungsclip von einer Minute und ein Merkbild: mehrere Rampen mit
verschiedenen Knickpunkten, übereinandergelegt zu einer weichen Kurve.

## Was zählt

Kurztest drei Punkte, Hausübung zehn Punkte, davon sechs auf die Interpretation. Aufgabe:
das vorgeführte Netz auf die krummen Daten anpassen, indem nur die Anzahl der Neuronen und
die Lernrate geändert werden, den erreichten Fehler berichten, und in fünf Sätzen
beantworten, was der Fehler von fast null aus dem ersten Teil der Einheit über die Güte eines
Gebäudemodells aussagt. Die erwartete Antwort ist: nichts.

Tests wieder offen, Bewertungslauf vor der Abgabe aufrufbar.

## Verschoben nach Einheit 3

Trainings- und Testaufteilung, Überanpassung und das Bild mit den auseinanderlaufenden
Kurven. Das braucht verrauschte Daten und eine halbe Einheit für sich, und es in die letzten
fünfzehn Minuten zu quetschen hieße, es zu behaupten statt zu zeigen.

## Offene Punkte

- Der krumme Datensatz muss gebaut werden, mit offen abgedruckter Formel und ohne
  physikalische Erzählung darüber.
- PyTorch im Hub-Image, sonst fällt die Vorführung aus. Gehört in die Anfrage ans dataLAB.
- Generalprobe mit zwanzig gleichzeitigen Kerneln, diesmal mit den Reglern.
