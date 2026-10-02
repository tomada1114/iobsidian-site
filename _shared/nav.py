"""Site-wide header and reader sidebar, shared by every build.py and by index.html.

Every page gets a compact header linking back to the bookshelf. Reader pages also
get a sidebar listing the reader's pages: fixed on the left on wide screens, a drawer
opened from the header's menu button on phones.

The site is also an installable web app that works offline: head() links the manifest and
icons, JS registers sw.js, and the bookshelf's "Save all for offline" button stores
every page in the service worker's cache. Opened online, the bookshelf counts new pages not
yet saved and removed pages still saved, so the reader knows when to press it again.

    python3 _shared/nav.py   # regenerates the bookshelf from the catalogue below
"""
import html, pathlib, re

SITE = pathlib.Path(__file__).resolve().parent.parent

# (slug, short label for navigation and reading history, entry page inside the slug folder)
READERS = [
    ("easy-reads", "Easy Reads", "index.html"),
    ("1on1-architecture", "Architecture", "ch00.html"),
    ("1on1-api-types", "API & TypeScript", "ch00.html"),
    ("1on1-aws", "AWS", "ch00.html"),
    ("1on1-ai", "AI in Production", "ch00.html"),
    ("1on1-ops", "Operations", "ch00.html"),
    ("agentcore-reader", "AgentCore", "ch00.html"),
    ("book-pause-before-speaking", "一拍おいて話す", "ch00.html"),
    ("book-career-transitions", "キャリアの移り目", "ch00.html"),
    ("book-spend-by-design", "貯めるより、使いきる設計", "ch00.html"),
    ("book-world-by-data", "思い込みを外して、世界をデータで見る", "ch00.html"),
    ("book-information-networks", "情報は人をつなぎ、分断する", "ch00.html"),
    ("book-tidy-then-change", "整えてから変えるか、変えてから整えるか", "ch00.html"),
    ("book-money-anxiety", "その不安は、お金で消えるのか", "ch00.html"),
    ("book-what-follows", "その文から何が言えるか", "ch00.html"),
    ("book-not-all-in", "全身全霊で働かないという選択", "ch00.html"),
    ("book-loose-steady", "ゆるく、でも毎日積み上げる", "ch00.html"),
    ("book-choose-the-question", "答えを出す前に、問いを選ぶ", "ch00.html"),
    ("book-keep-skills-current", "技能を更新しつづける", "ch00.html"),
    ("book-uncertainty-teams", "不確実性から考えるチームと組織", "ch00.html"),
    ("book-being-heard", "話を聞いてもらうと、なぜ人は変わるのか", "ch00.html"),
    ("book-job-membership", "ジョブ型とメンバーシップ型で読む働き方", "ch00.html"),
    ("book-team-english", "英語でチームを回す仕事の型", "ch00.html"),
    ("book-plan-and-dialogue", "計画と対話を行き来する", "ch00.html"),
    ("book-wealth-mindset", "富を積み上げる人の考え方", "ch00.html"),
    ("book-beyond-command", "命令の組織から、探検の組織へ", "ch00.html"),
    ("book-adler-relationships", "アドラー心理学で人間関係をほどく", "ch00.html"),
    ("book-where-gains-went", "稼いだ分は、どこへ行ったのか", "ch00.html"),
    ("book-walk-and-think", "歩くと、頭と体に何が起きるか", "ch00.html"),
    ("book-life-not-a-story", "人生を物語にしない生き方", "ch00.html"),
    ("book-growing-sense", "AIの時代に、センスはどう育つか", "ch00.html"),
    ("book-faith-divides-america", "アメリカを割る信仰", "ch00.html"),
    ("book-job-yardstick", "仕事選びのものさしを科学で直す", "ch00.html"),
    ("book-recall-to-learn", "思い出して覚える、勉強の組み立て方", "ch00.html"),
    ("book-english-gaps", "大人の英語は、ずれに気づいて身につける", "ch00.html"),
    ("book-grounded-words", "ことばは体から育つ", "ch00.html"),
    ("book-many-logics", "論理はひとつではない", "ch00.html"),
    ("book-lasting-craft", "流行に左右されない作り手の心得", "ch00.html"),
    ("book-finite-time", "全部はできない前提で、時間を使う", "ch00.html"),
]
CUR = " aria-current=\"page\""

