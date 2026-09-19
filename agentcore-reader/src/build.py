"""Assemble chapter bodies into standalone HTML pages.
Each src/chNN.body.html starts with a line: <!-- title: ... | accent: think -->"""
import re, pathlib
here = pathlib.Path(__file__).parent
css = (here/"base.css").read_text()
fonts = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=BIZ+UDPGothic:wght@400;700&family=Zen+Kaku+Gothic+New:wght@700;900&family=JetBrains+Mono:wght@500&display=swap">'
for f in sorted(here.glob("*.body.html")):
    src = f.read_text()
    m = re.match(r"<!--\s*title:\s*(.+?)\s*\|\s*accent:\s*(\w+)\s*-->\n", src)
    if not m: raise SystemExit(f"{f.name}: missing header comment")
    title, acc = m.groups()
    body = src[m.end():]
    out = f"<!doctype html>\n<html lang=\"en\">\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<meta name=\"robots\" content=\"noindex\">\n<title>{title}</title>\n{fonts}\n<style>\n{css}</style>\n<div class=\"wrap acc-{acc}\">\n{body}\n</div>\n"
    (here.parent/f.name.replace(".body","")).write_text(out)
    print("built", f.name.replace(".body",""), len(out))
