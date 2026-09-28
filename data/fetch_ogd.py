"""Holt Gebäude aus den offenen Daten der Stadt Wien und legt sie als CSV ab.

Quelle: WFS der Stadt Wien, Layer ogdwien:GEBAEUDETYPOGD (Gebäudetypen, 439.156 Polygone,
je mit Bauperiode und Bautyp). Lizenz CC BY 4.0, Stadt Wien, data.wien.gv.at.

Aus dem Polygon werden Grundfläche und Umfang gerechnet, daraus ein Kompaktheitsmaß. Die
Bauperiode liefert über eine Tabelle den typischen Wand-U-Wert. Der Heizwärmebedarf ist
KEINE Messung: er kommt aus der Formel unten und ist damit genau das, was die Studierenden
im Kurs nachbauen. Wer später gemessene Werte hat, ersetzt hier die Zielgröße.

    python fetch_ogd.py
"""
import csv
import json
import math
import urllib.request
from pathlib import Path

WFS = "https://data.wien.gv.at/daten/geo"
LAYER = "ogdwien:GEBAEUDETYPOGD"
# Vier Ausschnitte, damit nicht nur Gründerzeit im Datensatz steht: Innenstadt bis Gürtel,
# Sonnwendviertel, Floridsdorf und die Seestadt. lon/lat, so will es der Dienst.
BBOXEN = [
    (16.330, 48.185, 16.390, 48.215),
    (16.360, 48.170, 16.400, 48.190),
    (16.380, 48.250, 16.430, 48.280),
    (16.480, 48.215, 16.540, 48.245),
]
MAX = 2500
OUT = Path(__file__).with_name("gebaeude_wien.csv")

# Wand-U-Wert nach Bauperiode, gerundet nach österreichischer Gebäudetypologie (TABULA).
U_NACH_JAHR = [(1919, 1.50), (1945, 1.40), (1960, 1.30), (1980, 1.20),
               (1990, 0.80), (2000, 0.60), (2010, 0.40), (9999, 0.25)]


def u_wert(startjahr):
    for grenze, u in U_NACH_JAHR:
        if startjahr < grenze:
            return u
    return U_NACH_JAHR[-1][1]


def meter(ring, lat0):
    """Grad in Meter, lokal um lat0 linearisiert. Genau genug für Flächen dieser Größe."""
    mx = 111320 * math.cos(math.radians(lat0))
    return [(x * mx, y * 110540) for x, y in ring]


def flaeche_umfang(ring):
    a = 0.0
    u = 0.0
    for i in range(len(ring) - 1):
        x1, y1 = ring[i]
        x2, y2 = ring[i + 1]
        a += x1 * y2 - x2 * y1
        u += math.hypot(x2 - x1, y2 - y1)
    return abs(a) / 2, u


def startjahr(text):
    if not text:
        return None
    ziffern = "".join(c if c.isdigit() else " " for c in text).split()
    return int(ziffern[0]) if ziffern else None


def hole(bbox):
    url = (f"{WFS}?service=WFS&request=GetFeature&version=1.1.0&typeName={LAYER}"
           f"&srsName=EPSG:4326&outputFormat=json&maxFeatures={MAX}"
           f"&bbox={bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]},EPSG:4326")
    with urllib.request.urlopen(url, timeout=180) as r:
        return json.load(r)


def main():
    features = []
    for bbox in BBOXEN:
        teil = hole(bbox)["features"]
        print(f"bbox {bbox[0]}/{bbox[1]}: {len(teil)} Objekte")
        features += teil

    zeilen = []
    for f in features:
        p = f["properties"]
        geom = f["geometry"]
        if not geom or geom["type"] not in ("Polygon", "MultiPolygon"):
            continue
        ring = geom["coordinates"][0] if geom["type"] == "Polygon" else geom["coordinates"][0][0]
        if len(ring) < 4:
            continue
        lat0 = sum(pt[1] for pt in ring) / len(ring)
        lon0 = sum(pt[0] for pt in ring) / len(ring)
        a, u = flaeche_umfang(meter(ring, lat0))
        if a < 40:                      # Schuppen und Splitter raus
            continue
        jahr = startjahr(p.get("OBJ_STR_TXT"))
        if jahr is None:
            continue
        uw = u_wert(jahr)
        kompakt = u / math.sqrt(a)      # dimensionslos, Kreis liegt bei 3.5, Zeile weit darüber
        if kompakt > 12:                # zerfranste Splitterpolygone raus
            continue
        # Die Rechenvorschrift. Sie ist die Zielgröße des Kurses, keine Messung.
        hwb = 18 + 62 * uw + 9 * kompakt
        zeilen.append({
            "id": p["OBJECTID"],
            "bauperiode": p.get("OBJ_STR_TXT"),
            "startjahr": jahr,
            "bautyp": (p.get("BAUTYP_TXT") or "").split("-")[0],
            "flaeche_m2": round(a, 1),
            "umfang_m": round(u, 1),
            "kompaktheit": round(kompakt, 3),
            "u_wert": uw,
            "hwb": round(hwb, 2),
            "lat": round(lat0, 6),
            "lon": round(lon0, 6),
        })

    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(zeilen[0].keys()))
        w.writeheader()
        w.writerows(zeilen)
    print(f"{len(zeilen)} Gebäude in {OUT.name}")


if __name__ == "__main__":
    main()