CSS = """
/* ---------- site header + reader sidebar (Site/_shared/nav.py) ---------- */
.site-head{position:sticky;top:0;z-index:30;margin:0 -16px;background:var(--bg);border-bottom:1px solid var(--line)}
.site-head .bar{display:flex;align-items:center;gap:20px;height:64px;padding:0 24px;max-width:1152px;margin:0 auto;min-width:0}
.site-head .brand{display:inline-flex;align-items:center;gap:10px;min-height:44px;font:600 15px/1.3 system-ui,sans-serif;letter-spacing:-.02em;color:var(--text);text-decoration:none;white-space:nowrap;flex:none}
.brand-icon{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.site-head .here{display:flex;align-items:center;gap:16px;color:var(--text-muted);font-size:var(--fs-small);min-width:0}
.site-head .here::before{content:"/";color:var(--text-subtle);flex:none}
.site-head .here>span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.site-caption{margin-left:auto;font:400 13px/1.4 system-ui,sans-serif;letter-spacing:.01em;color:var(--text-subtle);white-space:nowrap}
.menu-btn{display:none;align-items:center;justify-content:center;margin-left:auto;min-width:72px;min-height:44px;padding:0 12px;border:1px solid var(--line);border-radius:6px;
  background:var(--bg);color:var(--text);font:500 13px/1.3 system-ui,sans-serif;cursor:pointer;flex:none}
.menu-btn:hover{background:var(--surface)}
.skip-link{position:fixed;left:16px;top:-100px;z-index:100;padding:8px 16px;background:var(--bg);color:var(--text);border:2px solid var(--accent)}
.skip-link:focus{top:8px}
.side{font-size:var(--fs-small);line-height:var(--lh-tight)}
.side h2{font-size:var(--fs-caption);text-transform:uppercase;letter-spacing:.06em;color:var(--text-subtle);margin:0 0 8px}
.side h2 a{color:inherit;text-decoration:none}
.side ol,.side ul{list-style:none;margin:0 0 24px;padding:0}
.side li a{display:flex;gap:10px;padding:7px 10px 7px 12px;border-left:2px solid var(--line);border-radius:0 var(--radius) var(--radius) 0;color:var(--text-muted);text-decoration:none}
.side li a:hover{background:var(--surface);color:var(--text)}
.side li a[aria-current]{border-left-color:var(--accent);color:var(--accent);font-weight:700}
.side .n{font-family:var(--font-mono);font-size:var(--fs-caption);color:var(--text-subtle);flex:none;min-width:1.6em;white-space:nowrap;padding-top:1px}
.side li a[aria-current] .n{color:var(--accent)}
.side .all{margin-top:24px;padding-top:16px;border-top:1px solid var(--line)}
.side .all a{display:inline-flex;align-items:center;min-height:44px;color:var(--text-muted);text-decoration:none}
@media (min-width:1080px){
  .has-side .page{margin-left:max(300px,calc((100% - var(--measure))/2))}
  .side{position:fixed;top:65px;bottom:0;left:0;width:272px;overflow-y:auto;padding:28px 16px 40px 20px;border-right:1px solid var(--line)}
}
@media (max-width:1079.98px){
  .has-side .menu-btn{display:inline-flex}
  .side{position:fixed;inset:65px 0 0 0;z-index:25;overflow-y:auto;overscroll-behavior:contain;background:var(--bg);padding:20px 16px 48px;display:none}
  body.nav-open{overflow:hidden}
  body.nav-open .side{display:block}
}
@media (max-width:600px){
  .site-head .bar{gap:12px;height:56px;padding:0 16px}
  .site-head .brand{font-size:14px;gap:8px}
  .site-head .here{gap:10px;font-size:12px}
  .site-caption{font-size:12px}
  .side{top:57px}
  .brand-icon{width:18px;height:18px}
}
.offline{display:grid;gap:6px;justify-items:start;margin:28px 0 0}
.offline[hidden]{display:none}
.save-btn{min-height:44px;padding:0 14px;border:1px solid var(--line-strong);border-radius:var(--radius);
  background:var(--surface);color:var(--text);font:inherit;font-size:var(--fs-small);cursor:pointer}
.save-btn:disabled{opacity:.6;cursor:progress}
.save-note{margin:0;font-size:var(--fs-caption);color:var(--text-muted);line-height:var(--lh-tight)}
"""

JS = r"""<script>
(function(){var b=document.querySelector(".menu-btn");if(!b)return;
var side=document.querySelector(".side"),main=document.querySelector(".page"),small=window.matchMedia("(max-width:1079.98px)");
function set(o){o=o&&small.matches;document.body.classList.toggle("nav-open",o);b.setAttribute("aria-expanded",String(o));b.textContent=o?"Close":"Contents";if(main)main.inert=o;
  if(o){var first=side.querySelector("a[aria-current]")||side.querySelector("a");if(first)first.focus()}else b.focus()}
b.addEventListener("click",function(){set(!document.body.classList.contains("nav-open"))});
document.addEventListener("keydown",function(e){if(!document.body.classList.contains("nav-open"))return;
  if(e.key==="Escape"){e.preventDefault();set(false)}
  if(e.key==="Tab"){var links=side.querySelectorAll("a[href]"),last=links[links.length-1];
    if(e.shiftKey&&document.activeElement===b){e.preventDefault();last.focus()}
    else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();b.focus()}}
});
small.addEventListener("change",function(){if(!small.matches){document.body.classList.remove("nav-open");b.setAttribute("aria-expanded","false");b.textContent="Contents";if(main)main.inert=false}});
var c=document.querySelector(".side [aria-current]");if(c&&c.scrollIntoView&&window.matchMedia("(min-width:1080px)").matches)c.scrollIntoView({block:"center"});
})();
(function(){var h=document.querySelector(".site-head"),s=h&&h.dataset.reader;if(!s||!document.body.classList.contains("has-side"))return;
var r;try{r=JSON.parse(localStorage.getItem("bookshelf:recent")||"[]")}catch(e){r=[]}if(!Array.isArray(r))r=[];
r=r.filter(function(e){return e&&e.s!==s});
r.unshift({s:s,l:h.dataset.label,u:location.pathname,t:/\/ch00\.html$/.test(location.pathname)?"Contents":document.title.replace(/ \| .*$/,"").replace(/^.*? (\d\d) · /,"$1 · "),at:Date.now()});
try{localStorage.setItem("bookshelf:recent",JSON.stringify(r.slice(0,8)))}catch(e){}
})();
(function(){var h=document.querySelector(".site-head");if(!h||!("serviceWorker" in navigator)||!window.caches)return;
var root=new URL(h.dataset.root||"./",location.href).href;
navigator.serviceWorker.register(root+"sw.js").catch(function(){});
var box=document.querySelector(".offline");if(!box)return;
var btn=box.querySelector(".save-btn"),label=btn.querySelector(".save-label")||btn,note=box.querySelector(".save-note"),C="bookshelf-pages",K="bookshelf:saved";
function saved(){try{return localStorage.getItem(K)}catch(e){return null}}
function clean(u,base){u=new URL(u,base);return u.origin+u.pathname}
function pages(doc,base){return Array.prototype.map.call(doc.querySelectorAll(".side ol a"),function(a){return clean(a.getAttribute("href"),base)})}
function uniq(a){return a.filter(function(u,i){return a.indexOf(u)===i})}
function isPage(u){return u.indexOf(root)===0&&/\.html$/.test(u)}
async function urls(){var lists=await Promise.all(Array.prototype.map.call(document.querySelectorAll(".book-list a[data-slug]"),async function(a){
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
function last(){var t=saved();return t?"Last saved "+t+".":"Not saved on this device yet."}
async function show(){label.textContent=saved()?"Update offline copy":"Save all for offline";
  if(!navigator.onLine){note.textContent="Offline. "+last();return}
  note.textContent=last();
  try{var list=await urls(),d=await diff(list),m=d.missing.length,g=d.gone.length;
    if(saved()&&(m||g))note.textContent=[m?m+" new page"+(m>1?"s":"")+" not saved":"",g?g+" removed page"+(g>1?"s":"")+" still saved":""].filter(Boolean).join(", ")+". Press the button to update.";
    else if(saved())note.textContent="All "+list.length+" pages are saved. "+last()}catch(e){}}
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
  <button class="save-btn" type="button"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12m-4-4 4 4 4-4M4 16v4h16v-4"/></svg><span class="save-label">Save all for offline</span></button>
  <p class="save-note" aria-live="polite"></p>
</div>"""


