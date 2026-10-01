"""Site-wide header and reader sidebar, shared by every build.py and by index.html.

Every page gets the header (links to the bookshelf and each reader). Reader pages also
get a sidebar listing the reader's pages: fixed on the left on wide screens, a drawer
opened from the header's menu button on phones.

The site is also an installable web app that works offline: head() links the manifest and
icons, JS registers sw.js, and the bookshelf's "Save all readers for offline" button stores
every page in the service worker's cache. Opened online, the bookshelf counts new pages not
yet saved and removed pages still saved, so the reader knows when to press it again.

    python3 _shared/nav.py   # re-inserts the header, app links and save button into the bookshelf index.html
"""
import html, pathlib, re

SITE = pathlib.Path(__file__).resolve().parent.parent

# (slug, short label for the header, entry page inside the slug folder)
READERS = [
    ("easy-reads", "Easy Reads", "index.html"),
    ("1on1-architecture", "Architecture", "ch00.html"),
    ("1on1-api-types", "API & TypeScript", "ch00.html"),
    ("1on1-aws", "AWS", "ch00.html"),
    ("1on1-ai", "AI in Production", "ch00.html"),
    ("1on1-ops", "Operations", "ch00.html"),
    ("agentcore-reader", "AgentCore", "ch00.html"),
]
CUR = " aria-current=\"page\""

CSS = """
/* ---------- site header + reader sidebar (Site/_shared/nav.py) ---------- */
.site-head{position:sticky;top:0;z-index:30;margin:0 -16px;background:var(--bg);border-bottom:1px solid var(--line)}
.site-head .bar{display:flex;align-items:center;gap:8px 20px;min-height:52px;padding:0 16px;max-width:1280px;margin:0 auto}
.site-head .brand{font-weight:700;color:var(--text);text-decoration:none;white-space:nowrap}
.site-head .here{display:none;color:var(--text-muted);font-size:var(--fs-small);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.site-head .readers{display:flex;gap:4px 16px;flex-wrap:wrap;margin:0;padding:0;list-style:none;font-size:var(--fs-small)}
.site-head .readers a{color:var(--text-muted);text-decoration:none;display:inline-block;padding:4px 0}
.site-head .readers a:hover{color:var(--text)}
.site-head .readers a[aria-current]{color:var(--accent);font-weight:700;box-shadow:inset 0 -2px 0 var(--accent)}
.menu-btn{display:none;margin-left:auto;min-width:44px;min-height:44px;padding:0 12px;border:1px solid var(--line-strong);border-radius:var(--radius);
  background:var(--surface);color:var(--text);font:inherit;font-size:var(--fs-small);cursor:pointer}
.side{font-size:var(--fs-small);line-height:var(--lh-tight)}
.side h2{font-size:var(--fs-caption);text-transform:uppercase;letter-spacing:.06em;color:var(--text-subtle);margin:0 0 8px}
.side h2 a{color:inherit;text-decoration:none}
.side ol,.side ul{list-style:none;margin:0 0 24px;padding:0}
.side li a{display:flex;gap:10px;padding:7px 10px 7px 12px;border-left:2px solid var(--line);border-radius:0 var(--radius) var(--radius) 0;color:var(--text-muted);text-decoration:none}
.side li a:hover{background:var(--surface);color:var(--text)}
.side li a[aria-current]{border-left-color:var(--accent);color:var(--accent);font-weight:700}
.side .n{font-family:var(--font-mono);font-size:var(--fs-caption);color:var(--text-subtle);flex:none;min-width:1.6em;white-space:nowrap;padding-top:1px}
.side li a[aria-current] .n{color:var(--accent)}
.side .all{display:none}
@media (min-width:1080px){
  .has-side .page{margin-left:max(300px,calc((100% - var(--measure))/2))}
  .side{position:fixed;top:53px;bottom:0;left:0;width:272px;overflow-y:auto;padding:28px 16px 40px 20px;border-right:1px solid var(--line)}
}
@media (max-width:1079.98px){
  .has-side .menu-btn,.site-head.no-side-mobile .menu-btn{display:inline-flex;align-items:center}
  .site-head .readers{display:none}
  .has-side .site-head .here{display:block;margin-left:-12px}
  .side{position:fixed;inset:53px 0 0 0;z-index:25;overflow-y:auto;background:var(--bg);padding:20px 16px 48px;display:none}
  body.nav-open{overflow:hidden}
  body.nav-open .side{display:block}
  .side .all{display:block}
}
@media (max-width:1079.98px){body:not(.has-side) .site-head .readers{display:flex;overflow-x:auto;flex-wrap:nowrap;white-space:nowrap;scrollbar-width:none;padding-bottom:2px}
  body:not(.has-side) .site-head .bar{flex-wrap:wrap;padding-block:6px}}
.offline{display:grid;gap:6px;justify-items:start;margin:28px 0 0}
.offline[hidden]{display:none}
.save-btn{min-height:44px;padding:0 14px;border:1px solid var(--line-strong);border-radius:var(--radius);
  background:var(--surface);color:var(--text);font:inherit;font-size:var(--fs-small);cursor:pointer}
.save-btn:disabled{opacity:.6;cursor:progress}
.save-note{margin:0;font-size:var(--fs-caption);color:var(--text-muted);line-height:var(--lh-tight)}
"""

