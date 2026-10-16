// The old flashcards lived here. This worker replaces the old one, deletes its caches and removes itself.
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", e => {
  e.waitUntil((async () => {
    const names = await caches.keys();
    await Promise.all(names.filter(n => n.startsWith("lernkarten")).map(n => caches.delete(n)));
    const target = new URL("../flashcards/", self.registration.scope).href;
    await self.registration.unregister();
    for (const c of await self.clients.matchAll()) c.navigate(target);
  })());
});