def lang_attr(slug):
    """ lang="xx" for a reader whose content is not English (the site UI is English)."""
    lang = BOOKS[slug][6] if slug in BOOKS else "en"
    return "" if lang == "en" else f' lang="{lang}"'


def header(root, current=None, with_side=False):
    """root: relative path from the page to Site/ ("" or "../" or "../../")."""
    label = next((label for slug, label, _ in READERS if slug == current), "")
    here = f'<span class="here"><span{lang_attr(current)}>{html.escape(label)}</span></span>' if with_side else ""
    btn = '\n  <button class="menu-btn" type="button" aria-controls="side" aria-expanded="false">Contents</button>' if with_side else '<span class="site-caption">Personal library</span>'
    data = f' data-reader="{html.escape(current, quote=True)}" data-label="{html.escape(label, quote=True)}"' if current else ""
    skip = '<a class="skip-link" href="#library">Skip to library</a>\n' if not with_side else ""
    return f"""{skip}<header class="site-head" lang="en" data-root="{root}"{data}>
<div class="bar">
  <a class="brand" href="{root}index.html"><svg class="brand-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4.5h5a6 6 0 0 1 4 1.5 6 6 0 0 1 4-1.5h5V20h-5a6 6 0 0 0-4 1.5A6 6 0 0 0 8 20H3zM12 6v15.5"/></svg>Bookshelf</a>{here}{btn}
</div>
</header>"""


