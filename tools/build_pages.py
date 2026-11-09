# Generate static crawlable pages: facts.html and videos.html
# Usage: python tools/build_pages.py
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_videos import categorize, CAT_INFO

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FACT_ORDER = ["space", "science", "animals", "human", "history", "tech", "nature", "geo"]
VIDEO_ORDER = ["food", "health", "news", "facts", "tech", "religion", "animals", "home", "money", "misc"]

HEAD = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://m3lomat-momt3a.org/{page}">
  <link rel="icon" href="assets/img/logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css">
  <script async src="https://www.googletagmanager.com/gtm.js?id=GTM-MXFQBXXJ"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
  </script>
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <a href="index.html" class="logo">
        <img class="logo-mark" src="assets/img/logo.png" alt="معلومات ممتعة">
        <span>معلومات <strong>ممتعة</strong></span>
      </a>
      <nav class="nav">
        <a href="index.html#random"><span class="ar-only">هل تعلم؟</span><span class="en-only">Did You Know?</span></a>
        <a href="videos.html"><span class="ar-only">فيديوهات</span><span class="en-only">Videos</span></a>
        <a href="articles.html"><span class="ar-only">مقالات</span><span class="en-only">Articles</span></a>
        <a href="books.html"><span class="ar-only">كتب</span><span class="en-only">Books</span></a>
        <a href="facts.html"><span class="ar-only">المعلومات</span><span class="en-only">Facts</span></a>
      </nav>
      <a class="btn yt sm" href="https://www.youtube.com/@m3lomat-momt3a?sub_confirmation=1" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8zM9.6 15.6V8.4L15.8 12z"/></svg>
        اشترك
      </a>
      <button class="lang-btn" id="langBtn" onclick="toggleLang()">EN</button>
    </div>
  </header>
  <main>
"""

FOOT = """  </main>
  <footer class="site-footer">
    <div class="container footer-inner">
      <p>معلومات ممتعة — m3lomat-momt3a.org</p>
      <p class="muted">تابعنا على يوتيوب لكل جديد</p>
    </div>
  </footer>
  <script>
    function applyLang(l) {
      var h = document.documentElement;
      h.dataset.lang = l; h.lang = l; h.dir = (l === "en") ? "ltr" : "rtl";
      var b = document.getElementById("langBtn");
      if (b) b.textContent = (l === "en") ? "عربي" : "EN";
      document.querySelectorAll('a[href="books.html"], a[href="books-en.html"]').forEach(function (x) {
        x.href = (l === "en") ? "books-en.html" : "books.html";
      });
    }
    function toggleLang() {
      var l = (document.documentElement.dataset.lang === "en") ? "ar" : "en";
      try { localStorage.setItem("lang", l); } catch (e) {}
      applyLang(l);
    }
    var _l = "ar";
    try { _l = localStorage.getItem("lang") || "ar"; } catch (e) {}
    applyLang(_l);
  </script>
</body>
</html>
"""


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def parse_facts():
    src = open(os.path.join(ROOT, "assets/js/facts.js"), encoding="utf-8").read()
    cats = {k: (ar, en, color) for k, ar, en, color in re.findall(
        r'(\w+):\s*\{ name: "([^"]+)",\s*en: "([^"]+)",\s*color: "([^"]+)"', src)}
    facts = re.findall(r'\{ t: "((?:[^"\\]|\\.)*)", e: "((?:[^"\\]|\\.)*)", c: "(\w+)" \}', src)
    return cats, [(t.replace('\\"', '"'), e.replace('\\"', '"'), c) for t, e, c in facts]


def build_facts_page():
    cats, facts = parse_facts()
    by_cat = {k: [] for k in FACT_ORDER}
    for t, e, c in facts:
        by_cat.setdefault(c, []).append((t, e))

    out = [HEAD.format(
        title="مكتبة المعلومات | معلومات ممتعة — حقائق ومقالات",
        desc="مكتبة معلومات ممتعة: حقائق ومقالات قصيرة في الفضاء والعلوم والحيوانات وجسم الإنسان والتاريخ والتقنية والطبيعة والجغرافيا.",
        page="facts.html")]
    out.append("""    <section class="library">
      <div class="container">
        <h1><span class="ar-only">مكتبة المعلومات</span><span class="en-only">Knowledge Library</span></h1>
        <p class="page-sub"><span class="ar-only">مقالات قصيرة وحقائق منتقاة من قناة معلومات ممتعة — مقسمة حسب الموضوع.</span><span class="en-only">Short articles and curated facts from the M3lomat Momt3a channel — sorted by topic.</span></p>
        <nav class="chips cat-index">
