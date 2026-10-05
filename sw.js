/* Demidov Scales service worker: keeps the app and its fonts available offline */
const CACHE = "demidov-shell-v1";
const SHELL = ["./", "./index.html", "./manifest.webmanifest", "./icon-192.png", "./icon-512.png", "./apple-touch-icon.png"];
self.addEventListener("install", e => { self.skipWaiting(); e.waitUntil(caches.open(CACHE).then(c => Promise.allSettled(SHELL.map(u => c.add(u))))); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  const req = e.request; if(req.method !== "GET") return;
  const u = new URL(req.url);
  if(u.searchParams.has("c")) return;                      /* update probes always go to the network */
  const isPage = req.mode === "navigate" || u.pathname.endsWith("/index.html") || u.pathname.endsWith("/");
  if(isPage){
    e.respondWith(fetch(req).then(r => { if(r.ok) caches.open(CACHE).then(c => c.put("./index.html", r.clone())); return r; })
      .catch(() => caches.match("./index.html")));
    return;
  }
  const own = u.origin === self.location.origin, font = /fonts\.(googleapis|gstatic)\.com$/.test(u.hostname);
  if(own || font){
    e.respondWith(caches.match(req).then(hit => {
      const net = fetch(req).then(r => { if(r.ok || r.type === "opaque") caches.open(CACHE).then(c => c.put(req, r.clone())); return r; }).catch(() => hit);
      return hit || net;
    }));
  }
});
