"""Assemble chapter bodies into standalone HTML pages.
Each src/chNN.body.html starts with a line: <!-- title: ... | accent: think -->
The page head matches reading-page-designing/assets/page-template.html; base.css is a copy of that skill's."""
import re, pathlib
here = pathlib.Path(__file__).parent
css = (here/"base.css").read_text()
LANG = "en"
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
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=BIZ+UDPGothic:wght@400;700&family=JetBrains+Mono:wght@500&display=swap">
<style>
{css}</style>
</head>
<body>
<div class="page acc-{acc}">
<svg class="svg-defs" width="0" height="0" aria-hidden="true" focusable="false" style="position:absolute">
  <defs>
    <marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker>
    <marker id="arw-acc" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah-acc"/></marker>
  </defs>
</svg>
"""
for f in sorted(here.glob("*.body.html")):
    src = f.read_text()
    m = re.match(r"<!--\s*title:\s*(.+?)\s*\|\s*accent:\s*(\w+)\s*-->\n", src)
    if not m: raise SystemExit(f"{f.name}: missing header comment")
    title, acc = m.groups()
    body = src[m.end():]
    out = head.format(lang=LANG, title=title, css=css, acc=ACCENT[acc]) + body.rstrip("\n") + "\n</div>\n</body>\n</html>\n"
    (here.parent/f.name.replace(".body","")).write_text(out)
    print("built", f.name.replace(".body",""), len(out))