""")
    for key in FACT_ORDER:
        items = by_cat.get(key)
        if not items:
            continue
        ar, en, _ = cats[key]
        out.append(f'          <a class="chip" href="#{key}"><span class="ar-only">{ar}</span><span class="en-only">{en}</span> ({len(items)})</a>\n')
    out.append("        </nav>\n")
    for key in FACT_ORDER:
        items = by_cat.get(key)
        if not items:
            continue
        ar, en, color = cats[key]
        out.append(f'        <h2 id="{key}" style="color:{color}"><span class="ar-only">{ar}</span> <span class="en-only">{en}</span></h2>\n')
        out.append('        <div class="grid">\n')
        for t, e in items:
            out.append(
                f'          <article class="fact-card">\n'
                f'            <p class="fact-text ar-only" lang="ar">{esc(t)}</p>\n'
                f'            <p class="fact-text en-only" lang="en" dir="ltr">{esc(e)}</p>\n'
                f'          </article>\n')
        out.append("        </div>\n")
    out.append("      </div>\n    </section>\n")
    out.append(FOOT)
    open(os.path.join(ROOT, "facts.html"), "w", encoding="utf-8").write("".join(out))
    print("facts.html:", sum(len(v) for v in by_cat.values()), "facts")


def build_videos_page():
    data = json.load(open(os.path.join(ROOT, "channel.json"), encoding="utf-8"))
    entries = [e for e in data.get("entries", []) if e and e.get("id")]
    by_cat = {k: [] for k in VIDEO_ORDER}
    for e in entries:
        title = (e.get("title") or "").strip() or "فيديو"
        if "challenges.cloudflare.com" in title:
            continue
        by_cat.setdefault(categorize(title), []).append((e["id"], title))

    out = [HEAD.format(
        title="كل الفيديوهات | معلومات ممتعة — Fun Facts",
        desc="جميع فيديوهات قناة معلومات ممتعة على يوتيوب مصنفة حسب الموضوع: وصفات، صحة، أخبار، قصص، أجهزة، دين، حيوانات، مال وأعمال.",
        page="videos.html")]
    total = sum(len(v) for v in by_cat.values())
    out.append(f"""    <section class="videos">
      <div class="container">
        <h1><span class="ar-only">كل فيديوهات القناة</span><span class="en-only">All Channel Videos</span> <span class="count">({total})</span></h1>
        <p class="page-sub"><span class="ar-only">جميع فيديوهات قناة <a href="https://www.youtube.com/@m3lomat-momt3a" rel="noopener">معلومات ممتعة</a> على يوتيوب — مصنفة حسب الموضوع.</span><span class="en-only">All videos from the <a href="https://www.youtube.com/@m3lomat-momt3a" rel="noopener">M3lomat Momt3a</a> YouTube channel — sorted by topic.</span></p>
        <nav class="chips cat-index">
