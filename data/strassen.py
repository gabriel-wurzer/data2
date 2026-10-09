"""Die Strassennamen von Wien holen, fuer das Zeichenmodell in Einheit 6.

Quelle: Strassengraph der Stadt Wien (WFS, Layer `ogdwien:STRASSENGRAPHOGD`). Der Graph hat
eine Kante je Strassenabschnitt, also kommt jeder Name vielfach vor; gespeichert wird die
eindeutige Liste.

    uv run python data/strassen.py
"""
import json
import urllib.parse
import urllib.request
from pathlib import Path

HIER = Path(__file__).resolve().parent
ZIEL = HIER / "strassennamen.txt"
WFS = "https://data.wien.gv.at/daten/geo"
KOPF = {"User-Agent": "aiape-kurs/1.0 (lehre, TU Wien)"}


def hole(start, anzahl=10000):
    frage = urllib.parse.urlencode({
        "service": "WFS", "request": "GetFeature", "version": "2.0.0",
        "typeNames": "ogdwien:STRASSENGRAPHOGD", "outputFormat": "json",
        "propertyName": "FEATURENAME", "count": str(anzahl), "startIndex": str(start)})
    req = urllib.request.Request(f"{WFS}?{frage}", headers=KOPF)
    with urllib.request.urlopen(req, timeout=300) as antwort:
        return json.load(antwort)


def main():
    namen, start = set(), 0
    while True:
        daten = hole(start)
        merkmale = daten.get("features", [])
        if not merkmale:
            break
        for m in merkmale:
            name = (m["properties"] or {}).get("FEATURENAME")
            if name:
                namen.add(name.strip())
        start += len(merkmale)
        print(f"{start} kanten, {len(namen)} namen")
        if len(merkmale) < 10000:
            break

    sortiert = sorted(namen)
    ZIEL.write_text("\n".join(sortiert) + "\n", encoding="utf-8")
    print(f"{len(sortiert)} strassennamen in {ZIEL.name}")
    print("beispiele:", ", ".join(sortiert[:5]))


if __name__ == "__main__":
    main()