def sidebar(title, home, items, current, root, reader_slug):
    """items: list of (href, number-or-empty, label). current: href of this page."""
    rows = "\n".join(
        f'    <li><a href="{h}"{CUR if h == current else ""}><span class="n">{n}</span><span>{html.escape(t)}</span></a></li>'
        for h, n, t in items)
    return f"""<aside class="side" id="side" aria-label="{html.escape(title)} pages">
  <h2><a href="{home}">{html.escape(title)}</a></h2>
  <ol>
{rows}
  </ol>
  <div class="all" lang="en">
    <a href="{root}index.html">← All readers</a>
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


# ---------- bookshelf (index.html) ----------
# Categories in display order: (key, heading, one-line note, page accent 1-4)
CATEGORIES = [
    ("english", "Everyday English", "Short and easy reads for daily practice.", 3),
    ("software", "Building Software", "Talks on how to shape code, types and APIs, and run a product safely.", 1),
    ("cloud-ai", "AWS and AI", "Talks on running an app on AWS, LLM features in production, and agents.", 2),
    ("quick-books", "Quick Books", "Japanese books you can finish in about an hour: business, ideas and skills.", 4),
]
# Bookshelf entry per reader slug: category key, series kicker, title, blurb, reading time, level (may be ""),
# language of the reader's content (a key of LANGS; it must match LANG in the reader's build.py).
# Kicker, title and blurb are written in that language; the rest of the UI stays English.
# The page count is read from the reader's src/ (chapters other than ch00, or Easy Reads' reads).
LANGS = {"en": ("English", "english"), "ja": ("Japanese", "japanese 日本語")}  # code -> (label, extra search words)
BOOKS = {
    "easy-reads": ("english", "", "Easy Reads", "Short and easy English reads on many topics. Six new ones every morning.", "3 to 4 min each", "A2+ to B1", "en"),
    "1on1-architecture": ("software", "One-on-Ones", "Architecture", "What architecture is for: dependency rules, ports and adapters, DDD, and how to choose.", "About 1.5 hours", "B2 · dialogue", "en"),
    "1on1-api-types": ("software", "One-on-Ones", "API and TypeScript", "Types and APIs that last: parsing at the boundary, contracts, versioning, retries and offline.", "About 1.5 hours", "B2 · dialogue", "en"),
    "1on1-ops": ("software", "One-on-Ones", "Operations and Quality", "Running and changing a product safely: logs, alarms, SLOs, tests, gates, deploys and launch.", "About 1.5 hours", "B2 · dialogue", "en"),
    "1on1-aws": ("cloud-ai", "One-on-Ones", "AWS Foundation", "Running a small app on AWS: access, Lambda, DynamoDB, infrastructure as code, sign-in and cost.", "About 2 hours", "B2 · dialogue", "en"),
    "1on1-ai": ("cloud-ai", "One-on-Ones", "AI in Production", "LLM features in a real product: cost, typed output, evaluation, defenses and agents.", "About 1.75 hours", "B2 · dialogue", "en"),
    "agentcore-reader": ("cloud-ai", "", "AgentCore Reader", "Building AI agents for companies on AWS, part by part, before the hands-on study.", "About 1.5 hours", "B2 · dialogue", "en"),
    "book-pause-before-speaking": ("quick-books", "", "一拍おいて話す", "口を開く前の数秒で信頼は決まる。指摘・報告・相談の場面で、話す前に何を確かめるか。", "About 1 hour", "", "ja"),
    "book-career-transitions": ("quick-books", "", "キャリアの移り目", "人生100年時代、働く途中の学び直しや休む期間をどう計画し、どう説明し、誰と支え合うか。", "About 1 hour", "", "ja"),
    "book-spend-by-design": ("quick-books", "", "貯めるより、使いきる設計", "お金・時間・健康を、いつ何に使うかを先に決める。貯め続けて使えずに終わらないための設計。", "About 1 hour", "", "ja"),
    "book-world-by-data": ("quick-books", "", "思い込みを外して、世界をデータで見る", "判断の前に数字を集め、比べる相手・変化の向き・散らばりと一緒に読む。思い込みのずれを七つの場面で確かめる。", "About 1 hour", "", "ja"),
    "book-information-networks": ("quick-books", "", "情報は人をつなぎ、分断する", "情報は事実を写すだけでなく人を結びつけ、ときに分ける。職場と社会で情報がどう働き、どこで誤るのか。", "About 1 hour", "", "ja"),
    "book-tidy-then-change": ("quick-books", "", "整えてから変えるか、変えてから整えるか", "コードの動きを変えずに形だけを小さく整える型と、整える時機の選び方を練習問題で身につける。", "About 1 hour", "", "ja"),
    "book-money-anxiety": ("quick-books", "", "その不安は、お金で消えるのか", "貯金を増やしても消えない将来の心配。その出どころを見分け、お金のほかに何を蓄えるかを昼休みの会話で考える。", "About 1 hour", "", "ja"),
    "book-what-follows": ("quick-books", "", "その文から何が言えるか", "文から必ず言えることと言えないことを見分ける。否定・量・前提・指示語の働きから、AIがつまずく所までを練習問題で。", "About 1 hour", "", "ja"),
    "book-not-all-in": ("quick-books", "", "全身全霊で働かないという選択", "働き始めて本が読めなくなったのはなぜか。仕事にすべてを注ぐ働き方を見直し、余力を残して働く決め方を考える。", "About 1 hour", "", "ja"),
    "book-loose-steady": ("quick-books", "", "ゆるく、でも毎日積み上げる", "大事なことと毎日の小さな行動には厳しく、やり方とペースは柔らかく。情報の入口から続け方までを職場の場面で。", "About 1 hour", "", "ja"),
    "book-choose-the-question": ("quick-books", "", "答えを出す前に、問いを選ぶ", "手を動かす前に答えるべき問いを選び、答えの出る形に直し、粗く確かめて渡す。仕事の進め方の基本。", "About 1 hour", "", "ja"),
    "book-keep-skills-current": ("quick-books", "", "技能を更新しつづける", "技能が古くなる速さが増すなかで、古びた所を見つけ、学び直し、隣の分野へ広げて長く働き続けるための道具。", "About 1 hour", "", "ja"),
    "book-uncertainty-teams": ("quick-books", "", "不確実性から考えるチームと組織", "職場の困りごとの多くは「わからなさ」から生まれる。不確実性を見分けて減らす考え方をチームと組織に当てはめる。", "About 1 hour", "", "ja"),
    "book-being-heard": ("quick-books", "", "話を聞いてもらうと、なぜ人は変わるのか", "カウンセリングで聞き手は何をしていて、相談した人はどう変わるのか。相談するときにも聞くときにも使える見方。", "About 1 hour", "", "ja"),
    "book-job-membership": ("quick-books", "", "ジョブ型とメンバーシップ型で読む働き方", "仕事が先か、人が先か。二つの型を物差しにすると、採用・給料・働く時間・非正規の問題が一本の筋でつながる。", "About 1 hour", "", "ja"),
    "book-team-english": ("quick-books", "", "英語でチームを回す仕事の型", "確認・依頼・任せ方・1on1・会議・意見の違い。六つの場面で、何をどの順にどんな短い英語で言うかを型で学ぶ。", "About 1 hour", "", "ja"),
    "book-plan-and-dialogue": ("quick-books", "", "計画と対話を行き来する", "計画どおりに進めるやり方と、対話で計画を変えるやり方を切り替え、結果を出しながら自分から動くチームをつくる。", "About 1 hour", "", "ja"),
    "book-wealth-mindset": ("quick-books", "", "富を積み上げる人の考え方", "お金・技能・信頼を使い切らずに次の元手にして増やす。投資の手法より長く効く、絞り方・続け方・付き合い方。", "About 1 hour", "", "ja"),
    "book-beyond-command": ("quick-books", "", "命令の組織から、探検の組織へ", "会社を軍隊とみなす前提が、目標・会議・成長の場面で意欲をどう下げるか。成果と一人ひとりの関心を両立させる組み替え方。", "About 1 hour", "", "ja"),
    "book-adler-relationships": ("quick-books", "", "アドラー心理学で人間関係をほどく", "過去の失敗、上司との関係、人からの評価。アドラー心理学の考え方を職場の場面に当てはめて、悩みをほどく。", "About 1 hour", "", "ja"),
    "book-where-gains-went": ("quick-books", "", "稼いだ分は、どこへ行ったのか", "生産性が上がっても賃金が上がらなかったのはなぜか。会社の儲けの分け方から、日本の働き手の30年をたどる。", "About 1 hour", "", "ja"),
    "book-walk-and-think": ("quick-books", "", "歩くと、頭と体に何が起きるか", "歩くと発想・対話・記憶・気分に何が起きるかを研究で確かめ、仕事と暮らしに歩く時間を取り戻す。", "About 1 hour", "", "ja"),
    "book-life-not-a-story": ("quick-books", "", "人生を物語にしない生き方", "キャリアのストーリーや「何者かになりたい」願いはなぜ人を縛るのか。人生を遊びとして見る別の見方を会話で。", "About 1 hour", "", "ja"),
    "book-growing-sense": ("quick-books", "", "AIの時代に、センスはどう育つか", "何を取り入れ、何を捨て、どこまで仕上げるか。仕事の差がつく判断のものさしを、上司と部下の会話で育てる。", "About 1 hour", "", "ja"),
    "book-faith-divides-america": ("quick-books", "", "アメリカを割る信仰", "福音派の信仰、とくに終末についての考え方が、アメリカの政治と社会の分断にどう結びついてきたのか。", "About 1 hour", "", "ja"),
    "book-job-yardstick": ("quick-books", "", "仕事選びのものさしを科学で直す", "好きなこと・年収・適性で選ぶ方法は満足につながりにくい。研究で確かめた条件で仕事を比べ直す。", "About 1 hour", "", "ja"),
    "book-recall-to-learn": ("quick-books", "", "思い出して覚える、勉強の組み立て方", "読み返すより思い出す。日を空ける・混ぜる・説明するなど、効果が確かめられた勉強の組み立て方を練習問題で。", "About 1 hour", "", "ja"),
    "book-english-gaps": ("quick-books", "", "大人の英語は、ずれに気づいて身につける", "同じ所で残る英語の誤りは、日本語と英語の使い方の「ずれ」から来る。ずれに気づいて直す手順を学ぶ。", "About 1 hour", "", "ja"),
    "book-grounded-words": ("quick-books", "", "ことばは体から育つ", "ことばの意味はどこから来るのか。オノマトペや子どもの言葉の覚え方から、学び直しや技能の伝え方まで。", "About 1 hour", "", "ja"),
    "book-many-logics": ("quick-books", "", "論理はひとつではない", "「論理的」に求められる筋道は一つではない。四つの型の仕組みと使いどころを確かめ、目的と相手で選ぶ。", "About 1 hour", "", "ja"),
    "book-lasting-craft": ("quick-books", "", "流行に左右されない作り手の心得", "道具が替わっても使える、結果を引き受ける構え・変えやすく作る原則・知識への投資を、作り手の仕事に当てはめる。", "About 1 hour", "", "ja"),
    "book-finite-time": ("quick-books", "", "全部はできない前提で、時間を使う", "すべてをこなす前提を手放すと、時間の使い方はどう変わるか。限りある時間で何を選び、何を諦めるか。", "About 1 hour", "", "ja"),
}

SHELF_CSS = """
/* ---------- bookshelf: a flat, searchable reading index ---------- */
.shelf{
  --bg:#fafafa;--surface:#f0f1f3;--text:#202124;--text-muted:#62656b;--text-subtle:#686b73;
  --line:#e2e3e6;--line-strong:#b5b8bf;--accent:#2563a6;
  --font-body:-apple-system,BlinkMacSystemFont,"Segoe UI","Hiragino Sans","Noto Sans JP",sans-serif;
  font-size:16px;line-height:1.55;
}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]) .shelf{
  --bg:#111214;--surface:#1b1d21;--text:#eeeeef;--text-muted:#a4a6ad;--text-subtle:#9699a2;
  --line:#292b30;--line-strong:#555962;--accent:#8db4dc;
}}
:root[data-theme="dark"] .shelf{
  --bg:#111214;--surface:#1b1d21;--text:#eeeeef;--text-muted:#a4a6ad;--text-subtle:#9699a2;
  --line:#292b30;--line-strong:#555962;--accent:#8db4dc;
}
.shelf .page{max-width:1104px;margin:0 auto;padding:56px 0 48px}
.shelf [hidden]{display:none!important}
.shelf-head{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;padding-bottom:36px;border-bottom:1px solid var(--line);scroll-margin-top:96px}
.shelf-head>*+*{margin-top:0}
.shelf-head h1{font-size:clamp(34px,3.8vw,48px);line-height:1.15;letter-spacing:-.045em;font-weight:600;text-wrap:balance}
.shelf-head .lead{font-size:16px;line-height:1.55;margin-top:12px}
.library-stats{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:18px;font-size:13px;letter-spacing:.01em;color:var(--text-subtle)}
.library-stats span+span::before{content:"·";margin-right:18px;color:var(--text-subtle)}
.shelf .offline{margin:0;gap:8px;max-width:240px;justify-items:end;text-align:right}
.shelf .save-btn{display:inline-flex;align-items:center;gap:8px;padding:0 12px;border-color:var(--line);background:var(--bg);font-size:13px;font-weight:500}
.shelf .save-btn:hover{background:var(--surface);border-color:var(--line-strong)}
.shelf .save-btn svg{height:16px;width:16px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;flex:none}
.shelf .save-note{font-size:12px;letter-spacing:.01em;line-height:1.5}
.shelf-label{font-size:12px;font-weight:500;letter-spacing:.06em;text-transform:uppercase;color:var(--text-subtle)}
.recent{margin-top:28px}
.recent ol{list-style:none;margin:12px 0 0;padding:0;border-top:1px solid var(--line)}
.recent li+li{margin-top:0}
.recent a{display:grid;grid-template-columns:minmax(0,1fr) auto 16px;align-items:center;gap:20px;padding:14px 0;border-bottom:1px solid var(--line);color:var(--text);text-decoration:none}
.recent a:hover{background:var(--surface)}
.recent .resume-copy{display:flex;align-items:baseline;flex-wrap:wrap;gap:4px 14px;min-width:0}
.recent .resume-copy b{font-size:15px;font-weight:500;line-height:1.6}
.recent .resume-copy span,.recent .when{font-size:12px;color:var(--text-muted)}
.recent .when{white-space:nowrap}
.recent .row-arrow{font-size:16px;color:var(--text-subtle)}
.library-layout{display:grid;grid-template-columns:176px minmax(0,1fr);gap:48px;margin-top:36px;align-items:start}
.shelf-browse{position:sticky;top:96px}
.shelf-browse .shelf-label{margin-bottom:12px}
.filters{display:flex;flex-direction:column;gap:4px}
.filter{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:44px;padding:8px 12px;border:0;border-radius:6px;background:transparent;color:var(--text-muted);font:inherit;font-size:13px;line-height:1.4;text-align:left;cursor:pointer}
.filter:hover{background:var(--surface);color:var(--text)}
.filter[aria-pressed="true"]{background:var(--surface);color:var(--text);font-weight:600}
.filter .n{font-size:12px;font-variant-numeric:tabular-nums;font-weight:400;color:var(--text-subtle)}
.browse-note{margin:24px 12px 0;padding-top:20px;border-top:1px solid var(--line);font-size:12px;line-height:1.65;letter-spacing:.01em;color:var(--text-subtle)}
.library-main{min-width:0;scroll-margin-top:88px}
.shelf-tools{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:28px}
.results-heading{font-size:18px;font-weight:600;line-height:1.4;letter-spacing:-.015em}
.result-count{margin-top:4px;font-size:12px;letter-spacing:.01em;color:var(--text-subtle)}
.search-wrap{position:relative;flex:0 1 288px;min-width:0}
.mobile-category{display:none}
.search-wrap svg{position:absolute;top:14px;left:14px;width:16px;height:16px;fill:none;stroke:var(--text-muted);stroke-width:1.7;stroke-linecap:round;pointer-events:none}
.shelf-search{width:100%;min-height:44px;padding:10px 12px 10px 40px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--text);font:inherit;font-size:14px;line-height:1.4}
.shelf-search::placeholder{color:var(--text-subtle);opacity:1}
.cat{margin-top:32px}
.cat:first-of-type{margin-top:0}
.cat>*+*{margin-top:0}
.cat-intro{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin-bottom:12px}
.library-main.filtered .cat-intro{display:none}
.cat-head{font-size:13px;font-weight:600;letter-spacing:.01em;line-height:1.4;color:var(--text-muted)}
.cat-head .n{margin-left:8px;font-size:12px;font-weight:400;color:var(--text-subtle);font-variant-numeric:tabular-nums}
.cat-note{font-size:12px;color:var(--text-subtle);line-height:1.5;text-align:right;max-width:50ch}
.book-list{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.book-list li+li{margin-top:0}
.book-row{display:grid;grid-template-columns:28px minmax(0,1fr) 138px 16px;gap:16px;align-items:start;padding:20px 0;border-bottom:1px solid var(--line);color:var(--text);text-decoration:none}
.book-row:hover{background:var(--surface)}
.book-row:hover .book-title{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:4px}
.book-number{padding-top:3px;color:var(--text-subtle);font:400 12px/1.5 var(--font-mono);font-variant-numeric:tabular-nums}
.book-copy{min-width:0}
.book-title{display:block;font-size:17px;font-weight:600;line-height:1.5;letter-spacing:-.012em;text-wrap:balance}
.book-title:lang(ja){letter-spacing:0;word-break:auto-phrase}
.book-series{font-weight:400;font-size:12px;letter-spacing:.01em;color:var(--text-subtle);margin-left:10px;white-space:nowrap}
.book-blurb{display:block;margin-top:6px;font-size:14px;color:var(--text-muted);line-height:1.6;text-wrap:pretty}
.book-blurb:lang(ja){line-height:1.75}
.book-facts{display:flex;flex-direction:column;gap:4px;padding-top:3px;font-size:12px;letter-spacing:.01em;line-height:1.5;color:var(--text-subtle);text-align:right;font-variant-numeric:tabular-nums}
.book-facts .reading-time{color:var(--text-muted)}
.book-row .row-arrow{padding-top:1px;font-size:17px;color:var(--text-subtle)}
.no-hits{padding:36px 0;border-top:1px solid var(--line)}
.no-hits h2{font-size:20px;font-weight:600;letter-spacing:-.02em}
.no-hits p{margin-top:8px;color:var(--text-muted);font-size:14px}
.reset-filters{min-height:44px;margin-top:16px;padding:0;border:0;background:transparent;color:var(--text);font:inherit;font-size:14px;text-decoration:underline;text-underline-offset:4px;cursor:pointer}
.shelf-foot{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px 20px;margin-top:48px;padding-top:20px;border-top:1px solid var(--line);font-size:12px;letter-spacing:.01em;color:var(--text-subtle)}
.shelf-foot a{display:inline-flex;align-items:center;min-height:44px;color:var(--text-muted);text-decoration:none}
.shelf-foot a:hover{text-decoration:underline}
.shelf button{touch-action:manipulation}
@media(max-width:900px){
  .library-layout{grid-template-columns:150px minmax(0,1fr);gap:28px}
  .cat-note{display:none}
  .book-row{grid-template-columns:24px minmax(0,1fr) 16px;gap:12px}
  .book-facts{grid-column:2;grid-row:2;flex-direction:row;flex-wrap:wrap;text-align:left;padding-top:0;gap:4px 12px;margin-top:-4px}
  .book-row .row-arrow{grid-column:3;grid-row:1}
}
@media(max-width:700px){
  .shelf .page{padding:32px 4px 24px}
  .shelf-head{display:block;padding-bottom:24px}
  .shelf-head .lead{font-size:14px}
  .library-stats{font-size:12px;gap:6px 12px;margin-top:14px}
  .library-stats span+span::before{margin-right:12px}
  .shelf .offline{max-width:none;justify-items:start;text-align:left;margin-top:24px}
  .shelf .save-note{max-width:36ch}
  .library-layout{display:block;margin-top:28px}
  .shelf-browse{display:none}
  .shelf-tools{flex-wrap:wrap;gap:16px;margin-bottom:24px}
  .search-wrap{flex:1 1 100%;order:-1}
  .mobile-category{display:block;max-width:55%;min-width:0}
  .category-select{width:100%;min-height:44px;padding:8px 10px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--text);font:inherit;font-size:12px;line-height:1.4;cursor:pointer}
  .book-row{padding:18px 0}
  .book-title{font-size:16px}
  .book-blurb{font-size:13px}
  .book-number{font-size:11px}
  .book-series{display:block;margin:4px 0 0}
  .recent a{gap:12px;grid-template-columns:minmax(0,1fr) auto 16px}
  .recent .resume-copy{display:block}
  .recent .resume-copy span{display:block;margin-top:2px}
  .recent .when{font-size:11px}
  .shelf-foot{margin-top:32px}
}
"""


SHELF_JS = r"""<script>
(function(){
var q=document.querySelector(".shelf-search"),filters=document.querySelectorAll(".filter"),select=document.querySelector(".category-select"),none=document.querySelector(".no-hits"),count=document.querySelector(".result-count"),heading=document.querySelector(".results-heading"),cat="";
if(!q)return;
function normalize(s){return s.normalize("NFKC").toLowerCase()}
function apply(){var words=normalize(q.value.trim()).split(/\s+/).filter(Boolean),total=0;
  document.querySelector(".library-main").classList.toggle("filtered",!!cat);
  document.querySelectorAll(".cat").forEach(function(sec){var n=0;
    sec.querySelectorAll(".book-list>li").forEach(function(li){var text=normalize(li.dataset.text),ok=(!cat||sec.dataset.cat===cat)&&words.every(function(w){return text.indexOf(w)>=0});li.hidden=!ok;if(ok)n++});
    sec.hidden=!n;sec.querySelector(".cat-head .n").textContent=n;total+=n});
  count.textContent=total+" reader"+(total===1?"":"s")+(q.value.trim()?" found":"");none.hidden=total>0;
  filters.forEach(function(f){f.setAttribute("aria-pressed",String(f.dataset.cat===cat))});
  select.value=cat;
  var active=Array.prototype.find.call(filters,function(f){return f.dataset.cat===cat});heading.textContent=active.dataset.name;
}
q.addEventListener("input",apply);
filters.forEach(function(f){f.addEventListener("click",function(){cat=f.dataset.cat;apply()})});
select.addEventListener("change",function(){cat=select.value;apply()});
document.querySelector(".reset-filters").addEventListener("click",function(){cat="";q.value="";apply();q.focus()});
apply();
var r;try{r=JSON.parse(localStorage.getItem("bookshelf:recent")||"[]")}catch(e){r=[]}if(!Array.isArray(r))r=[];
var box=document.querySelector(".recent"),catalog=new Map();
document.querySelectorAll(".book-list a[data-slug]").forEach(function(a){catalog.set(a.dataset.slug,a)});
var fmt=window.Intl&&Intl.RelativeTimeFormat?new Intl.RelativeTimeFormat("en",{numeric:"auto"}):null;
function ago(t){if(!fmt)return "Recently";var h=Math.round((t-Date.now())/36e5);return h>-1?"Just now":h>-24?fmt.format(h,"hour"):fmt.format(Math.round(h/24),"day")}
var shown=0;
r.forEach(function(e){if(!e||shown>=3||!catalog.has(e.s)||!Number.isFinite(e.at))return;
  var book=catalog.get(e.s),url;try{url=new URL(e.u,location.href)}catch(err){return}
  var readerRoot=new URL("./",book.href);if(url.origin!==location.origin||!url.pathname.startsWith(readerRoot.pathname)||!url.pathname.endsWith(".html"))return;
  var li=document.createElement("li"),a=document.createElement("a"),copy=document.createElement("span"),title=document.createElement("b"),page=document.createElement("span"),when=document.createElement("time"),arrow=document.createElement("span");
  a.href=url.pathname;a.setAttribute("aria-label","Continue reading "+book.dataset.title+": "+(e.t||"Contents"));copy.className="resume-copy";
  title.textContent=book.dataset.title;title.lang=book.dataset.lang;page.textContent=e.t||"Contents";page.lang=e.t&&e.t!=="Contents"?book.dataset.lang:"en";
  when.className="when";when.dateTime=new Date(e.at).toISOString();when.textContent=ago(e.at);arrow.className="row-arrow";arrow.textContent="→";arrow.setAttribute("aria-hidden","true");
  copy.append(title,page);a.append(copy,when,arrow);li.appendChild(a);box.querySelector("ol").appendChild(li);shown++;
});
box.hidden=!shown;
})();
</script>"""


def page_count(slug):
    """Counted from the sources, so it is right before the reader is built."""
    src = SITE / slug / "src"
    if (src / "reads").is_dir():
        return len(list((src / "reads").glob("*.body.html"))), "reads"
    return len([f for f in src.glob("ch[0-9][0-9].body.html") if not f.name.startswith("ch00")]), "pages"


def shelf():
    """Generate the reading index, category rail, search, history and offline controls."""
    entry = {slug: e for slug, _, e in READERS}
    total = sum(page_count(s)[0] for s in BOOKS)
    sections = []
    filters = [f'<button class="filter" type="button" data-cat="" data-name="All readers" aria-pressed="true"><span>All readers</span><span class="n">{len(BOOKS)}</span></button>']
    options = [f'<option value="">All readers ({len(BOOKS)})</option>']
    number = 0
    for key, name, note, _ in CATEGORIES:
        books = [s for s, *_ in READERS if BOOKS[s][0] == key]
        if not books:
            continue
        filters.append(f'<button class="filter" type="button" data-cat="{key}" data-name="{html.escape(name, quote=True)}" aria-pressed="false"><span>{html.escape(name)}</span><span class="n">{len(books)}</span></button>')
        options.append(f'<option value="{key}">{html.escape(name)} ({len(books)})</option>')
        rows = []
        for slug in books:
            number += 1
            _, series, title, blurb, time, level, lang = BOOKS[slug]
            n, unit = page_count(slug)
            language, words = LANGS[lang]
            text = html.escape(" ".join([series, title, blurb, name, time, level, language, words]).lower(), quote=True)
            lt = lang_attr(slug)
            series_label = f' <span class="book-series"{lt}>{html.escape(series)}</span>' if series else ""
            facts = [time, f"{n} {unit if n != 1 else unit[:-1]}", f"{language} · {level}" if level else language]
            rows.append(f"""    <li data-text="{text}">
      <a class="book-row" href="{slug}/{entry[slug]}" data-slug="{slug}" data-title="{html.escape(title, quote=True)}" data-lang="{lang}">
        <span class="book-number" aria-hidden="true">{number:02d}</span>
        <span class="book-copy"><span class="book-title"{lt}>{html.escape(title)}{series_label}</span><span class="book-blurb"{lt}>{html.escape(blurb)}</span></span>
        <span class="book-facts"><span class="reading-time">{html.escape(facts[0])}</span><span>{html.escape(facts[1])}</span><span>{html.escape(facts[2])}</span></span>
        <span class="row-arrow" aria-hidden="true">→</span>
      </a>
    </li>""")
        sections.append(f"""<section class="cat" data-cat="{key}" aria-labelledby="cat-{key}">
  <div class="cat-intro"><h2 class="cat-head" id="cat-{key}">{html.escape(name)} <span class="n">{len(books)}</span></h2><p class="cat-note">{html.escape(note)}</p></div>
  <ul class="book-list">
{chr(10).join(rows)}
  </ul>
