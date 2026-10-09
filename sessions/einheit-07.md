# Einheit 7: Rauschen wegnehmen, und wozu das alles

259.075 VU Data-integrated Algorithmic Design Processes II
Siebte von sieben Einheiten, Freitag 09:00 bis 11:00, EDV-Labor PC5, rund 20 Studierende

## Wo wir herkommen

Einheit 5 hat Formen aus einer Verteilung gezogen, Einheit 6 Buchstaben. Beides war dasselbe
Prinzip mit verschiedenen Ausgängen. Die Bildmodelle, von denen alle reden, arbeiten anders, und
der Unterschied lässt sich an den Grundrissen aus Einheit 4 in einer halben Stunde vorführen.

Danach wird der Bogen zurückgeschlagen. Der Kurs hat sieben Wochen lang ein Ersatzmodell gebaut,
und das gehört am Ende benannt.

## Lernziele

Am Ende der Einheit können die Studierenden

- beschreiben, wie ein Diffusionsmodell ein Bild erzeugt, und sagen, was daran der gelernte Teil
  ist,
- die Zahl der Schritte verstellen und die Wirkung an den erzeugten Grundrissen zeigen,
- erklären, was LoRA tut, und an den Zahlen zeigen, wie wenige Gewichte dabei bewegt werden,
- den Unterschied zwischen Vortraining, Feintuning und Prompt benennen und sagen, welches davon
  wie viel kostet,
- sagen, was ein Ersatzmodell ist, wo die Grenzen seiner Gültigkeit liegen und wie man sie
  prüft.

## Ablauf

0 bis 10: Rückwärts. Ein Grundriss aus Einheit 4, und dann zwanzig Bilder, in denen schrittweise
Rauschen daraufkommt, bis nichts mehr zu sehen ist. Das ist der Vorwärtsweg, und er braucht kein
Modell, sondern nur einen Zufallsgenerator. Die Frage der Einheit lautet: kann man diesen Weg
umkehren?

10 bis 35: Das Modell lernt genau eine Sache, und sie ist kleiner als erwartet: aus einem
verrauschten Bild und der Angabe, wie stark es verrauscht ist, das Rauschen zu schätzen. Das ist
wieder eine Zahl-hinein-Zahl-heraus-Aufgabe mit quadratischem Fehler, also genau das, was seit
Einheit 1 gebaut wird. Das Erzeugen ist dann nur die Schleife: Rauschen hinlegen, schätzen,
abziehen, wiederholen.

Das Modell ist vortrainiert und wird mitgeliefert. In der Stunde wird gezogen.

35 bis 50: Die Schrittzahl. Regler von 2 bis 200, daneben die erzeugten Grundrisse. Bei zwei
Schritten kommt Matsch, bei zweihundert kommen Formen, und irgendwo dazwischen wird es nicht
mehr besser. Das ist derselbe Regler, der in jeder Bildoberfläche "steps" heißt, und ab jetzt
weiß jeder, warum er Zeit kostet.

50 bis 60: Pause.

60 bis 80: LoRA, am eigenen Modell. Das trainierte Diffusionsmodell wird eingefroren. Daneben
kommen zwei kleine Matrizen, deren Produkt die Form einer Gewichtsmatrix hat, und nur die werden
trainiert, auf einer Untermenge: nur Hofhäuser. Nach zwei Minuten zieht dasselbe Modell mit
aufgestecktem LoRA Hofhäuser und ohne LoRA wieder alles. Danach die Zahlen: wie viele Gewichte
hat das Grundmodell, wie viele das LoRA, wie viele Prozent sind das.

Hier fällt auch der Satz, warum es diese Technik gibt: ein großes Modell noch einmal ganz zu
trainieren kostet ein Rechenzentrum, ein LoRA kostet einen Nachmittag, und beide Ergebnisse
kann man tauschen wie einen Schlüssel.

80 bis 95: Der Bogen. Einheit 1 hat gefragt, wie lange eine Simulation für hundert Varianten
braucht. Was dieser Kurs seither gebaut hat, heißt in der Literatur *surrogate model*: ein
schnelles Modell, das ein langsames nachahmt. Was davon gilt, gilt nur im geprüften Bereich; was
außerhalb liegt, ist Extrapolation, und die steht nirgends drauf.

Dazu die drei Fragen, die man einem fremden Modell stellt, bevor man ihm etwas glaubt: woher
kommen die Daten, was war der Testteil, und wo liegen die Grenzen des geprüften Bereichs. Wer
diese drei Fragen stellen kann, hat den Kurs verstanden.

95 bis 105: Kurztest.

105 bis 120: Abschluss, Fragen, und der Hinweis, was als Nächstes zu lernen wäre und wo.

## Was man sieht

**Die Rauschleiter.** Ein Grundriss in zwanzig Stufen bis zum Rauschen, als Bildreihe. Darunter
dieselbe Reihe rückwärts, erzeugt.

**Die Schrittzahl.** Regler, daneben ein Raster von zwölf erzeugten Grundrissen, fester
Startwert, damit man den Vergleich führen kann.

**Mit und ohne LoRA.** Zwei Raster nebeneinander, dasselbe Modell, dieselben Startwerte, einmal
mit aufgestecktem LoRA und einmal ohne. Darunter die Gewichtszählung als zwei Balken, der eine
kaum sichtbar.

**Der Bogen.** Die Punktwolke aus Einheit 1, daneben das, was in Einheit 7 daraus geworden ist.
Ein Bild, zwei Minuten, keine Nostalgie.

## Was zählt

Kurztest drei Punkte, Hausübung zehn Punkte, davon sechs auf die Interpretation. Aufgabe: ein
eigenes LoRA auf eine selbst gewählte Untermenge der Wiener Grundrisse trainieren, mit und ohne
ziehen, beides abbilden. In fünf Sätzen: ob der Unterschied sichtbar ist, woran man das
festmacht, und was man an der Auswahl der Untermenge ändern würde.

Dazu eine halbe Seite zum Kurs: das Modell aus Einheit 3, und die drei Fragen darauf angewendet.

## Offene Punkte

- Das Diffusionsmodell auf 32 mal 32 Grundrissen muss vortrainiert werden. Auf CPU über Nacht,
  Architektur klein halten, sonst wird das Ziehen in der Stunde zu langsam.
- Ob zweihundert Schritte mal zwölf Bilder mal zwanzig Kernel der Hub aushält, vorher messen.
  Notfalls die Schrittzahl deckeln und den Regler nur bis 50 laufen lassen.
- Die Hofhaus-Untermenge muss ausgezählt werden. Wenn es zu wenige sind, eine andere Eigenschaft
  nehmen, etwa besonders schlanke Grundrisse.
- Für den Bogen am Schluss die Zahlen aus Einheit 1 und 3 nebeneinanderlegen, damit der Vergleich
  stimmt und nicht nur behauptet ist.
