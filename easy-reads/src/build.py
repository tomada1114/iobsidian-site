"""Build Easy Reads: one page per src/reads/<id>.body.html into ../p/<id>.html, plus ../index.html.
Each body starts with: <!-- title: ... | topic: <topic> | blurb: ... -->
The page head matches reading-page-designing/assets/page-template.html; base.css is a copy of that skill's."""
import re, math, html, datetime, pathlib
here = pathlib.Path(__file__).parent
root = here.parent
css = (here/"base.css").read_text()
LANG = "en"
SERIES = "Easy Reads"
WPM = 120  # a comfortable pace for a learner reading easy English
TOPICS = {  # topic -> (label, page accent 1-4)
    "tech": ("Technology", 1), "work": ("Work", 1), "language": ("Language", 1),
    "science": ("Science", 2), "nature": ("Nature", 2), "space": ("Space", 2), "health": ("Health", 2),
    "history": ("History", 3), "people": ("People", 3), "culture": ("Culture", 3), "food": ("Food", 3), "story": ("Story", 3),
    "life": ("Life in the US", 4), "money": ("Money", 4), "mind": ("Mind", 4), "sports": ("Sports", 4), "art": ("Art", 4),
}
HEADER = re.compile(r"<!--\s*title:\s*(.+?)\s*\|\s*topic:\s*(\w+)\s*\|\s*blurb:\s*(.+?)\s*-->\n", re.S)
READ_JS = """<script>
(function(){var K="easy-reads:read",s;try{s=JSON.parse(localStorage.getItem(K)||"[]")}catch(e){s=[]}
%s})();
</script>"""
MARK_JS = READ_JS % """var id=document.body.dataset.id;function mark(){if(s.indexOf(id)<0){s.push(id);try{localStorage.setItem(K,JSON.stringify(s))}catch(e){}}}
var p=document.querySelector(".pager");if(p&&"IntersectionObserver" in window){new IntersectionObserver(function(e,o){if(e[0].isIntersecting){mark();o.disconnect()}}).observe(p)}else{mark()}"""
SHOW_JS = READ_JS % """document.querySelectorAll("dd[data-id]").forEach(function(d){if(s.indexOf(d.dataset.id)>=0){var t=document.createElement("span");t.className="tag";t.textContent="read";d.prepend(t)}});"""

def page(title, acc, body, data_id=""):
    attr = f' data-id="{data_id}"' if data_id else ""
    return f"""<!doctype html>
<html lang="{LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#131615" media="(prefers-color-scheme: dark)">
<meta name="robots" content="noindex">
<title>{html.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=BIZ+UDPGothic:wght@400;700&family=JetBrains+Mono:wght@500&display=swap">
<style>
{css}</style>
</head>
<body{attr}>
<div class="page acc-{acc}">
{body.rstrip()}
</div>
</body>
</html>
"""

def reading_words(body):
    """Words the reader reads as the article: the word list and the asides are left out."""
    t = re.sub(r'<section class="words".*?</section>|<div class="aside.*?</div>', " ", body, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return len(re.findall(r"[A-Za-z][A-Za-z'’-]*", t))

def when(read_id):
    d = datetime.date(int(read_id[:4]), int(read_id[4:6]), int(read_id[6:8]))
    return d, d.strftime("%a, %b ") + str(d.day) + d.strftime(", %Y")

reads = []
for f in sorted((here/"reads").glob("*.body.html")):
    src = f.read_text()
    m = HEADER.match(src)
    if not m: raise SystemExit(f"{f.name}: missing header comment")
    title, topic, blurb = m.groups()
    if topic not in TOPICS: raise SystemExit(f"{f.name}: unknown topic {topic!r} (one of {', '.join(TOPICS)})")
    body = src[m.end():]
    rid = f.name.removesuffix(".body.html")
    n = reading_words(body)
    reads.append(dict(id=rid, title=title, topic=topic, blurb=blurb, body=body, words=n, mins=max(1, math.ceil(n/WPM))))

for i, r in enumerate(reads):
    label, acc = TOPICS[r["topic"]]
    _, day = when(r["id"])
    prev_ = reads[i-1] if i > 0 else None
    next_ = reads[i+1] if i+1 < len(reads) else None
    pager = '<nav class="pager" aria-label="More reads">\n'
    pager += f'  <a class="prev" href="{prev_["id"]}.html"><span>Previous</span><b>{prev_["title"]}</b></a>\n' if prev_ else '  <a class="prev" href="../index.html"><span>Back to</span><b>All reads</b></a>\n'
    pager += f'  <a class="next" href="{next_["id"]}.html"><span>Next</span><b>{next_["title"]}</b></a>\n' if next_ else '  <a class="next" href="../index.html"><span>Back to</span><b>All reads</b></a>\n'
    pager += "</nav>"
    body = f"""<header class="page-head">
  <p class="kicker"><a href="../index.html"><b>{SERIES}</b></a><span>{day}</span></p>
  <h1>{r["title"]}</h1>
  <p class="lead">{r["blurb"]}</p>
  <p class="meta"><span>{label}</span><span>{r["words"]} words</span><span>About {r["mins"]} min</span></p>
</header>

<div class="flow">
{r["body"].strip()}

{pager}
  <p class="fine"><a href="../index.html">All reads</a></p>
</div>
{MARK_JS}"""
    (root/"p").mkdir(exist_ok=True)
    (root/"p"/f'{r["id"]}.html').write_text(page(f'{r["title"]} | {SERIES}', acc, body, r["id"]))

days = {}
for r in reversed(reads):
    days.setdefault(r["id"][:8], []).append(r)
secs = []
for key, items in days.items():
    _, day = when(key)
    rows = "\n".join(
        f'      <dt><a href="p/{r["id"]}.html">{r["title"]}</a></dt>\n'
        f'      <dd data-id="{r["id"]}">{TOPICS[r["topic"]][0]} · {r["words"]} words · {r["blurb"]}</dd>'
        for r in sorted(items, key=lambda r: r["id"]))
    secs.append(f"""  <section aria-labelledby="d{key}">
    <h2 id="d{key}">{day}</h2>
    <dl class="terms">
{rows}
    </dl>
  </section>""")
total = sum(r["words"] for r in reads)
index = f"""<header class="page-head">
  <p class="kicker"><a href="../index.html"><b>Bookshelf</b></a><span>Updated every morning</span></p>
  <h1>Easy Reads</h1>
  <p class="lead">Short and easy English reads on many topics. Pick the ones you like. Read a lot, read fast, and do not stop for every word.</p>
  <p class="meta"><span>{len(reads)} reads</span><span>{total:,} words</span><span>Level A2+ to B1</span></p>
</header>

<div class="flow">
{chr(10).join(secs) if secs else "  <p>No reads yet.</p>"}
</div>
{SHOW_JS}"""
(root/"index.html").write_text(page(SERIES, 1, index))
print(f"built {len(reads)} reads + index.html")