</section>""")
    languages = " & ".join(LANGS[l][0] for l in LANGS if any(b[6] == l for b in BOOKS.values()))
    return f"""<header class="page-head shelf-head" id="shelf-top">
  <div class="intro">
    <h1>Bookshelf</h1>
    <p class="lead">Readers I made for my own study.</p>
    <p class="library-stats"><span>{len(BOOKS)} readers</span><span>{total} pages</span><span>{html.escape(languages)}</span></p>
  </div>
  {offline_box()}
</header>
<section class="recent" aria-labelledby="recent-title" hidden>
  <h2 class="shelf-label" id="recent-title">Continue reading</h2>
  <ol></ol>
</section>
<div class="library-layout">
  <aside class="shelf-browse" aria-label="Library categories">
    <h2 class="shelf-label">Browse</h2>
    <div class="filters" role="group" aria-label="Categories">
      {(chr(10) + "      ").join(filters)}
    </div>
    <p class="browse-note">A little English practice.<br>A new way to think.<br>Something to build.</p>
  </aside>
  <main class="library-main" id="library" tabindex="-1" aria-labelledby="results-title">
    <div class="shelf-tools">
      <div><h2 class="results-heading" id="results-title">All readers</h2><p class="result-count" role="status" aria-live="polite" aria-atomic="true">{len(BOOKS)} readers</p></div>
      <div class="search-wrap"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4.5 4.5"/></svg><input class="shelf-search" type="search" placeholder="Search titles or topics" aria-label="Search readers" autocomplete="off"></div>
      <label class="mobile-category"><select class="category-select" aria-label="Browse category">{"".join(options)}</select></label>
    </div>
    {chr(10).join(sections)}
    <div class="no-hits" hidden><h2>No readers found</h2><p>Try another title or topic, or browse all readers.</p><button class="reset-filters" type="button">Clear search and filters</button></div>
  </main>
