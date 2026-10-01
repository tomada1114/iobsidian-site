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
  body:not(.has-side) .site-head .bar{flex-wrap:wrap;padding-block:6px}
  body:not(.has-side) .site-head nav{flex:1 1 100%;min-width:0}}
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
(function(){var cur=document.querySelector(".site-head .readers a[aria-current]");if(!cur||!document.body.classList.contains("has-side"))return;
var s=new URL(cur.href).pathname.split("/").slice(-2,-1)[0],r;try{r=JSON.parse(localStorage.getItem("bookshelf:recent")||"[]")}catch(e){r=[]}
r=r.filter(function(e){return e.s!==s});
r.unshift({s:s,l:cur.textContent,u:location.pathname,t:/\\/ch00\\.html$/.test(location.pathname)?"Contents":document.title.replace(/ \\| .*$/,"").replace(/^.*? (\\d\\d) · /,"$1 · "),at:Date.now()});
try{localStorage.setItem("bookshelf:recent",JSON.stringify(r.slice(0,8)))}catch(e){}
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
    if(localStorage.getItem(K)&&(m||g))note.textContent=[m?m+" new page"+(m>1?"s":"")+" not saved":"",g?g+" removed page"+(g>1?"s":"")+" still saved":""].filter(Boolean).join(", ")+". Press the button to update.";
    else if(localStorage.getItem(K))note.textContent="All "+list.length+" pages are saved. "+last()}catch(e){}}
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


def lang_attr(slug):
    """ lang="xx" for a reader whose content is not English (the site UI is English)."""
    lang = BOOKS[slug][6] if slug in BOOKS else "en"
    return "" if lang == "en" else f' lang="{lang}"'


def header(root, current=None, with_side=False):
    """root: relative path from the page to Site/ ("" or "../" or "../../")."""
    links = "\n".join(
        f'    <li><a href="{root}{slug}/{entry}"{CUR if slug == current else ""}{lang_attr(slug)}>{label}</a></li>'
        for slug, label, entry in READERS)
    here = next((f'<span class="here">/ <span{lang_attr(slug)}>{label}</span></span>' for slug, label, _ in READERS if slug == current), "") if with_side else ""
    btn = '\n  <button class="menu-btn" type="button" aria-controls="side" aria-expanded="false">Menu</button>' if with_side else ""
    return f"""<header class="site-head" lang="en" data-root="{root}">
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
        f'    <li><a href="{root}{slug}/{entry}"{CUR if slug == reader_slug else ""}><span{lang_attr(slug)}>{label}</span></a></li>'
        for slug, label, entry in READERS)
    return f"""<aside class="side" id="side" aria-label="{html.escape(title)} pages">
  <h2><a href="{home}">{html.escape(title)}</a></h2>
  <ol>
{rows}
  </ol>
  <div class="all" lang="en">
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


# ---------- bookshelf (index.html) ----------
# Categories in display order: (key, heading, one-line note, page accent 1-4)
CATEGORIES = [
    ("english", "Everyday English", "Short and easy reads for daily practice.", 3),
    ("software", "Building Software", "Talks on how to shape code, types and APIs, and run a product safely.", 1),
    ("cloud-ai", "AWS and AI", "Talks on running an app on AWS, LLM features in production, and agents.", 2),
    ("quick-books", "Quick Books", "Japanese books you can finish in about an hour: business, ideas and skills.", 4),
]
# Bookshelf card per reader slug: category key, series kicker, title, blurb, reading time, level (may be ""),
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
/* ---------- bookshelf (Site/_shared/nav.py) ---------- */
.shelf .page{max-width:1120px}
.shelf-head{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:20px 40px}
.shelf-head>*+*{margin-top:0}
.shelf-head .intro>*+*{margin-top:12px}
.shelf-head .offline{margin:0}
.shelf-label{font-size:var(--fs-caption);font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--text-subtle)}
.recent{margin-top:32px}
.recent ol,.cards{list-style:none;margin:12px 0 0;padding:0;display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}
.recent li+li,.cards li+li{margin-top:0}
.recent a{display:grid;gap:2px;height:100%;padding:12px 16px;border:1px solid var(--line);border-radius:var(--radius);color:var(--text);text-decoration:none;
  box-shadow:inset 3px 0 0 var(--accent)}
