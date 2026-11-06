(function () {
  "use strict";

  // ---------- i18n ----------

  var I18N = {
    ar: {
      title: "معلومات ممتعة | Fun Facts — هل تعلم؟ حقائق وفيديوهات ممتعة",
      nav_dyak: "هل تعلم؟",
      nav_videos: "فيديوهات",
      nav_facts: "المعلومات",
      subscribe: "اشترك",
      hero_1: "معلومات",
      hero_2: "ممتعة",
      hero_3: "تجعلك أذكى كل يوم",
      hero_sub: "الموقع الرسمي لقناة معلومات ممتعة على يوتيوب — أغرب وأطرف الحقائق في العلوم والفضاء والحيوانات والتاريخ والتقنية.",
      random_hint: "اضغط الزر لاكتشاف معلومة جديدة",
      new_fact: "معلومة جديدة",
      copy: "نسخ",
      videos_head: "فيديوهات القناة",
      all_videos: "كل الفيديوهات على يوتيوب",
      video_search_ph: "ابحث في الفيديوهات…",
      load_more: "عرض المزيد",
      videos_n: "فيديو",
      subscribe_banner: "شاهد المزيد من المعلومات الممتعة على قناتنا",
      subscribe_cta: "اشترك في القناة",
      library_head: "مكتبة المعلومات",
      search_ph: "ابحث عن معلومة…",
      all: "الكل",
      facts_n: "معلومة",
      empty: "لا توجد نتائج مطابقة لبحثك.",
      footer_1: "معلومات ممتعة — m3lomat-momt3a.org",
      footer_2: "تابعنا على يوتيوب لكل جديد — شارك المعرفة مع أصدقائك",
      copied: "تم النسخ",
      copy_fail: "تعذر النسخ",
      discover_first: "اكتشف معلومة أولًا",
      dyk: "هل تعلم؟ ",
      nav_articles: "مقالات",
      articles_head: "مقالات ممتعة",
      articles_n: "مقال",
      article_search_ph: "ابحث في المقالات…",
      read_more: "اقرأ المقال",
      photo_by: "الصورة:",
      see_also: "شوف كمان الفيديوهات دي",
      vlinks_head: "أحدث فيديوهات القناة"
    },
    en: {
      title: "Fun Facts | M3lomat Momt3a — Did You Know?",
      nav_dyak: "Did You Know?",
      nav_videos: "Videos",
      nav_facts: "Facts",
      subscribe: "Subscribe",
      hero_1: "Fun",
      hero_2: "Facts",
      hero_3: "to make you smarter every day",
      hero_sub: "The official site of the Fun Facts YouTube channel — the strangest and coolest facts in science, space, animals, history and tech.",
      random_hint: "Press the button to discover a new fact",
      new_fact: "New fact",
      copy: "Copy",
      videos_head: "Channel videos",
      all_videos: "All videos on YouTube",
      video_search_ph: "Search videos…",
      load_more: "Load more",
      videos_n: "videos",
      subscribe_banner: "Watch more fun facts on our channel",
      subscribe_cta: "Subscribe to the channel",
      library_head: "Facts Library",
      search_ph: "Search facts…",
      all: "All",
      facts_n: "facts",
      empty: "No results match your search.",
      footer_1: "Fun Facts — m3lomat-momt3a.org",
      footer_2: "Follow us on YouTube — share knowledge with your friends",
      copied: "Copied",
      copy_fail: "Copy failed",
      discover_first: "Discover a fact first",
      dyk: "Did you know? ",
      nav_articles: "Articles",
      articles_head: "Fun Articles",
      articles_n: "articles",
      article_search_ph: "Search articles…",
      read_more: "Read article",
      photo_by: "Photo:",
      see_also: "See also these videos",
      vlinks_head: "Latest channel videos"
    }
  };

  var lang = localStorage.getItem("lang") === "en" ? "en" : "ar";

  var chipsEl = document.getElementById("chips");
  var gridEl = document.getElementById("factsGrid");
  var searchEl = document.getElementById("searchInput");
  var countEl = document.getElementById("factCount");
  var emptyEl = document.getElementById("emptyMsg");
  var toastEl = document.getElementById("toast");
  var langBtn = document.getElementById("langBtn");

  var randomText = document.getElementById("randomText");
  var randomCat = document.getElementById("randomCat");
  var newFactBtn = document.getElementById("newFactBtn");
  var copyRandomBtn = document.getElementById("copyRandomBtn");

  var activeCategory = "all";
  var lastFactIndex = -1;
  var currentRandom = null;
  var toastTimer = null;

  function t(key) { return I18N[lang][key]; }

  function factText(f) { return lang === "en" && f.e ? f.e : f.t; }
  function catName(key) { return lang === "en" ? CATEGORIES[key].en : CATEGORIES[key].name; }

  // ---------- helpers ----------

  function catBadge(catKey) {
    var cat = CATEGORIES[catKey];
    var span = document.createElement("span");
    span.className = "fact-cat";
    span.textContent = catName(catKey);
    span.style.background = cat.color + "22";
    span.style.borderColor = cat.color + "55";
    span.style.color = cat.color;
    return span;
  }

  function showToast(msg) {
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      toastEl.classList.remove("show");
    }, 1800);
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(
        function () { showToast(t("copied")); },
        function () { fallbackCopy(text); }
      );
    } else {
      fallbackCopy(text);
    }
  }

  function fallbackCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); showToast(t("copied")); }
    catch (e) { showToast(t("copy_fail")); }
    document.body.removeChild(ta);
  }

  // ---------- static text ----------

  function applyI18n() {
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
    document.title = t("title");

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      if (I18N[lang][key] !== undefined) el.textContent = I18N[lang][key];
    });
    document.querySelectorAll("[data-i18n-ph]").forEach(function (el) {
      var key = el.getAttribute("data-i18n-ph");
      if (I18N[lang][key] !== undefined) el.placeholder = I18N[lang][key];
    });
    document.querySelectorAll("[data-ar][data-en]").forEach(function (el) {
      el.textContent = el.getAttribute("data-" + lang);
    });

    langBtn.textContent = lang === "ar" ? "EN" : "عربي";
    langBtn.setAttribute("aria-label", lang === "ar" ? "Switch to English" : "التبديل إلى العربية");
  }

  // ---------- category chips ----------

  function buildChips() {
    chipsEl.innerHTML = "";

    var allBtn = document.createElement("button");
    allBtn.className = "chip" + (activeCategory === "all" ? " active" : "");
    allBtn.dataset.cat = "all";
    allBtn.textContent = t("all");
    chipsEl.appendChild(allBtn);

    Object.keys(CATEGORIES).forEach(function (key) {
      var btn = document.createElement("button");
      btn.className = "chip" + (activeCategory === key ? " active" : "");
      btn.dataset.cat = key;
      btn.textContent = catName(key);
      chipsEl.appendChild(btn);
    });
  }

  // ---------- facts grid ----------

  function filteredFacts() {
    var q = searchEl.value.trim().toLowerCase();
    return FACTS.filter(function (f) {
      var matchCat = activeCategory === "all" || f.c === activeCategory;
      var matchSearch = q === "" ||
        f.t.indexOf(q) !== -1 ||
        (f.e && f.e.toLowerCase().indexOf(q) !== -1);
      return matchCat && matchSearch;
    });
  }

  function renderGrid() {
    var list = filteredFacts();
    gridEl.innerHTML = "";

    list.forEach(function (f) {
      var card = document.createElement("article");
      card.className = "fact-card";

      var badge = catBadge(f.c);
      var p = document.createElement("p");
      p.className = "fact-text";
      p.textContent = factText(f);

      var foot = document.createElement("div");
      foot.className = "card-foot";

      var copyBtn = document.createElement("button");
      copyBtn.className = "btn ghost sm";
      copyBtn.textContent = t("copy");
      copyBtn.addEventListener("click", function () {
        copyText(t("dyk") + factText(f));
      });

      foot.appendChild(copyBtn);
      card.appendChild(badge);
      card.appendChild(p);
      card.appendChild(foot);
      gridEl.appendChild(card);
    });

    countEl.textContent = list.length + " " + t("facts_n");
    emptyEl.hidden = list.length !== 0;
  }

  // ---------- random fact ----------

  function paintRandom() {
    if (!currentRandom) {
      randomText.textContent = t("random_hint");
      randomCat.textContent = "—";
      return;
    }
    randomText.textContent = factText(currentRandom);
    randomCat.textContent = catName(currentRandom.c);
    var color = CATEGORIES[currentRandom.c].color;
    randomCat.style.background = color + "22";
    randomCat.style.borderColor = color + "55";
    randomCat.style.color = color;
  }

  function showRandomFact() {
    if (FACTS.length === 0) return;
    var idx;
    do {
      idx = Math.floor(Math.random() * FACTS.length);
    } while (idx === lastFactIndex && FACTS.length > 1);
    lastFactIndex = idx;
    currentRandom = FACTS[idx];

    var card = document.getElementById("randomCard");
    card.style.animation = "none";
    void card.offsetWidth; // reflow to restart animation
    card.style.animation = "";

    paintRandom();
  }

  // ---------- videos ----------

  var PAGE = 24;
  var videoChipsEl = document.getElementById("videoChips");
  var videoGridEl = document.getElementById("videoGrid");
  var videoSearchEl = document.getElementById("videoSearch");
  var videoCountEl = document.getElementById("videoCount");
  var videoEmptyEl = document.getElementById("videoEmpty");
  var loadMoreWrap = document.getElementById("loadMoreWrap");
  var loadMoreBtn = document.getElementById("loadMoreBtn");

  var videoCat = "all";
  var renderedCount = 0;

  function vcatName(key) {
    return lang === "en" ? VIDEO_CATS[key].en : VIDEO_CATS[key].name;
  }

  function buildVideoChips() {
    videoChipsEl.innerHTML = "";
    var allBtn = document.createElement("button");
    allBtn.className = "chip" + (videoCat === "all" ? " active" : "");
    allBtn.dataset.cat = "all";
    allBtn.textContent = t("all");
    videoChipsEl.appendChild(allBtn);

    Object.keys(VIDEO_CATS).forEach(function (key) {
      var btn = document.createElement("button");
      btn.className = "chip" + (videoCat === key ? " active" : "");
      btn.dataset.cat = key;
      btn.textContent = vcatName(key);
      videoChipsEl.appendChild(btn);
    });
  }

  function filteredVideos() {
    var q = videoSearchEl.value.trim().toLowerCase();
    return VIDEOS.filter(function (v) {
      var matchCat = videoCat === "all" || v[1] === videoCat;
      var matchSearch = q === "" || v[2].toLowerCase().indexOf(q) !== -1;
      return matchCat && matchSearch;
    });
  }

  function embedVideo(card, id) {
    if (card.classList.contains("playing")) return;
    card.classList.add("playing");
    var thumb = card.querySelector(".thumb");
    thumb.innerHTML = "";
    var iframe = document.createElement("iframe");
    iframe.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
    iframe.allowFullscreen = true;
    thumb.appendChild(iframe);
  }

  function makeVideoCard(v) {
    var card = document.createElement("div");
    card.className = "video-card";

    var thumb = document.createElement("div");
    thumb.className = "thumb";
    var img = document.createElement("img");
    img.loading = "lazy";
    img.src = "https://i.ytimg.com/vi/" + v[0] + "/mqdefault.jpg";
    img.alt = v[2];
    var play = document.createElement("span");
    play.className = "play";
    play.textContent = "▶";
    thumb.appendChild(img);
    thumb.appendChild(play);

    var h3 = document.createElement("h3");
    h3.textContent = v[2];
    h3.dir = "auto";

    card.appendChild(thumb);
    card.appendChild(h3);
    card.addEventListener("click", function () { embedVideo(card, v[0]); });
    return card;
  }

  function renderVideos(reset) {
    var list = filteredVideos();
    if (reset) {
      videoGridEl.innerHTML = "";
      renderedCount = 0;
    }
    var end = Math.min(renderedCount + PAGE, list.length);
    for (var i = renderedCount; i < end; i++) {
      videoGridEl.appendChild(makeVideoCard(list[i]));
    }
    renderedCount = end;

    videoCountEl.textContent = "(" + list.length + " " + t("videos_n") + ")";
    videoEmptyEl.hidden = list.length !== 0;
    loadMoreWrap.style.display = renderedCount < list.length ? "" : "none";
  }

  // ---------- articles ----------

  var APAGE = 12;
  var articleChipsEl = document.getElementById("articleChips");
  var articleGridEl = document.getElementById("articleGrid");
  var articleSearchEl = document.getElementById("articleSearch");
  var articleCountEl = document.getElementById("articleCount");
  var articleEmptyEl = document.getElementById("articleEmpty");
  var articleLoadMoreWrap = document.getElementById("articleLoadMoreWrap");
  var articleLoadMoreBtn = document.getElementById("articleLoadMore");

  var modalEl = document.getElementById("articleModal");
  var modalImg = document.getElementById("modalImg");
  var modalCat = document.getElementById("modalCat");
  var modalTitle = document.getElementById("modalTitle");
  var modalText = document.getElementById("modalText");
  var modalCredit = document.getElementById("modalCredit");
  var articleCloseBtn = document.getElementById("articleClose");

  var articleCat = "all";
  var articleRendered = 0;

  function artTitle(a) { return lang === "en" && a.te ? a.te : a.ta; }
  function artBody(a) { return lang === "en" && a.be ? a.be : a.ba; }

  function buildArticleChips() {
    articleChipsEl.innerHTML = "";
    var allBtn = document.createElement("button");
    allBtn.className = "chip" + (articleCat === "all" ? " active" : "");
    allBtn.dataset.cat = "all";
    allBtn.textContent = t("all");
    articleChipsEl.appendChild(allBtn);

    Object.keys(CATEGORIES).forEach(function (key) {
      var btn = document.createElement("button");
      btn.className = "chip" + (articleCat === key ? " active" : "");
      btn.dataset.cat = key;
      btn.textContent = catName(key);
      articleChipsEl.appendChild(btn);
    });
  }

  function filteredArticles() {
    var q = articleSearchEl.value.trim().toLowerCase();
    return ARTICLES.filter(function (a) {
      var matchCat = articleCat === "all" || a.c === articleCat;
      var matchSearch = q === "" ||
        a.ta.indexOf(q) !== -1 || a.ba.indexOf(q) !== -1 ||
        (a.te && a.te.toLowerCase().indexOf(q) !== -1) ||
        (a.be && a.be.toLowerCase().indexOf(q) !== -1);
      return matchCat && matchSearch;
    });
  }

  var ART_VC = {
    space: ["facts"], science: ["facts", "tech"], animals: ["animals"],
    human: ["health"], history: ["facts", "news"], tech: ["tech"],
    nature: ["animals", "misc"], geo: ["facts", "news"]
  };

  var modalVideosEl = document.getElementById("modalVideos");

  function relatedVideos(a) {
    var cats = ART_VC[a.c] || ["misc"];
    var pool = VIDEOS.filter(function (v) { return cats.indexOf(v[1]) !== -1; });
    var picked = [];
    for (var k = 0; k < 5 && pool.length; k++) {
      picked.push(pool[(a.i * 7 + k) % pool.length]);
    }
    return picked;
  }

  function openArticle(a) {
    modalImg.src = a.img;
    modalImg.alt = artTitle(a);
    var cat = CATEGORIES[a.c];
    modalCat.textContent = catName(a.c);
    modalCat.style.background = cat.color + "22";
    modalCat.style.borderColor = cat.color + "55";
    modalCat.style.color = cat.color;
    modalTitle.textContent = artTitle(a);
    modalTitle.dir = "auto";

    var paras = (lang === "en" && a.pe ? a.pe : a.pa) || [artBody(a)];
    modalText.innerHTML = "";
    paras.forEach(function (t) {
      var p = document.createElement("p");
      p.className = "modal-text";
      p.textContent = t;
      p.dir = "auto";
      modalText.appendChild(p);
    });

    modalVideosEl.innerHTML = "";
    relatedVideos(a).forEach(function (v) {
      var wrap = document.createElement("div");
      wrap.className = "mv";
      var iframe = document.createElement("iframe");
      iframe.loading = "lazy";
      iframe.src = "https://www.youtube-nocookie.com/embed/" + v[0] + "?rel=0";
      iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
      iframe.allowFullscreen = true;
      iframe.title = v[2];
      var cap = document.createElement("div");
      cap.className = "mv-title";
      cap.textContent = v[2];
      cap.dir = "auto";
      wrap.appendChild(iframe);
      wrap.appendChild(cap);
      modalVideosEl.appendChild(wrap);
    });

    if (a.ph) {
      modalCredit.hidden = false;
      modalCredit.href = a.phu;
      modalCredit.textContent = t("photo_by") + " " + a.ph + " — Pexels";
    } else {
      modalCredit.hidden = true;
    }
    modalEl.hidden = false;
    document.body.style.overflow = "hidden";
  }

  function closeArticle() {
    modalEl.hidden = true;
    modalVideosEl.innerHTML = "";
    document.body.style.overflow = "";
  }

  function makeArticleCard(a) {
    var card = document.createElement("article");
    card.className = "article-card";

    var thumb = document.createElement("div");
    thumb.className = "thumb";
    var img = document.createElement("img");
    img.loading = "lazy";
    img.src = a.thumb || a.img;
    img.alt = artTitle(a);
    thumb.appendChild(img);

    var body = document.createElement("div");
    body.className = "card-body";
    body.appendChild(catBadge(a.c));

    var h3 = document.createElement("h3");
    h3.textContent = artTitle(a);
    h3.dir = "auto";

    var ex = document.createElement("p");
    ex.className = "excerpt";
    var b = artBody(a);
    ex.textContent = b.length > 110 ? b.slice(0, 110) + "…" : b;
    ex.dir = "auto";

    var foot = document.createElement("div");
    foot.className = "card-foot";
    var readBtn = document.createElement("button");
    readBtn.className = "btn ghost sm";
    readBtn.textContent = t("read_more");
    foot.appendChild(readBtn);

    body.appendChild(h3);
    body.appendChild(ex);
    body.appendChild(foot);
    card.appendChild(thumb);
    card.appendChild(body);
    card.addEventListener("click", function () { openArticle(a); });
    return card;
  }

  function renderArticles(reset) {
    var list = filteredArticles();
    if (reset) {
      articleGridEl.innerHTML = "";
      articleRendered = 0;
    }
    var end = Math.min(articleRendered + APAGE, list.length);
    for (var i = articleRendered; i < end; i++) {
      articleGridEl.appendChild(makeArticleCard(list[i]));
    }
    articleRendered = end;

    articleCountEl.textContent = "(" + list.length + " " + t("articles_n") + ")";
    articleEmptyEl.hidden = list.length !== 0;
    articleLoadMoreWrap.style.display = articleRendered < list.length ? "" : "none";
  }

  // ---------- video links ----------

  var VLINKS_N = 24;
  var vlinksEl = document.getElementById("videoLinks");
  var vlinkCountEl = document.getElementById("vlinkCount");

  function renderVideoLinks() {
    vlinksEl.innerHTML = "";
    var list = VIDEOS.slice(0, VLINKS_N);
    list.forEach(function (v) {
      var a = document.createElement("a");
      a.href = "https://www.youtube.com/watch?v=" + v[0];
      a.target = "_blank";
      a.rel = "noopener";
      a.dir = "auto";
      var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("viewBox", "0 0 24 24");
      svg.setAttribute("width", "18");
      svg.setAttribute("height", "18");
      svg.setAttribute("fill", "currentColor");
      var path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.setAttribute("d", "M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8zM9.6 15.6V8.4L15.8 12z");
      svg.appendChild(path);
      var span = document.createElement("span");
      span.textContent = v[2];
      a.appendChild(svg);
      a.appendChild(span);
      vlinksEl.appendChild(a);
    });
    vlinkCountEl.textContent = "(" + list.length + ")";
  }

  // ---------- events ----------

  newFactBtn.addEventListener("click", showRandomFact);

  copyRandomBtn.addEventListener("click", function () {
    if (currentRandom) copyText(t("dyk") + factText(currentRandom));
    else showToast(t("discover_first"));
  });

  chipsEl.addEventListener("click", function (e) {
    var btn = e.target.closest(".chip");
    if (!btn) return;
    activeCategory = btn.dataset.cat;
    chipsEl.querySelectorAll(".chip").forEach(function (c) {
      c.classList.toggle("active", c === btn);
    });
    renderGrid();
  });

  videoChipsEl.addEventListener("click", function (e) {
    var btn = e.target.closest(".chip");
    if (!btn) return;
    videoCat = btn.dataset.cat;
    videoChipsEl.querySelectorAll(".chip").forEach(function (c) {
      c.classList.toggle("active", c === btn);
    });
    renderVideos(true);
  });

  loadMoreBtn.addEventListener("click", function () { renderVideos(false); });

  articleChipsEl.addEventListener("click", function (e) {
    var btn = e.target.closest(".chip");
    if (!btn) return;
    articleCat = btn.dataset.cat;
    articleChipsEl.querySelectorAll(".chip").forEach(function (c) {
      c.classList.toggle("active", c === btn);
    });
    renderArticles(true);
  });

  articleLoadMoreBtn.addEventListener("click", function () { renderArticles(false); });

  var aDebounce;
  articleSearchEl.addEventListener("input", function () {
    clearTimeout(aDebounce);
    aDebounce = setTimeout(function () { renderArticles(true); }, 150);
  });

  articleCloseBtn.addEventListener("click", closeArticle);
  modalEl.addEventListener("click", function (e) {
    if (e.target === modalEl) closeArticle();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !modalEl.hidden) closeArticle();
  });

  var vDebounce;
  videoSearchEl.addEventListener("input", function () {
    clearTimeout(vDebounce);
    vDebounce = setTimeout(function () { renderVideos(true); }, 150);
  });

  langBtn.addEventListener("click", function () {
    lang = lang === "ar" ? "en" : "ar";
    localStorage.setItem("lang", lang);
    applyI18n();
    buildChips();
    buildVideoChips();
    buildArticleChips();
    renderGrid();
    renderVideos(true);
    renderArticles(true);
    renderVideoLinks();
    paintRandom();
  });

  var debounce;
  searchEl.addEventListener("input", function () {
    clearTimeout(debounce);
    debounce = setTimeout(renderGrid, 150);
  });

  // ---------- init ----------

  applyI18n();
  buildChips();
  buildVideoChips();
  buildArticleChips();
  renderGrid();
  renderVideos(true);
  renderArticles(true);
  renderVideoLinks();
  showRandomFact();
})();
