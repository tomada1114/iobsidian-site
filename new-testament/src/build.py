"""Assemble chapter bodies into standalone HTML pages.
Each src/chNN.body.html starts with a line: <!-- title: ... | accent: think -->
The page head matches reading-page-designing/assets/page-template.html; base.css is a copy of that skill's."""
import re, sys, pathlib
here = pathlib.Path(__file__).parent
sys.path.insert(0, str(here.parent.parent/"_shared"))
import nav
css = (here/"base.css").read_text() + nav.CSS
LANG = "ja"
ACCENT = {"think": "1", "reach": "2", "run": "3", "guard": "4"}
head = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#131615" media="(prefers-color-scheme: dark)">
<meta name="robots" content="noindex">
{app}
<title>{title}</title>
<link rel="canonical" href="{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=BIZ+UDGothic:wght@400;700&family=BIZ+UDPGothic:wght@400;700&family=JetBrains+Mono:wght@500&display=swap">
<style>
{css}</style>
</head>
<body class="has-side acc-{acc}">
{header}
{side}
<div class="page acc-{acc}">
<svg class="svg-defs" width="0" height="0" aria-hidden="true" focusable="false" style="position:absolute">
  <defs>
    <marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker>
    <marker id="arw-acc" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah-acc"/></marker>
  </defs>
</svg>
"""

def book_list():
    """Render the 27-book catalogue, linking only to books with built sources."""
    import html, json
    books = json.loads((here / "books.json").read_text())
    if len(books) != 27 or len({b["slug"] for b in books}) != 27:
        raise SystemExit("books.json must contain 27 distinct books")
    groups = {"gospels": "福音書 — イエスの活動、死、復活", "acts": "使徒言行録 — 初期の共同体と宣教", "letters": "書簡 — 共同体や個人への教え", "revelation": "黙示録 — 幻と象徴による希望と裁き"}
    if any(b["group"] not in groups or not re.fullmatch(r"[a-z0-9-]+", b["slug"]) for b in books):
        raise SystemExit("Invalid book group or slug")
    rows = []
    for group, label in groups.items():
        rows.append("<h3>" + html.escape(label) + "</h3><ul>")
        for book in (b for b in books if b["group"] == group):
            sources = here.parent / book["slug"] / "src"
            chapters = sorted(p for p in sources.glob("ch[0-9][0-9].body.html") if p.name != "ch00.body.html")
            title = html.escape(book["title"])
            if chapters:
                if not (sources / "ch00.body.html").exists():
                    raise SystemExit(f"{book['slug']}: contents source missing")
                entry = f"<a href=\"{book['slug']}/ch00.html\">{title} — {len(chapters)}章を収録</a>"
            else:
                entry = title + " — 未収録"
            rows.append("<li>" + entry + "</li>")
        rows.append("</ul>")
    return "\n".join(rows)


def redirect(path, target):
    """Keep previously published links usable without duplicating reader bodies."""
    import html, json
    canonical = "https://tomada1114.github.io/iobsidian-site/" + str((path.parent / target).resolve().relative_to(nav.SITE.resolve()))
    if canonical.endswith("/new-testament"):
        canonical += "/"
    out = '<!doctype html>\n<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light dark"><meta name="robots" content="noindex">'
    out += '<title>新約聖書 — 新しい場所へ</title><link rel="canonical" href="' + html.escape(canonical, quote=True) + '">'
    out += '<meta http-equiv="refresh" content="0; url=' + html.escape(target, quote=True) + '"><style>' + (here / "base.css").read_text() + '</style></head><body><main class="page acc-1"><h1>新しい場所へ移動します</h1><p><a href="' + html.escape(target, quote=True) + '">新約聖書を読む</a></p></main>'
    out += '<script>location.replace(' + json.dumps(target) + '+location.search+location.hash);</script></body></html>\n'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(out)

items = [("./" if href == "ch00.html" else href, num, label) for href, num, label in nav.chapter_items(here)]
series = re.match(r"<!--\s*title:\s*(.+?)\s*·", (here/"ch00.body.html").read_text()).group(1)
slug = here.parent.name
for f in sorted(here.glob("*.body.html")):
    src = f.read_text()
    m = re.match(r"<!--\s*title:\s*(.+?)\s*\|\s*accent:\s*(\w+)\s*-->\n", src)
    if not m: raise SystemExit(f"{f.name}: missing header comment")
    title, acc = m.groups()
    body = src[m.end():].replace("<!-- book-list -->", book_list())
    filename = "index.html" if f.name == "ch00.body.html" else f.name.replace(".body", "")
    canonical = "https://tomada1114.github.io/iobsidian-site/new-testament/" + ("" if filename == "index.html" else filename)
    out = head.format(lang=LANG, canonical=canonical, app=nav.head("../"), title=title, css=css, acc=ACCENT[acc], header=nav.header("../", slug, True), side=nav.sidebar(series, "./", items, "./" if filename == "index.html" else filename, "../", slug)) + body.rstrip("\n") + "\n</div>\n" + nav.JS + "\n</body>\n</html>\n"
    (here.parent/filename).write_text(out)
    print("built", filename, len(out))

redirect(here.parent / "ch00.html", "./")
for source in sorted((here.parent / "john/src").glob("ch*.body.html")):
    filename = source.name.replace(".body", "")
    redirect(nav.SITE / "new-testament-john" / filename, "../new-testament/john/" + filename)
