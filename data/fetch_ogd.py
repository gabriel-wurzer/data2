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

# Angenommener Wand-U-Wert je Bauperiode des Layers. Das sind Lehrwerte in der
# Größenordnung der österreichischen Gebäudetypologie, keine erhobenen Kennwerte: die
# Kategorie "Nach 1976" umfasst alles vom Plattenbau bis zum Passivhaus, ein einzelner Wert
# kann das nicht abbilden. Wer es genauer braucht, ersetzt die Tabelle durch gemessene Werte.
U_JE_PERIODE = {
    "Vor 1683": 1.50, "1683-1740": 1.50, "1741-1780": 1.50, "1781-1848": 1.50,
    "1849-1859": 1.50, "1860-1883": 1.50, "1884-1918": 1.45, "1919-1945": 1.40,
    "1946-1976": 1.30, "Nach 1976": 0.70,
}

# Meter pro Grad: Breitengrad bei 48 Grad Nord, Längengrad zusätzlich mit cos(lat) verkürzt.
M_PRO_GRAD_LAT = 111200.0
M_PRO_GRAD_LON = 111320.0


def meter(ring, lat0, lon0):
    """Grad in Meter, lokal um den Schwerpunkt linearisiert und dorthin verschoben."""
    mx = M_PRO_GRAD_LON * math.cos(math.radians(lat0))
    return [((x - lon0) * mx, (y - lat0) * M_PRO_GRAD_LAT) for x, y in ring]


def flaeche_umfang(ring):
    a = 0.0
    u = 0.0
    for i in range(len(ring) - 1):
        x1, y1 = ring[i]
        x2, y2 = ring[i + 1]
        a += x1 * y2 - x2 * y1
        u += math.hypot(x2 - x1, y2 - y1)
    return abs(a) / 2, u


def polygon_masse(poly, lat0, lon0):
    """Außenring minus Höfe. Der Hofumfang zählt mit, er ist Außenwand."""
    flaeche, umfang = 0.0, 0.0
    for i, ring in enumerate(poly):
        if len(ring) < 4:
            continue
        a, u = flaeche_umfang(meter(ring, lat0, lon0))
        flaeche += a if i == 0 else -a
        umfang += u
    return flaeche, umfang


def startjahr(periode):
    """Erste Jahreszahl der Periode, nur zum Sortieren und Einfärben."""
    ziffern = "".join(c if c.isdigit() else " " for c in periode).split()
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
    gesehen = set()
    for f in features:
        p = f["properties"]
        geom = f["geometry"]
        if not geom or geom["type"] not in ("Polygon", "MultiPolygon"):
            continue
        if p["OBJECTID"] in gesehen:    # die Ausschnitte überlappen einander
            continue
        teile = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
        aussen = teile[0][0]
        if len(aussen) < 4:
            continue
        lat0 = sum(pt[1] for pt in aussen) / len(aussen)
        lon0 = sum(pt[0] for pt in aussen) / len(aussen)

        a = u = 0.0
        for poly in teile:              # jeder Teil des Bauwerks zählt mit
            pa, pu = polygon_masse(poly, lat0, lon0)
            a += pa
            u += pu
        if a < 40:                      # Schuppen und Splitter raus
            continue

        periode = p.get("OBJ_STR_TXT")
        if periode not in U_JE_PERIODE:
            continue
        uw = U_JE_PERIODE[periode]
        kompakt = u / math.sqrt(a)      # dimensionslos, Kreis liegt bei 3.5, Zeile weit darüber
        if kompakt > 12:                # zerfranste Splitterpolygone raus
            continue
        # Die Rechenvorschrift. Sie ist die Zielgröße des Kurses, keine Messung.
        hwb = 18 + 62 * uw + 9 * kompakt
        gesehen.add(p["OBJECTID"])
        zeilen.append({
            "id": p["OBJECTID"],
            "bauperiode": periode,
            "startjahr": startjahr(periode),
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