.recent a:hover,.cards a:hover{background:var(--surface);border-color:var(--line-strong)}
.recent .kick,.cards .kick{font-size:var(--fs-caption);font-weight:700;letter-spacing:.04em;color:var(--accent)}
.recent b{font-size:var(--fs-small);line-height:var(--lh-tight)}
.recent .when{font-size:var(--fs-caption);color:var(--text-subtle)}
.shelf-tools{display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px;margin-top:36px;padding-bottom:16px;border-bottom:1px solid var(--line)}
.shelf-search{flex:1 1 240px;max-width:420px;min-height:44px;padding:0 12px;border:1px solid var(--line-strong);border-radius:var(--radius);
  background:var(--bg);color:var(--text);font:inherit;font-size:var(--fs-small)}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 14px;border:1px solid var(--line);border-radius:var(--radius);
  background:var(--bg);color:var(--text-muted);font:inherit;font-size:var(--fs-small);cursor:pointer}
.chip:hover{border-color:var(--line-strong);color:var(--text)}
.chip[aria-pressed="true"]{background:var(--text);border-color:var(--text);color:var(--bg)}
.chip .n,.cat-head .n{font-family:var(--font-mono);font-size:var(--fs-caption);font-weight:500;opacity:.75}
.cat{margin-top:36px}
.cat>*+*{margin-top:4px}
.cat-head{display:flex;align-items:center;gap:10px;font-size:var(--fs-h3)}
.cat-head::before{content:"";width:10px;height:10px;border-radius:2px;background:var(--accent);flex:none}
.cat-head .n{color:var(--text-subtle)}
.cat-note{font-size:var(--fs-small);color:var(--text-muted)}
.cat>.cards{margin-top:14px}
.cards a{position:relative;display:flex;flex-direction:column;gap:6px;height:100%;padding:16px 18px 16px 24px;border:1px solid var(--line);
  border-radius:var(--radius);color:var(--text);text-decoration:none}