JS = """<script>
(function(){var b=document.querySelector(".menu-btn");if(!b)return;
function set(o){document.body.classList.toggle("nav-open",o);b.setAttribute("aria-expanded",o);b.textContent=o?"Close":"Menu"}
b.addEventListener("click",function(){set(!document.body.classList.contains("nav-open"))});
document.addEventListener("keydown",function(e){if(e.key==="Escape")set(false)});
var c=document.querySelector(".side [aria-current]");if(c&&c.scrollIntoView&&window.matchMedia("(min-width:1080px)").matches)c.scrollIntoView({block:"center"});
})();
(function(){var h=document.querySelector(".site-head");if(!h||!("serviceWorker" in navigator)||!window.caches)return;
var root=new URL(h.dataset.root||"./",location.href).href;
navigator.serviceWorker.register(root+"sw.js").catch(function(){});
var box=document.querySelector(".offline");if(!box)return;
var btn=box.querySelector(".save-btn"),note=box.querySelector(".save-note"),C="bookshelf-pages",K="bookshelf:saved";
function clean(u,base){u=new URL(u,base);return u.origin+u.pathname}
function pages(doc,base){return Array.prototype.map.call(doc.querySelectorAll(".side ol a"),function(a){return clean(a.getAttribute("href"),base)})}
function uniq(a){return a.filter(function(u,i){return a.indexOf(u)===i})}
function isPage(u){return u.indexOf(root)===0&&/\.html$/.test(u)}
async function urls(){var lists=await Promise.all(Array.prototype.map.call(h.querySelectorAll(".readers a"),async function(a){
    var u=clean(a.getAttribute("href"),location.href),r=await fetch(u,{cache:"no-cache"});if(!r.ok)throw new Error(u);
    return [u].concat(pages(new DOMParser().parseFromString(await r.text(),"text/html"),u))}));
  return uniq([].concat.apply([root+"index.html"],lists))}
async function diff(list){var c=await caches.open(C),keys=(await c.keys()).map(function(k){return k.url}).filter(isPage);
  return {c:c,missing:list.filter(function(u){return keys.indexOf(u)<0}),gone:keys.filter(function(u){return list.indexOf(u)<0})}}
async function save(list){var d=await diff(list),i=0,done=0;
  async function run(){while(i<list.length){var u=list[i++],r=await fetch(u,{cache:"no-cache"});if(!r.ok)throw new Error(u);await d.c.put(u,r);note.textContent="Saving "+(++done)+" of "+list.length+"\u2026"}}
  await Promise.all([run(),run(),run(),run()]);
  await Promise.all(d.gone.map(function(u){return d.c.delete(u)}));
  var f=document.querySelector('link[href*="fonts.googleapis.com/css"]');if(f)await fetch(f.href).catch(function(){})}
function last(){var t=localStorage.getItem(K);return t?"Last saved "+t+".":"Not saved on this device yet."}
async function show(){btn.textContent=localStorage.getItem(K)?"Update offline copy":"Save all readers for offline";
  if(!navigator.onLine){note.textContent="Offline. "+last();return}
  note.textContent=last();
  try{var list=await urls(),d=await diff(list),m=d.missing.length,g=d.gone.length;
    if(!localStorage.getItem(K))note.textContent="Not saved on this device yet ("+list.length+" pages).";
    else if(m||g)note.textContent=[m?m+" new page"+(m>1?"s":"")+" not saved":"",g?g+" removed page"+(g>1?"s":"")+" still saved":""].filter(Boolean).join(", ")+". Press the button to update.";
    else note.textContent="All "+list.length+" pages are saved. "+last()}catch(e){}}
btn.addEventListener("click",async function(){btn.disabled=true;
  try{if(navigator.storage&&navigator.storage.persist)navigator.storage.persist();
    await save(await urls());localStorage.setItem(K,new Date().toLocaleString([],{month:"short",day:"numeric",hour:"2-digit",minute:"2-digit"}));await show()}
  catch(e){note.textContent="Could not save. Check your connection and try again."}
  finally{btn.disabled=false}});
box.hidden=false;show();
})();
</script>"""