""")
    for key in VIDEO_ORDER:
        items = by_cat.get(key)
        if not items:
            continue
        ar, en = CAT_INFO[key]
        out.append(f'          <a class="chip" href="#{key}"><span class="ar-only">{ar}</span><span class="en-only">{en}</span> ({len(items)})</a>\n')
    out.append("        </nav>\n")
    for key in VIDEO_ORDER:
        items = by_cat.get(key)
        if not items:
            continue
        ar, en = CAT_INFO[key]
        out.append(f'        <h2 id="{key}"><span class="ar-only">{ar}</span> <span class="en-only">{en}</span> <span class="count">({len(items)})</span></h2>\n')
        out.append('        <div class="video-grid">\n')
        for vid, title in items:
            out.append(
                f'          <a class="video-card" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">\n'
                f'            <div class="thumb"><img loading="lazy" src="https://i.ytimg.com/vi/{vid}/mqdefault.jpg" alt="{esc(title)}"><span class="play">▶</span></div>\n'
                f'            <h3 dir="auto">{esc(title)}</h3>\n'
                f'          </a>\n')
        out.append("        </div>\n")
    out.append("      </div>\n    </section>\n")
    out.append(FOOT)
    open(os.path.join(ROOT, "videos.html"), "w", encoding="utf-8").write("".join(out))
    print("videos.html:", total, "videos")


ART_CAT_COLORS = {
    "space": "#8b5cf6", "science": "#22d3ee", "animals": "#34d399", "human": "#f472b6",
    "history": "#fbbf24", "tech": "#60a5fa", "nature": "#a3e635", "geo": "#fb923c",
}


def load_articles():
    src = open(os.path.join(ROOT, "assets/js/articles.js"), encoding="utf-8").read()
    m = re.search(r"const ARTICLES=(\[.*\]);?\s*$", src, re.S)
    return json.loads(m.group(1))


def load_videos_flat():
    src = open(os.path.join(ROOT, "assets/js/videos.js"), encoding="utf-8").read()
    return re.findall(r'\["([^"]+)","(\w+)","((?:[^"\\]|\\.)*)","[^"]*",\d+\]', src)


# article category -> video categories to pull related videos from
ART_VC = {
    "space": ["facts"], "science": ["facts", "tech"], "animals": ["animals"],
    "human": ["health"], "history": ["facts", "news"], "tech": ["tech"],
    "nature": ["animals", "misc"], "geo": ["facts", "news"],
}


def related_videos(a, vids):
    cats = ART_VC.get(a["c"], ["misc"])
    pool = [v for v in vids if v[1] in cats]
    return [pool[(a["i"] * 7 + k) % len(pool)] for k in range(min(5, len(pool)))]


def video_card(v):
    vid, _cat, title = v
    return (
        f'          <a class="video-card" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">\n'
        f'            <div class="thumb"><img loading="lazy" src="https://i.ytimg.com/vi/{vid}/mqdefault.jpg" alt="{esc(title)}"><span class="play">▶</span></div>\n'
        f'            <h3 dir="auto">{esc(title)}</h3>\n'
        f'          </a>\n')


def article_card(a, cats):
    ar, en, color = cats[a["c"]]
    return (
        f'          <a class="video-card" href="article-{a["i"]}.html">\n'
        f'            <div class="thumb"><img loading="lazy" src="{a["thumb"]}" alt="{esc(a["ta"])}"><span class="play" style="font-size:.9rem"><span class="ar-only">{ar}</span><span class="en-only">{en}</span></span></div>\n'
        f'            <h3 dir="auto"><span class="ar-only">{esc(a["ta"])}</span><span class="en-only">{esc(a["te"])}</span></h3>\n'
        f'          </a>\n')


def build_articles_pages(cats):
    articles = load_articles()
    vids = load_videos_flat()
    by_cat = {}
    for a in articles:
        by_cat.setdefault(a["c"], []).append(a)

    # ---- index page ----
    out = [HEAD.format(
        title="مقالات | معلومات ممتعة — Fun Facts Articles",
        desc="مقالات قصيرة ممتعة بالعربية والإنجليزية من قناة معلومات ممتعة: حقائق في الفضاء والعلوم والحيوانات وجسم الإنسان والتاريخ والتقنية.",
        page="articles.html")]
    out.append(f"""    <section class="videos">
      <div class="container">
        <h1><span class="ar-only">مقالات</span><span class="en-only">Articles</span> <span class="count">({len(articles)})</span></h1>
        <p class="page-sub"><span class="ar-only">مقالات قصيرة ممتعة بالعربية والإنجليزية — اضغط على أي مقال لقراءته كاملًا.</span><span class="en-only">Fun short articles in Arabic and English — click any article to read it in full.</span></p>
        <nav class="chips cat-index">
