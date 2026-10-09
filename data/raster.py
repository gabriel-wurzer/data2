"""Grundrisspolygone ausrichten und in ein 32x32-Raster legen.

Aus `gebaeude_wien.geojson` wird ein Stapel Schwarzweissbilder, einer je Gebaeude, plus eine
Tabelle mit Gebaeude-Nummer und Bauperiode in derselben Reihenfolge. Das ist der Eingang fuer
Einheit 4.

Ausgerichtet wird nach der Planung: Schwerpunkt aus der Flaeche, Hauptachse waagrecht,
gleichmaessig skaliert mit Rand, Hoefe bleiben Loecher. Zwei Fallen sind bewusst behandelt: bei
fast quadratischen Grundrissen ist die Hauptachse instabil, und ihre Richtung kann um 180 Grad
kippen. Deshalb wird die Richtung ueber das dritte Moment festgenagelt und die Instabilitaet
mitgeschrieben, statt sie zu verschweigen.

    uv run --with numpy python data/raster.py
"""
import json
from pathlib import Path

import numpy as np

HIER = Path(__file__).resolve().parent
GEOJSON = HIER / "gebaeude_wien.geojson"
BILDER = HIER / "grundrisse.npy"
TABELLE = HIER / "grundrisse.csv"
N = 32
RAND = 0.12                      # Anteil des Bildes, der ringsum frei bleibt


def ringe(geometrie):
    """Alle Ringe eines Polygons oder Multipolygons, aussen zuerst."""
    art, koord = geometrie["type"], geometrie["coordinates"]
    teile = [koord] if art == "Polygon" else koord
    for teil in teile:
        yield [np.asarray(r, dtype=float)[:, :2] for r in teil]


def meter(ring, lat0, ursprung):
    """Grad in Meter, lokal linearisiert. Fuer ein Haus genau genug. Alle Ringe eines Polygons
    brauchen denselben Ursprung, sonst rutschen die Hoefe aus dem Haus."""
    x = (ring[:, 0] - ursprung[0]) * 111320.0 * np.cos(np.deg2rad(lat0))
    y = (ring[:, 1] - ursprung[1]) * 110540.0
    return np.column_stack([x, y])


def flaeche_und_schwerpunkt(ring):
    """Shoelace. Vorzeichenbehaftet, damit Hoefe sich von selbst abziehen."""
    x, y = ring[:, 0], ring[:, 1]
    x1, y1 = np.roll(x, -1), np.roll(y, -1)
    kreuz = x * y1 - x1 * y
    a = float(kreuz.sum()) / 2.0
    if abs(a) < 1e-12:
        return 0.0, np.array([x.mean(), y.mean()])
    cx = float(((x + x1) * kreuz).sum()) / (6.0 * a)
    cy = float(((y + y1) * kreuz).sum()) / (6.0 * a)
    return a, np.array([cx, cy])


def dichte_punkte(ringe_m, anzahl=4000, samen=0):
    """Punkte gleichverteilt im Polygon, fuer Momente und Hauptachse."""
    alle = np.vstack(ringe_m)
    lo, hi = alle.min(axis=0), alle.max(axis=0)
    r = np.random.default_rng(samen)
    kandidaten = r.uniform(lo, hi, size=(anzahl * 4, 2))
    drin = im_polygon(kandidaten, ringe_m)
    return kandidaten[drin][:anzahl]


def im_polygon(punkte, ringe_m):
    """Even-odd-Regel, vektorisiert. Innenringe zaehlen mit und schneiden Hoefe aus."""
    drin = np.zeros(len(punkte), dtype=bool)
    px, py = punkte[:, 0], punkte[:, 1]
    for ring in ringe_m:
        x, y = ring[:, 0], ring[:, 1]
        x1, y1 = np.roll(x, -1), np.roll(y, -1)
        for a_x, a_y, b_x, b_y in zip(x, y, x1, y1):
            if a_y == b_y:
                continue
            trifft = (a_y > py) != (b_y > py)
            with np.errstate(divide="ignore", invalid="ignore"):
                schnitt = (b_x - a_x) * (py - a_y) / (b_y - a_y) + a_x
            drin ^= trifft & (px < schnitt)
    return drin


