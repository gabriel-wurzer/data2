# data2

Notebooks, Daten und interaktive Web-Apps für datengetriebenes Entwerfen.

- `notebooks/` — Jupyter-Notebooks, Analyse und Modelle
- `data/` — Datensätze, roh und aufbereitet
- `webapps/` — eigenständige three.js- und CesiumJS-Anwendungen, aus den Notebooks
  aufrufbar und einzeln im Browser lauffähig

Eine Web-App ist ein Ordner unter `webapps/` mit eigener `index.html`. Die Notebooks rufen
sie über einen lokalen Server auf und übergeben Daten per Query-Parameter oder als Datei in
`data/`.