</div>
<footer class="shelf-foot"><span>A personal library by tomada.</span><a href="#shelf-top">Back to top ↑</a></footer>
{SHELF_JS}"""



def patch_index():
    """Regenerate the bookshelf body from READERS, CATEGORIES and BOOKS, keeping index.html's head."""
    missing = [s for s, *_ in READERS if s not in BOOKS]
    if missing:
        raise SystemExit(f"add a BOOKS entry for: {', '.join(missing)}")
    p = SITE / "index.html"
    s = p.read_text()
    s = re.sub(r"\n<style id=\"site-nav\">.*?</style>", "", s, flags=re.S)
    s = s.replace("</head>", f'<style id="site-nav">{CSS}{SHELF_CSS}</style>\n</head>', 1)
    s = re.sub(r"<!-- app -->.*?<!-- /app -->\n", "", s, flags=re.S)
    s = s.replace("</head>", f"<!-- app -->\n{head('')}\n<!-- /app -->\n</head>", 1)
    s = re.sub(r"<body[^>]*>\n.*</body>", lambda m: f"""<body class="shelf acc-1">
<!-- site-header -->
{header('')}
<!-- /site-header -->
<div class="page">
{shelf()}
</div>
<!-- site-js -->
{JS}
<!-- /site-js -->
</body>""", s, count=1, flags=re.S)
    p.write_text(s)
    print("built index.html")


if __name__ == "__main__":
    patch_index()
