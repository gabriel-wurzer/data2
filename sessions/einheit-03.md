# Einheit 3: Wenn das Modell auswendig lernt

259.075 VU Data-integrated Algorithmic Design Processes II
Dritte von sieben Einheiten, Freitag 09:00 bis 11:00, EDV-Labor PC5, rund 20 Studierende

## Wo wir herkommen

Einheit 2 endete mit der Frage, was passiert, wenn ein Netz genug Knicke hat, um durch jeden
einzelnen Punkt zu gehen. Diese Einheit gibt die Antwort, und sie ist die wichtigste des
Semesters: ein Modell, das die Trainingsdaten perfekt trifft, ist meistens das schlechtere.

Dazu kommt der Schritt, den Einheit 2 aufgeschoben hat: hier greifen die Studierenden zum
ersten Mal selbst in PyTorch-Code ein.

## Die Daten, und warum Rauschen daraufliegt

Bis jetzt war die Zielgröße glatt gerechnet, und jedes ausreichend große Modell konnte sie
beliebig genau treffen. Ab heute liegt Rauschen darauf. Der Grund ist banal: wir haben für
Wien keinen offenen Datensatz gefunden, der den gemessenen Verbrauch einzelner Gebäude
enthält, und was es an Verbrauchsdaten gibt, ist aggregiert. Ob solche Daten
personenbezogen wären, hängt davon ab, ob sich einzelne Haushalte daraus erkennen lassen, und
ist eine Frage für sich, nicht der Grund unserer Entscheidung. Wir simulieren also
Messunsicherheit und schreiben das in die erste Zelle. Der Rest des Semesters hängt daran,
dass Signal und Zufall nicht mehr auseinanderzuhalten sind, wenn man nur lange genug
trainiert.

## Lernziele

Am Ende der Einheit können die Studierenden

- ein kleines Netz in PyTorch trainieren und die Rolle von Modell, Verlustfunktion,
  Optimierer und Schleife benennen,
- Daten in Trainings-, Validierungs- und Testteil zerlegen, in dieser Reihenfolge, und sagen,
  wofür jeder Teil da ist,
- an zwei Fehlerkurven ablesen, wo der beste Abbruchzeitpunkt liegt,
- zwei Gegenmittel anwenden, kleineres Netz und früher abbrechen, und ihre Wirkung zeigen,
- begründen, warum man den Testteil erst am Schluss ansieht, und was diese Zahl aussagt und
  was nicht.

## Ablauf

0 bis 20: Dasselbe Netz wie letzte Woche, jetzt in PyTorch. Das Gerüst steht da, offen sind
drei Zeilen: der Vorwärtsdurchlauf, das Nullsetzen der Gradienten und der Optimierungsschritt.
Es sind dieselben Zeilen, mit denselben Namen und in derselben Reihenfolge wie in der
Vorführung aus Einheit 2, und sie stehen dort auch als Merkkarte im Notebook. Direkt darunter
läuft eine Prüfzelle, die Form und Datentyp der Tensoren anschreit, bevor irgendwer eine halbe
Stunde an einem stillen Broadcasting-Fehler sitzt.

Nach zehn Minuten wird die Auflösung der drei Zeilen freigeschaltet, für alle, ohne Nachfrage
und ohne Abzug, siehe `kursregeln.md`. Niemand verliert die eigentliche Aufgabe an einer
Klammer, und niemand kann sich hinter einer Klammer verstecken.

Daneben, im selben Notebook, eine kurze Fehlerkunde: die vier Meldungen, die in diesen zwanzig
Minuten tatsächlich auftreten, auf Deutsch übersetzt. Was "shape mismatch" heißt und wo man
nachsieht, warum ein `Double` auf ein `Float` trifft, was passiert, wenn `zero_grad()` fehlt,
und warum eine Zelle Unsinn rechnet, wenn man sie in falscher Reihenfolge ausgeführt hat. Wer
festsitzt, liest zuerst dort nach und hebt dann die Hand.

20 bis 35: Die Aufteilung, und zwar in der richtigen Reihenfolge. Zuerst teilen, dann
normieren, und die Normierung nur aus dem Trainingsteil bestimmen. Warum das nicht egal ist,
wird am Gegenbeispiel gezeigt: wer vorher normiert, hat die Testhäuser schon angefasst.

35 bis 50: Das Bild der Einheit. Trainings- und Validierungsfehler über die Schritte, in einem
Diagramm mitgezeichnet, mit einer Linie am tiefsten Punkt der Validierungskurve. Gerechnet
wird das auf dem krummen Spielzeugdatensatz aus Einheit 2 mit aufgelegtem Rauschen und einem
absichtlich zu großen Netz, weil die Kurve nur dann zuverlässig umdreht. Die Einstellungen
sind vorher über mehrere Startwerte geprüft und liegen fest; als Rückfall gibt es einen
aufgezeichneten Lauf.