def head(root):
    """App links for <head>: manifest, home-screen icon and title."""
    return f"""<link rel="manifest" href="{root}manifest.webmanifest">
<link rel="apple-touch-icon" href="{root}icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-title" content="Bookshelf">
<meta name="mobile-web-app-capable" content="yes">"""


def offline_box():
    """Bookshelf button that saves every page of every reader, and removes pages the site no longer has."""
    return f"""<div class="offline" hidden>
  <button class="save-btn" type="button">Save all readers for offline</button>
  <p class="save-note" aria-live="polite"></p>
</div>"""


def header(root, current=None, with_side=False):
    """root: relative path from the page to Site/ ("" or "../" or "../../")."""
    links = "\n".join(
        f'    <li><a href="{root}{slug}/{entry}"{CUR if slug == current else ""}>{label}</a></li>'
        for slug, label, entry in READERS)
    here = next((f'<span class="here">/ {label}</span>' for slug, label, _ in READERS if slug == current), "") if with_side else ""
    btn = '\n  <button class="menu-btn" type="button" aria-controls="side" aria-expanded="false">Menu</button>' if with_side else ""
    return f"""<header class="site-head" data-root="{root}">
<div class="bar">
  <a class="brand" href="{root}index.html">Bookshelf</a>{here}
  <nav aria-label="Readers"><ul class="readers">
{links}
  </ul></nav>{btn}
</div>
</header>"""


def sidebar(title, home, items, current, root, reader_slug):
    """items: list of (href, number-or-empty, label). current: href of this page."""
    rows = "\n".join(
        f'    <li><a href="{h}"{CUR if h == current else ""}><span class="n">{n}</span><span>{html.escape(t)}</span></a></li>'
        for h, n, t in items)
    others = "\n".join(
        f'    <li><a href="{root}{slug}/{entry}"{CUR if slug == reader_slug else ""}><span>{label}</span></a></li>'
        for slug, label, entry in READERS)
    return f"""<aside class="side" id="side" aria-label="{html.escape(title)} pages">
  <h2><a href="{home}">{html.escape(title)}</a></h2>
  <ol>
{rows}
  </ol>
  <div class="all">
  <h2><a href="{root}index.html">All readers</a></h2>
  <ul>
{others}
  </ul>
  </div>
</aside>"""


def chapter_items(src_dir):
    """Sidebar items for a chNN reader, from each body's title comment ("Series 01 · Label")."""
    items = []
    for f in sorted(src_dir.glob("ch*.body.html")):
        title = re.match(r"<!--\s*title:\s*(.+?)\s*\|", f.read_text()).group(1)
        num = f.name[2:4]
        label = "Contents" if num == "00" else title.split(" · ", 1)[-1]
        items.append((f.name.replace(".body", ""), "" if num == "00" else num, label))
    return items


def patch_index():
    p = SITE / "index.html"
    s = p.read_text()
    s = re.sub(r"\n<style id=\"site-nav\">.*?</style>", "", s, flags=re.S)
    s = s.replace("</head>", f'<style id="site-nav">{CSS}</style>\n</head>', 1)
    s = re.sub(r"<!-- site-header -->.*?<!-- /site-header -->\n", "", s, flags=re.S)
    s = re.sub(r"<body>\n", f"<body>\n<!-- site-header -->\n{header('')}\n<!-- /site-header -->\n", s, count=1)
    s = re.sub(r"<!-- app -->.*?<!-- /app -->\n", "", s, flags=re.S)
    s = s.replace("</head>", f"<!-- app -->\n{head('')}\n<!-- /app -->\n</head>", 1)
    s = re.sub(r"<!-- offline -->.*?<!-- /offline -->\n", "", s, flags=re.S)
    s = re.sub(r"(<header class=\"page-head\">.*?</header>\n)", lambda m: f"{m.group(1)}<!-- offline -->\n{offline_box()}\n<!-- /offline -->\n", s, count=1, flags=re.S)
    s = re.sub(r"<!-- site-js -->.*?<!-- /site-js -->\n", "", s, flags=re.S)
    s = s.replace("</body>", f"<!-- site-js -->\n{JS}\n<!-- /site-js -->\n</body>", 1)
    p.write_text(s)
    print("patched index.html")


if __name__ == "__main__":
    patch_index()
