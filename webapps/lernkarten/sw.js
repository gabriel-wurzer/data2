// Alles offline verfügbar halten, damit die App in der U-Bahn läuft.
const CACHE = "lernkarten-v1";
const DATEIEN = ["./", "./index.html", "./fragen.json", "./manifest.webmanifest",
                 "./icon.svg", "./icon-192.png", "./icon-512.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(DATEIEN)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(namen => Promise.all(namen.filter(n => n !== CACHE).map(n => caches.delete(n))))
    .then(() => self.clients.claim()));
});

// Aus dem Cache, wenn vorhanden; sonst holen und für das nächste Mal behalten.
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(caches.match(e.request).then(treffer => treffer || fetch(e.request).then(antwort => {
    const kopie = antwort.clone();
    caches.open(CACHE).then(c => c.put(e.request, kopie)).catch(() => {});
    return antwort;
  }).catch(() => treffer)));
});