def ausrichten(ringe_m):
    """Schwerpunkt in den Ursprung, Hauptachse waagrecht, Richtung eindeutig."""
    wolke = dichte_punkte(ringe_m)
    if len(wolke) < 50:
        return None, None
    mitte = wolke.mean(axis=0)
    zentriert = wolke - mitte
    kovarianz = np.cov(zentriert.T)
    werte, vektoren = np.linalg.eigh(kovarianz)
    haupt = vektoren[:, np.argmax(werte)]
    winkel = float(np.arctan2(haupt[1], haupt[0]))
    dreh = np.array([[np.cos(-winkel), -np.sin(-winkel)],
                     [np.sin(-winkel), np.cos(-winkel)]])
    gedreht = zentriert @ dreh.T
    # Richtung festnageln: die Seite mit der groesseren Masse kommt nach rechts.
    if float(np.mean(gedreht[:, 0] ** 3)) < 0:
        dreh = -dreh
    # Wie sicher ist die Hauptachse ueberhaupt? 1 heisst rund, 0 heisst schlank.
    rundheit = float(min(werte) / max(werte)) if max(werte) > 0 else 1.0
    return dreh, (mitte, rundheit)


def rastere(ringe_m, dreh, mitte):
    """Polygon in ein N x N Bild, gleichmaessig skaliert, mit Rand."""
    verschoben = [(r - mitte) @ dreh.T for r in ringe_m]
    alle = np.vstack(verschoben)
    halb = float(np.abs(alle).max())
    if halb <= 0:
        return None
    mass = (N / 2.0) * (1.0 - RAND) / halb
    skaliert = [r * mass for r in verschoben]

    achse = np.arange(N) - (N - 1) / 2.0
    gx, gy = np.meshgrid(achse, achse)
    gitter = np.column_stack([gx.ravel(), gy.ravel()])
    bild = im_polygon(gitter, skaliert).reshape(N, N).astype(np.float32)
    return bild[::-1]            # y nach oben, damit die Bilder aufrecht stehen


def tabelle_lesen():
    """Die Kennwerte aus gebaeude_wien.csv, nach Gebaeude-Nummer. Das GeoJSON hat nur id
    und Bauperiode, alles andere steht in der Tabelle."""
    zeilen = (HIER / "gebaeude_wien.csv").read_text(encoding="utf-8").strip().splitlines()
    kopf = zeilen[0].split(",")
    nach = {}
    for zeile in zeilen[1:]:
        werte = dict(zip(kopf, zeile.split(",")))
        nach[werte["id"]] = werte
    return nach


def main():
    daten = json.loads(GEOJSON.read_text(encoding="utf-8"))
    kennwerte = tabelle_lesen()
    bilder, zeilen, verworfen = [], [], 0
    for merkmal in daten["features"]:
        eigenschaften = merkmal["properties"]
        geometrie = merkmal["geometry"]
        lat0 = float(np.asarray(next(ringe(geometrie))[0])[:, 1].mean())
        teile = [[meter(r, lat0, gruppe[0][0]) for r in gruppe] for gruppe in ringe(geometrie)]
        # groesster Teil gewinnt; mehrteilige Bauwerke werden nicht zusammengefasst
        teile.sort(key=lambda g: abs(flaeche_und_schwerpunkt(g[0])[0]), reverse=True)
        ringe_m = teile[0]

        dreh, zusatz = ausrichten(ringe_m)
        if dreh is None:
            verworfen += 1
            continue
        mitte, rundheit = zusatz
        bild = rastere(ringe_m, dreh, mitte)
        if bild is None or bild.sum() < 20:      # zu wenig gefuellt, unbrauchbar
            verworfen += 1
            continue
        k = kennwerte.get(str(eigenschaften.get("id")), {})
        bilder.append(bild)
        zeilen.append((eigenschaften.get("id"), eigenschaften.get("bauperiode"),
                       k.get("startjahr", ""), k.get("flaeche_m2", ""),
                       k.get("kompaktheit", ""), round(rundheit, 4),
                       round(float(bild.mean()), 4)))

    stapel = np.stack(bilder).astype(np.float32)
    np.save(BILDER, stapel)
    kopf = "id,bauperiode,startjahr,flaeche_m2,kompaktheit,rundheit,fuellgrad\n"
    TABELLE.write_text(kopf + "\n".join(",".join(str(v) for v in z) for z in zeilen) + "\n",
                       encoding="utf-8")
    print(f"{len(stapel)} grundrisse gerastert, {verworfen} verworfen")
    print(f"fuellgrad im mittel {stapel.mean():.3f}, "
          f"fast quadratisch (rundheit > 0.8): {sum(z[5] > 0.8 for z in zeilen)}")


if __name__ == "__main__":
    main()
