# Einheit 6: Was ein Sprachmodell tut

259.075 VU Data-integrated Algorithmic Design Processes II
Sechste von sieben Einheiten, Freitag 09:00 bis 11:00, EDV-Labor PC5, rund 20 Studierende

## Wo wir herkommen

Fünf Einheiten lang war der Eingang eine Zahl oder ein Bild, und die Zielgröße war eine Zahl.
Heute ist beides Text, und damit ändert sich die Verlustfunktion zum ersten Mal seit Einheit 1.
Das ist der eigentliche Inhalt: nicht dass Sprachmodelle groß sind, sondern dass sie eine andere
Frage stellen.

Die Studierenden benutzen diese Werkzeuge seit zwei Jahren täglich. Der Zweck der Einheit ist,
dass sie danach sagen können, was darin passiert, und zwar in Begriffen, die sie selbst gebaut
haben.

## Die Daten

Die Straßennamen von Wien, rund 6900 Stück, aus dem offenen Datenportal der Stadt. Kein Text
aus dem Netz, nichts Urheberrechtliches, nichts Peinliches, und jeder im Raum weiß sofort, ob
ein erzeugter Name plausibel klingt oder nicht. Trainiert wird auf Zeichen, nicht auf Wörtern:
das Vokabular hat rund sechzig Einträge und passt auf eine Folie.

## Lernziele

Am Ende der Einheit können die Studierenden

- erklären, was ein Token ist, und an einem Beispiel zeigen, dass die Zerlegung eine
  Entscheidung und keine Naturkonstante ist,
- sagen, warum ein Modell, das Text erzeugt, eine Wahrscheinlichkeit je möglichem nächsten
  Token ausgibt und nicht einen Text,
- die Kreuzentropie als Verlustfunktion benennen und sagen, wofür sie bestraft,
- ein kleines Zeichenmodell trainieren und mit der Temperatur steuern,
- erklären, warum ein Sprachmodell erfundene Angaben in demselben Ton ausgibt wie richtige, und
  was daraus für die Verwendung im Büro folgt.

## Ablauf

0 bis 15: Zerlegen. Derselbe Satz, dreimal zerlegt: in Zeichen, in Wörter, in Wortstücke. Wie
viele Einträge hat das Vokabular jeweils, wie lang wird die Folge, was passiert mit
"Lerchenfelder"? Danach ist klar, warum Modelle Wortstücke verwenden und warum ein Modell
manchmal an Zahlen scheitert.

15 bis 30: Die neue Frage. Bisher: gib eine Zahl aus, der Fehler ist der Abstand. Jetzt: gib für
jeden der sechzig möglichen nächsten Buchstaben eine Wahrscheinlichkeit aus, und der Fehler ist,
wie überrascht das Modell vom tatsächlichen nächsten Buchstaben war. Das ist die Kreuzentropie,
und sie wird an einem Balkendiagramm vorgeführt, nicht an einer Formel: drei Vorhersagen für
denselben Buchstaben, die dazugehörigen drei Verlustwerte.

30 bis 50: Das Modell. Ein Zeichenmodell, das aus den letzten acht Buchstaben den nächsten
schätzt. Die Architektur ist die aus Einheit 2, nur mit einem Ausgang je Buchstabe. Es trainiert
in der Stunde, auf CPU, in unter zwei Minuten, und danach zieht jeder im Raum eigene Namen.

50 bis 60: Pause.

60 bis 75: Temperatur. Derselbe Regler wie in Einheit 5, jetzt an Buchstaben. Kalt gezogen kommt
"Straßengasse" und danach nichts Neues mehr, heiß gezogen kommt Buchstabensalat. Dazwischen
liegen Namen, die es nicht gibt und die es geben könnte. Die Gruppe entscheidet, welche.

75 bis 90: Von hier zu ChatGPT. Was ändert sich, wenn man dasselbe Prinzip auf Wortstücke
anwendet, den Kontext von acht auf hunderttausend Zeichen verlängert, und statt sechstausend
Namen den halben Buchdruck trainiert? Drei Dinge, ehrlich benannt: es wird nicht anders, es wird
größer; die Aufmerksamkeit ersetzt das feste Fenster, erklärt in zwei Sätzen und einem Bild;
und das Nachtrainieren auf menschliche Rückmeldung macht aus dem Fortsetzungsautomaten einen
Gesprächspartner.

Hier steht auch der Satz, der hängenbleiben soll: ein Sprachmodell schätzt die wahrscheinliche
Fortsetzung. Wahrscheinlich und wahr sind nicht dasselbe. Was wir Halluzination nennen, ist kein
Defekt, der wegrepariert wird, sondern dieselbe Eigenschaft, die das Ding brauchbar macht.

90 bis 95: Was das fürs Büro heißt. Wofür man es verwendet, wofür nicht, und wie man eine Angabe
prüft, ohne dem Ding zu glauben. Kurz, konkret, keine Moralpredigt.

95 bis 105: Kurztest.

105 bis 120: Hausübung, Fragen, Puffer. Ausblick: Buchstaben werden Wahrscheinlichkeiten,
Grundrisse werden Wahrscheinlichkeiten. Was macht man mit einem Bild?

## Was man sieht

**Drei Zerlegungen.** Derselbe Satz, drei Zeilen, farbig nach Token, mit der Länge der Folge und
der Größe des Vokabulars daneben.

**Der Balken der nächsten Buchstaben.** Nach "Gumpendorfer Stra" die Verteilung über alle
sechzig Zeichen, mit "ß" ganz oben. Beim Tippen aktualisiert sich das Bild: man schreibt in ein
Feld und sieht, was das Modell als nächstes erwartet.

**Die Lernkurve.** Kreuzentropie über die Schritte, daneben alle fünfhundert Schritte fünf
gezogene Namen. Am Anfang Buchstabensalat, nach zwei Minuten Wiener Straßennamen. Das ist das
Bild, das die Einheit trägt.

**Die Temperatur.** Regler von 0,2 bis 2,0, darunter zwanzig gezogene Namen, neu gezogen bei
jedem Rutsch.

**Aufmerksamkeit.** Ein Satz, darüber die Gewichte, mit denen ein Wort auf die anderen schaut.
Ein vorgerechnetes Bild aus einem kleinen fertigen Modell, zwei Minuten, kein eigener Code.

## Was zählt

Kurztest drei Punkte, Hausübung zehn Punkte, davon sechs auf die Interpretation. Aufgabe: das
Zeichenmodell auf einen selbst gewählten Wortschatz trainieren, zwanzig Namen bei drei
Temperaturen ziehen und abbilden. Dazu in fünf Sätzen: bei welcher Temperatur die Ausgaben
aufhören, brauchbar zu sein, und woran man das erkennt; und ein Beispiel aus dem eigenen
Studium, in dem ein Sprachmodell etwas Plausibles und Falsches gesagt hat, mit der Angabe, wie
man es hätte merken können.

## Offene Punkte

- Die Straßennamen müssen aus dem OGD-Portal gezogen und als Textdatei mitgeliefert werden.
- Zwei Minuten Training mal zwanzig Kernel gleichzeitig: vorher messen. Wenn der Hub das nicht
  trägt, wird das Modell vortrainiert mitgeliefert und in der Stunde nur nachtrainiert.
- Für die Aufmerksamkeitsabbildung ein kleines fertiges Modell suchen, das ohne Netzzugang läuft.
  Notfalls ein von Hand gezeichnetes Schema, dann aber als Schema benannt.
