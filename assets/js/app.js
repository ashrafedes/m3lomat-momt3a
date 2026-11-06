(function () {
  "use strict";

  var chipsEl = document.getElementById("chips");
  var gridEl = document.getElementById("factsGrid");
  var searchEl = document.getElementById("searchInput");
  var countEl = document.getElementById("factCount");
  var emptyEl = document.getElementById("emptyMsg");
  var toastEl = document.getElementById("toast");

  var randomText = document.getElementById("randomText");
  var randomCat = document.getElementById("randomCat");
  var newFactBtn = document.getElementById("newFactBtn");
  var copyRandomBtn = document.getElementById("copyRandomBtn");

  var activeCategory = "all";
  var lastFactIndex = -1;
  var currentRandom = null;
  var toastTimer = null;

  // ---------- helpers ----------

  function catBadge(catKey) {
    var cat = CATEGORIES[catKey];
    var span = document.createElement("span");
    span.className = "fact-cat";
    span.textContent = cat.name;
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
        function () { showToast("تم النسخ"); },
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
    try { document.execCommand("copy"); showToast("تم النسخ"); }
    catch (e) { showToast("تعذر النسخ"); }
    document.body.removeChild(ta);
  }

  // ---------- category chips ----------

  function buildChips() {
    var allBtn = document.createElement("button");
    allBtn.className = "chip active";
    allBtn.dataset.cat = "all";
    allBtn.textContent = "الكل";
    chipsEl.appendChild(allBtn);

    Object.keys(CATEGORIES).forEach(function (key) {
      var btn = document.createElement("button");
      btn.className = "chip";
      btn.dataset.cat = key;
      btn.textContent = CATEGORIES[key].name;
      chipsEl.appendChild(btn);
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
  }

  // ---------- facts grid ----------

  function filteredFacts() {
    var q = searchEl.value.trim();
    return FACTS.filter(function (f) {
      var matchCat = activeCategory === "all" || f.c === activeCategory;
      var matchSearch = q === "" || f.t.indexOf(q) !== -1;
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
      p.textContent = f.t;

      var foot = document.createElement("div");
      foot.className = "card-foot";

      var copyBtn = document.createElement("button");
      copyBtn.className = "btn ghost sm";
      copyBtn.textContent = "نسخ";
      copyBtn.addEventListener("click", function () {
        copyText("هل تعلم؟ " + f.t);
      });

      foot.appendChild(copyBtn);
      card.appendChild(badge);
      card.appendChild(p);
      card.appendChild(foot);
      gridEl.appendChild(card);
    });

    countEl.textContent = list.length + " معلومة";
    emptyEl.hidden = list.length !== 0;
  }

  // ---------- random fact ----------

  function showRandomFact() {
    if (FACTS.length === 0) return;
    var idx;
    do {
      idx = Math.floor(Math.random() * FACTS.length);
    } while (idx === lastFactIndex && FACTS.length > 1);
    lastFactIndex = idx;

    var f = FACTS[idx];
    currentRandom = f;

    var card = document.getElementById("randomCard");
    card.style.animation = "none";
    void card.offsetWidth; // reflow to restart animation
    card.style.animation = "";

    randomText.textContent = f.t;
    randomCat.textContent = CATEGORIES[f.c].name;
    var color = CATEGORIES[f.c].color;
    randomCat.style.background = color + "22";
    randomCat.style.borderColor = color + "55";
    randomCat.style.color = color;
  }

  // ---------- events ----------

  newFactBtn.addEventListener("click", showRandomFact);

  copyRandomBtn.addEventListener("click", function () {
    if (currentRandom) copyText("هل تعلم؟ " + currentRandom.t);
    else showToast("اكتشف معلومة أولًا");
  });

  var debounce;
  searchEl.addEventListener("input", function () {
    clearTimeout(debounce);
    debounce = setTimeout(renderGrid, 150);
  });

  // ---------- init ----------

  buildChips();
  renderGrid();
  showRandomFact();
})();
