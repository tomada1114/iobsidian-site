/* Bookshelf service worker (Site/sw.js). Scope: the whole site.
   Pages: network first, falling back to the saved copy after 3 s or when offline.
   Every page fetched online is saved; the Save buttons (_shared/nav.py) save whole readers.
   Google Fonts: saved on first use, then served from the cache. */
const PAGES = "bookshelf-pages", FONTS = "bookshelf-fonts", WAIT_MS = 3000;

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", e => e.waitUntil(self.clients.claim()));

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin === location.origin) e.respondWith(networkFirst(e, url));
  else if (url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com") e.respondWith(cacheFirst(req));
});

async function networkFirst(e, url) {
  const cache = await caches.open(PAGES);
  const key = url.origin + url.pathname;
  const net = fetch(e.request).then(res => {
    if (res.ok && res.type === "basic") cache.put(key, res.clone());
    return res;
  });
  e.waitUntil(net.catch(() => {}));
  try {
    return await Promise.race([net, new Promise((_, no) => setTimeout(no, WAIT_MS))]);
  } catch {
    const saved = await cache.match(key);
    if (saved) return saved;
    try { return await net; } catch { return e.request.mode === "navigate" ? offlinePage() : Response.error(); }
  }
}

async function cacheFirst(req) {
  const cache = await caches.open(FONTS);
  const saved = await cache.match(req.url);
  if (saved) return saved;
  try {
    const res = await fetch(req);
    if (res.ok || res.type === "opaque") cache.put(req.url, res.clone());
    return res;
  } catch { return Response.error(); }
}

function offlinePage() {
  const home = self.registration.scope + "index.html";
  return new Response(`<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light dark">
<title>Offline</title><style>body{font-family:system-ui,sans-serif;max-width:32rem;margin:15vh auto;padding:0 20px;line-height:1.6}</style></head>
<body><h1>You are offline</h1><p>This page is not saved on this device yet. Open it once while online, or use “Save for offline” on its reader.</p>
<p><a href="${home}">Back to the bookshelf</a></p></body></html>`, { status: 503, headers: { "Content-Type": "text/html; charset=utf-8" } });
}