""")
    for key in FACT_ORDER:
        items = by_cat.get(key)
        if not items:
            continue
        ar, en, _ = cats[key]
        out.append(f'          <a class="chip" href="#{key}"><span class="ar-only">{ar}</span><span class="en-only">{en}</span> ({len(items)})</a>\n')
    out.append("        </nav>\n")
    for key in FACT_ORDER:
        items = by_cat.get(key)
        if not items:
            continue
        ar, en, _ = cats[key]
        out.append(f'        <h2 id="{key}"><span class="ar-only">{ar}</span> <span class="en-only">{en}</span> <span class="count">({len(items)})</span></h2>\n')
        out.append('        <div class="video-grid">\n')
        for a in items:
            out.append(article_card(a, cats))
        out.append("        </div>\n")
    out.append("      </div>\n    </section>\n")
    out.append(FOOT)
    open(os.path.join(ROOT, "articles.html"), "w", encoding="utf-8").write("".join(out))

    # ---- individual article pages ----
    for a in articles:
        ar, en, color = cats[a["c"]]
        related = [x for x in by_cat.get(a["c"], []) if x["i"] != a["i"]][:4]
        og_head = HEAD.format(
            title=f'{a["ta"]} | معلومات ممتعة',
            desc=a["ba"][:150],
            page=f'article-{a["i"]}.html')
        og_head = og_head.replace(
            '<link rel="icon"',
            f'  <meta property="og:type" content="article">\n'
            f'  <meta property="og:title" content="{esc(a["ta"])}">\n'
            f'  <meta property="og:image" content="{a["img"]}">\n'
            f'  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article",'
            f'"headline":"{esc(a["ta"])}","image":"{a["img"]}","inLanguage":["ar","en"],'
            f'"author":{{"@type":"Organization","name":"معلومات ممتعة | Fun Facts"}}}}</script>\n'
            '  <link rel="icon"')
        ar_paras = a.get("pa") or [a["ba"]]
        en_paras = a.get("pe") or [a["be"]]
        body_paras = "\n          ".join(
            f'<p class="article-body ar-only" lang="ar">{esc(p)}</p>' for p in ar_paras)
        body_paras += "\n          " + "\n          ".join(
            f'<p class="article-body en-only" lang="en" dir="ltr">{esc(p)}</p>' for p in en_paras)
        out = [og_head]
        out.append(f"""    <section class="library">
      <div class="container article-page">
        <nav class="breadcrumb"><a href="articles.html"><span class="ar-only">مقالات</span><span class="en-only">Articles</span></a> / <a href="articles.html#{a["c"]}" style="color:{color}"><span class="ar-only">{ar}</span><span class="en-only">{en}</span></a></nav>
        <article>
          <h1><span class="ar-only">{esc(a["ta"])}</span><span class="en-only">{esc(a["te"])}</span></h1>
          <p class="article-meta"><span class="fact-cat" style="background:{color}22;border-color:{color}55;color:{color}"><span class="ar-only">{ar}</span><span class="en-only">{en}</span></span></p>
          <img class="article-hero" src="{a["img"]}" alt="{esc(a["ta"])}" loading="lazy">
          <p class="credit">Photo: <a href="{a["phu"]}" target="_blank" rel="noopener">{esc(a["ph"])}</a> / Pexels</p>
          {body_paras}
        </article>
""")
        rv = related_videos(a, vids)
        if rv:
            out.append('        <h2><span class="ar-only">شوف كمان الفيديوهات دي</span><span class="en-only">Watch these videos too</span></h2>\n        <div class="video-grid">\n')
            for v in rv:
                out.append(video_card(v))
            out.append("        </div>\n")
        if related:
            out.append('        <h2><span class="ar-only">مقالات ذات صلة</span><span class="en-only">Related articles</span></h2>\n        <div class="video-grid">\n')
            for r in related:
                out.append(article_card(r, cats))
            out.append("        </div>\n")
        out.append("      </div>\n    </section>\n")
        out.append(FOOT)
        open(os.path.join(ROOT, f'article-{a["i"]}.html'), "w", encoding="utf-8").write("".join(out))

    print("articles:", len(articles), "pages")


if __name__ == "__main__":
    cats, _ = parse_facts()
    build_facts_page()
    build_videos_page()
    build_articles_pages(cats)
