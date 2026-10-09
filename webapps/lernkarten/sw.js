// Die Hülle vorab, die Kartenbilder erst wenn die Karte drankommt. Zwei Megabyte je Karte
// will niemand im Voraus laden.
const CACHE = "lernkarten-v4";
const DATEIEN = ["./", "./index.html", "./fragen.json", "./manifest.json",
                 "./icon.svg", "./icon-192.png", "./icon-512.png"];

// Karten und Hülle: erst das Netz, damit eine geänderte Karte sofort ankommt und nicht erst,
// wenn jemand die Cache-Version hochzählt. Bilder: erst der Cache, die ändern sich nicht.
const FRISCH = [/fragen\.json$/, /index\.html$/, /\/$/];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(DATEIEN)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(namen => Promise.all(namen.filter(n => n !== CACHE).map(n => caches.delete(n))))
    .then(() => self.clients.claim()));
});

self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  const zuerstNetz = FRISCH.some(r => r.test(new URL(e.request.url).pathname));

  e.respondWith((async () => {
    const speicher = await caches.open(CACHE);
    // Nur Erfolge behalten. Ein gecachter 404 bleibt sonst für immer ein 404, auch wenn die
    // Datei längst auf dem Server liegt.
    const behalte = (antwort) => {
      if (antwort.ok) speicher.put(e.request, antwort.clone());
      return antwort;
    };
    if (zuerstNetz) {
      try {
        return behalte(await fetch(e.request));
      } catch (nichts) {
        const treffer = await speicher.match(e.request);
        if (treffer) return treffer;
        throw nichts;
      }
    }
    const treffer = await speicher.match(e.request);
    if (treffer) return treffer;
    return behalte(await fetch(e.request));
  })());
});