Die Sprechweise dabei ist genau: der tiefste Punkt der Validierungskurve schätzt, wann man
aufhören sollte. Er markiert keinen Moment, in dem Lernen in Auswendiglernen umschlägt.

50 bis 60: Pause.

60 bis 80: Gegenmittel, mit Reglern. Erst die Anzahl der Neuronen kleiner drehen und zusehen,
wie die Kurven zusammenrücken. Dann beim tiefsten Punkt abbrechen statt weiterzutrainieren.
Beides ausprobieren, beides erklären können.

80 bis 95: Der Blick auf den Testteil, gemeinsam, einmal. Die Zahl ist die Schätzung für neue
Häuser derselben Art, mehr nicht: sie kann besser ausfallen als die Validierungszahl, und wenn
das passiert, ist das kein Fehler, sondern Zufall bei 160 Häusern. Was sie nicht sagt: wie
sich das Modell in einem anderen Bezirk oder bei einer anderen Bauweise schlägt.

95 bis 105: Kurztest.

105 bis 120: Hausübung, Fragen, Puffer, und der Ausblick: bisher waren die Eingänge Zahlen,
die jemand ausgesucht hat. Was macht man, wenn der Eingang ein Grundriss ist?

## Was man sieht

**Die zwei Kurven.** Trainings- und Validierungsfehler, mitgezeichnet, mit Markierung am
tiefsten Punkt. Aktualisiert wird im Block alle fünfzig Schritte, nicht bei jedem, sonst
erstickt der Hub an Nachrichten. Wenn das Bild nur eines hinterlässt, dann dieses.

**Der Fächer.** Vier Netze mit zwei, vier, sechzehn und vierundsechzig Neuronen über der
krummen Spielzeugkurve aus Einheit 2, beschriftet als genau dieser Datensatz und nicht als
Wien. Links zu stumpf, rechts zu zappelig. Die vier Läufe sind vorgerechnet und liegen als
Kurven bereit, gerechnet wird in der Stunde nichts davon.

**Rauschen sichtbar machen.** Die Punkte mit und ohne Rauschen übereinander, Regler für die
Stärke, daneben das jeweils neu angepasste Modell aus dem Vorrat. Man sieht, wie es anfängt,
dem Zufall hinterherzulaufen.

**Der Testteil als verschlossene Schachtel.** Die Punktwolke dreifarbig, der Testteil
ausgegraut, bis er in Minute 80 aufgedeckt wird.

Dazu der Vorbereitungsclip und ein Merkbild: jemand, der die Prüfungsangabe des Vorjahres
auswendig kann und bei der leicht anderen Frage danebensteht.

## Was zählt

Kurztest drei Punkte, Hausübung zehn Punkte, davon sechs auf die Interpretation. Aufgabe: das
Netz auf den verrauschten Daten so einstellen, dass der Validierungsfehler am kleinsten wird,
das Modell an dieser Stelle einfrieren und abgeben. Der Testteil der Hausübung ist ein
eigener, zurückgehaltener Satz Häuser, den niemand vorher sieht; er wird beim Bewertungslauf
angelegt.

Die sechs Interpretationspunkte hängen an sechs Kriterien, die in der Angabe stehen: Lage des
Abbruchpunkts mit Begründung aus der eigenen Kurve, Wirkung der Netzgröße mit Beleg,
Reihenfolge von Teilen und Normieren, Aussage des Testwerts, eine benannte Grenze dieser
Aussage, und eine Entwurfsfolgerung. Eine flache Validierungskurve ist eine zulässige
Beobachtung und kostet keinen Punkt, solange sie belegt und richtig gedeutet ist. Ein
besonders guter Testwert bringt keinen Punkt, das steht ausdrücklich in der Angabe.

## Offene Punkte

- Netzgröße und Rauschstärke für die Vorführung festzurren. Erste Rechnungen zeigen: vier
  Neuronen genügen nicht, die Kurve bleibt flach. Mit vierundsechzig Neuronen und kräftigem
  Rauschen dreht sie, aber nicht bei jedem Startwert gleich deutlich. Also Startwert fest,
  Lauf vorher zehnmal prüfen, Aufzeichnung als Rückfall bereitlegen.
- PyTorch im Hub-Image, ohne das fällt die erste halbe Stunde aus.
- Generalprobe mit zwanzig gleichzeitigen Kerneln, diesmal mit mitgezeichneten Kurven.