.cards a::before{content:"";position:absolute;left:-1px;top:-1px;bottom:-1px;width:6px;background:var(--accent);border-radius:var(--radius) 0 0 var(--radius)}
.cards b{font-size:var(--fs-lead);line-height:var(--lh-tight)}
.cards .blurb{font-size:var(--fs-small);color:var(--text-muted);line-height:1.55;flex:1}
.cards .facts{display:flex;flex-wrap:wrap;gap:2px 14px;font-size:var(--fs-caption);color:var(--text-subtle)}
.no-hits{margin-top:32px;color:var(--text-muted)}
.cards b:lang(ja),.recent a:lang(ja) b{line-height:1.5;word-break:auto-phrase}
.cards .blurb:lang(ja){line-height:1.75}
"""

SHELF_JS = """<script>
(function(){var q=document.querySelector(".shelf-search"),chips=document.querySelectorAll(".chip"),none=document.querySelector(".no-hits"),cat="";
function apply(){var s=q.value.trim().toLowerCase(),any=false;
  document.querySelectorAll(".cat").forEach(function(sec){var n=0;
    sec.querySelectorAll(".cards>li").forEach(function(li){var ok=(!cat||sec.dataset.cat===cat)&&(!s||li.dataset.text.indexOf(s)>=0);li.hidden=!ok;if(ok)n++});
    sec.hidden=!n;if(n)any=true});
  none.hidden=any}
q.addEventListener("input",apply);
chips.forEach(function(c){c.addEventListener("click",function(){cat=c.dataset.cat;chips.forEach(function(x){x.setAttribute("aria-pressed",x===c)});apply()})});
var r;try{r=JSON.parse(localStorage.getItem("bookshelf:recent")||"[]")}catch(e){r=[]}
var box=document.querySelector(".recent");if(!box||!r.length)return;
var fmt=window.Intl&&Intl.RelativeTimeFormat?new Intl.RelativeTimeFormat("en",{numeric:"auto"}):null;
function ago(t){if(!fmt)return "";var h=Math.round((t-Date.now())/36e5);return h>-1?"Just now":h>-24?fmt.format(h,"hour"):fmt.format(Math.round(h/24),"day")}
r.slice(0,3).forEach(function(e){var card=document.querySelector('.cards a[data-slug="'+e.s+'"]');if(!card)return;
  var li=document.createElement("li"),a=document.createElement("a");li.className=card.closest(".cat").className.replace("cat","").trim();a.href=e.u;if(card.dataset.lang)a.lang=card.dataset.lang;
  [["kick",e.l],["b",e.t],["when",ago(e.at)]].forEach(function(p){var x=document.createElement(p[0]==="b"?"b":"span");if(p[0]!=="b")x.className=p[0];x.textContent=p[1];a.appendChild(x)});
  li.appendChild(a);box.querySelector("ol").appendChild(li)});
box.hidden=!box.querySelector("li")})();
</script>"""


def page_count(slug):
    """Counted from the sources, so it is right before the reader is built."""
    src = SITE / slug / "src"
    if (src / "reads").is_dir():
        return len(list((src / "reads").glob("*.body.html"))), "reads"
    return len([f for f in src.glob("ch[0-9][0-9].body.html") if not f.name.startswith("ch00")]), "pages"


def shelf():
    """The bookshelf page body: head with the save button, continue reading, search and category filter, category sections."""
    entry = {slug: e for slug, _, e in READERS}
    total = sum(page_count(s)[0] for s in BOOKS)
    secs, chips = [], ['<button class="chip" type="button" data-cat="" aria-pressed="true">All <span class="n">%d</span></button>' % len(BOOKS)]
    for key, name, note, acc in CATEGORIES:
        books = [s for s, *_ in READERS if BOOKS[s][0] == key]
        if not books:
            continue
        chips.append(f'<button class="chip" type="button" data-cat="{key}" aria-pressed="false">{html.escape(name)} <span class="n">{len(books)}</span></button>')
        cards = []
        for s in books:
            _, series, title, blurb, time, level, lang = BOOKS[s]
            n, unit = page_count(s)
            la, words = LANGS[lang]
            text = html.escape(" ".join([series, title, blurb, name, level, la, words]).lower(), quote=True)
            lt, dl = lang_attr(s), f' data-lang="{lang}"' if lang != "en" else ""
            kick = f'<span class="kick"{lt}>{html.escape(series)}</span>' if series else ""
            facts = [f"{n} {unit if n != 1 else unit[:-1]}", time, f"{la}, {level}" if level else la]
            cards.append(f"""    <li data-text="{text}"><a href="{s}/{entry[s]}" data-slug="{s}"{dl}>{kick}<b{lt}>{html.escape(title)}</b>
      <span class="blurb"{lt}>{html.escape(blurb)}</span>
      <span class="facts">{"".join(f"<span>{html.escape(f)}</span>" for f in facts)}</span></a></li>""")
        secs.append(f"""<section class="cat acc-{acc}" data-cat="{key}" aria-labelledby="cat-{key}">
  <h2 class="cat-head" id="cat-{key}">{html.escape(name)} <span class="n">{len(books)}</span></h2>
  <p class="cat-note">{html.escape(note)}</p>
  <ul class="cards">
{chr(10).join(cards)}
  </ul>
</section>""")
    return f"""<header class="page-head shelf-head">
<div class="intro">
  <h1>Bookshelf</h1>
  <p class="lead">Readers I made for my own study.</p>
  <p class="meta"><span>{len(BOOKS)} readers</span><span>{total} pages</span><span>{" and ".join(LANGS[l][0] for l in LANGS if any(b[6] == l for b in BOOKS.values()))}</span></p>
</div>
{offline_box()}
</header>
<div class="recent" hidden>
  <h2 class="shelf-label">Continue reading</h2>
  <ol></ol>
</div>
<div class="shelf-tools">
  <input class="shelf-search" type="search" placeholder="Search readers" aria-label="Search readers">
  <div class="chips" role="group" aria-label="Categories">
    {(chr(10) + "    ").join(chips)}
  </div>
</div>
{chr(10).join(secs)}
<p class="no-hits" hidden>No readers match.</p>
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
