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
      videos_head: "أحدث فيديوهات القناة",
      all_videos: "كل الفيديوهات على يوتيوب",
      subscribe_banner: "شاهد المزيد من المعلومات الممتعة على قناتنا",
      subscribe_cta: "اشترك في القناة",
      library_head: "مكتبة المعلومات",
      search_ph: "ابحث عن معلومة…",
      all: "الكل",
      facts_n: "معلومة",
      empty: "لا توجد نتائج مطابقة لبحثك.",
      footer_1: "معلومات ممتعة — m3lomat-momt3a.bestsell.site",
      footer_2: "تابعنا على يوتيوب لكل جديد — شارك المعرفة مع أصدقائك",
      copied: "تم النسخ",
      copy_fail: "تعذر النسخ",
      discover_first: "اكتشف معلومة أولًا",
      dyk: "هل تعلم؟ "
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
      videos_head: "Latest channel videos",
      all_videos: "All videos on YouTube",
      subscribe_banner: "Watch more fun facts on our channel",
      subscribe_cta: "Subscribe to the channel",
      library_head: "Facts Library",
      search_ph: "Search facts…",
      all: "All",
      facts_n: "facts",
      empty: "No results match your search.",
      footer_1: "Fun Facts — m3lomat-momt3a.bestsell.site",
      footer_2: "Follow us on YouTube — share knowledge with your friends",
      copied: "Copied",
      copy_fail: "Copy failed",
      discover_first: "Discover a fact first",
      dyk: "Did you know? "
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

  langBtn.addEventListener("click", function () {
    lang = lang === "ar" ? "en" : "ar";
    localStorage.setItem("lang", lang);
    applyI18n();
    buildChips();
    renderGrid();
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
  renderGrid();
  showRandomFact();
})();
