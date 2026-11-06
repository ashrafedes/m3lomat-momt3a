# Regenerate assets/js/videos.js and the video entries in sitemap.xml
# Usage: python tools/build_videos.py   (needs channel.json from yt-dlp, or it fetches it)
import json, re, subprocess, os
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHANNEL = "https://www.youtube.com/@m3lomat-momt3a/videos"
DOMAIN = "https://m3lomat-momt3a.org"

# category key -> (Arabic name, English name, keywords) — first match wins
CATS = [
    ("food", "وصفات وأكل", "Food & Recipes",
     "مسقع وصفة طبخ طبخة اكل أكل أكلة طعم لحم لحمة فراخ دجاج تونة باذنج صلص شوربة حلو حلويات مكرون معكرونة كشري رقاق محشي محش كناف قهوة عصير شاي بيتزا برجر برغر سندوتش شاورما مطبخ فطار عشا معجنات كيك تورتة بسبوسة مهلبية طماطم بطاطس جبن جبنة مشوي مقلي شواء تتبيلة خضار فواكه فاكهة تفاح موز مانجو فراولة خيار جزر بصل ثوم بهارات توابل زيت سمن زبدة عسل لبن حليب زبادي أرز خبز دقيق سكر ملح مشروب وجبة شيف طباخ recipe food cook chips petit chocolate cake kitchen grill"),
    ("health", "صحة وجسمك", "Health & Body",
     "جسم صحة صحتك دم قلب أسنان اسنان لثة teeth gums skin بشرة شعر دواء مرض حبوب شطة عضل نوم نحافة وزن رجيم دايت فيتامين عظام مخ دماغ أعصاب سعال برد انفلونزا ضغط سكر سكري كولسترول كبد كلى معدة قولون هضم رئتين تنفس عيون نظر سمع وجع ألم التهاب حساسية مناعة عطس صداع طبيب علاج أعراض اعراض علامات حامل حمل جنين تكيس مبايض رحم جدري نزيف انف أنف تخسيس تجميل دوخة دوار غثيان درقية غدة نفسية اكتئاب حزن كاحل صدفية يأس إيدز ايدز لقاح تطعيم تشققات نزلات فيروس بكتيريا جرثومة امعاء أمعاء تطويل القامة النمو طول"),
    ("religion", "دين وعبادة", "Faith",
     "دعاء دعوة النبي رسول سنن مسلم مسلمين مسلمون صيام صيامه صوم حكم أحكام فقه عاشوراء صلاة صلاه الفجر المغرب العشاء قرآن آية سورة ذكر أذكار استغفار تسبيح إسلام اسلام اسلامية مكة الكعبة مسجد جمعة عبادة حرام حلال رمضان"),
    ("home", "بيت وتنظيم", "Home & Hacks",
     "منزل بيت صرصار صراصير حشرة حشرات ناموس ذباب نملة تنظيف نظافة غسيل بقع ثلاجة فريزر حائط أثاث اثاث ديكور ستارة ترتيب تنظيم روائح مبخرة تسرب سباكة صيانة نباتات منزلية زراعة خدعة حيلة طريقة تنظيم"),
    ("tech", "أجهزة وتطبيقات", "Tech & Apps",
     "مراجعة review ninja جهاز منتج product تطبيق app apk برنامج هاتف موبايل ساعة ايفون سامسونج ai ذكاء روبوت تقنية تكنولوجيا كمبيوتر لابتوب شاشة بلايستيشن petty water quality monitoring wifi انترنت إنترنت سوفتوير تحديث ويندوز أندرويد اندرويد طابعة كاميرا سماعة سماعات مضخة usb شاحن بطارية تلفزيون تليفزيون رسيفر درون سكوتر"),
    ("animals", "حيوانات وأطفال", "Animals & Kids",
     "حيوان حيوانات قط قطط كلب كلاب أسد نمر زرافة فيل elephant giraffe animal cat dog طيور طائر عصفور بومة بطريق دولفين حوت ثعبان افعى أفعى عقرب عنكبوت نحل فراشة سمك قرش أطفال اطفال kids baby children tom talking farm مزرعة حديقة حيوان zoo ludo لعبة العاب ألعاب game توم دب ارنب أرنب حصان غزال تمساح"),
    ("money", "مال وأعمال", "Money & Business",
     "مال فلوس استثمار ربح تسويق business invest money حرية مالية شركة شركتك مشروع أسهم بورصة دخل وظيفة فريلانس بزنس ادخار ديون بنك مبيعات عملاء أرباح"),
    ("news", "أخبار ورياضة", "News & Sports",
     "أخبار خبر ترامب trump news سياسة سياسية سياسي حكومة انتخابات رئيس رئاسة وزير وزارة مصر مصرية سيناء المتحف الإمارات امارات دبي السعودية الكويت قطر غزة فلسطين إسرائيل اسرائيل أوكرانيا روسيا الصين أمريكا امريكا امريكية ديمقراطية ماغا تشيني رياضة رياضية رياضي مباراة كورة كرة القدم الدوري منتخب نادي هدف جون مونديال كأس football nike mascot kit eagles bayern أولمبياد سباق جائزة دراسي مدارس امتحانات تنسيق الثانوية شم النسيم العيد عيد مواصلات مترو شواطئ عاصفة فيضان فيضانات طقس مناخ حفل مهرجان فعاليات حفلات موعد أسعار الدولار البنزين الذهب عاجل نتائج سيارات نيسان لامبورجيني فولكس"),
    ("facts", "قصص ومعرفة", "Stories & Facts",
     "قصة story تاريخ حرب ملك ملكة إمبراطور أسطورة غموض لغز حقيقة حقائق اكتشاف علم علمي فضاء زمن قديم فرعون أهرام هرم حضارة سر أسرار غريب عجيب أخطر أغرب أقوى أكبر أطول ماذا لماذا ليه إزاي ازاي كيف هل تعلم bhopal drug lords japanese giza world العالم دولة مدينة جبل نهر بحر محيط كوكب نجوم زلزال بركان ظاهرة"),
]
MISC = ("misc", "متنوع", "More")
KW = [(key, kws.split()) for key, ar, en, kws in CATS]
CAT_INFO = {k: (ar, en) for k, ar, en, _ in CATS}
CAT_INFO[MISC[0]] = (MISC[1], MISC[2])

def categorize(title):
    low = " " + (title or "").lower() + " "
    for key, words in KW:
        for w in words:
            if w in low:
                return key
    return "misc"

def main():
    src = os.path.join(ROOT, "channel.json")
    if not os.path.exists(src):
        print("fetching channel data...")
        out = subprocess.run(
            ["python", "-m", "yt_dlp", "--flat-playlist", "--dump-single-json", CHANNEL],
            capture_output=True, text=True, encoding="utf-8")
        open(src, "w", encoding="utf-8").write(out.stdout)
    data = json.load(open(src, encoding="utf-8"))
    entries = [e for e in data.get("entries", []) if e and e.get("id")]

    videos = []
    for e in entries:
        title = (e.get("title") or "").strip() or "فيديو"
        if "challenges.cloudflare.com" in title:
            continue
        cat = categorize(title)
        ts = e.get("timestamp")
        date = datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d") if ts else ""
        dur = e.get("duration") or 0
        videos.append([e["id"], cat, title, date, int(dur)])

    counts = {}
    for v in videos:
        counts[v[1]] = counts.get(v[1], 0) + 1
    print("total:", len(videos), counts)

    # videos.js
    cats_js = "{" + ",".join(
        f'"{k}":{{"name":"{ar}","en":"{en}"}}' for k, (ar, en) in CAT_INFO.items()) + "}"
    lines = ["// Generated by tools/build_videos.py — do not edit by hand",
             f"const VIDEO_CATS={cats_js};",
             "// [id, category, title, date(YYYY-MM-DD), duration(sec)]",
             "const VIDEOS=["]
    for v in videos:
        title = v[2].replace("\\", "\\\\").replace('"', '\\"')
        lines.append(f'["{v[0]}","{v[1]}","{title}","{v[3]}",{v[4]}],')
    lines.append("];")
    open(os.path.join(ROOT, "assets/js/videos.js"), "w", encoding="utf-8").write("\n".join(lines) + "\n")

    # sitemap.xml with video entries
    esc = lambda s: (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                     .replace('"', "&quot;").replace("'", "&apos;"))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
          '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"',
          '        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">',
          "  <url>",
          f"    <loc>{DOMAIN}/</loc>",
          f"    <lastmod>{datetime.now(timezone.utc).strftime('%Y-%m-%d')}</lastmod>",
          "    <changefreq>weekly</changefreq>",
          "    <priority>1.0</priority>",
          "    <image:image>",
          "      <image:loc>https://i.ytimg.com/vi/luMka87efig/hqdefault.jpg</image:loc>",
          "      <image:title>معلومات ممتعة | Fun Facts</image:title>",
          "    </image:image>"]
    for vid, cat, title, date, dur in videos:
        cat_ar, cat_en = CAT_INFO[cat]
        sm += ["    <video:video>",
               f"      <video:thumbnail_loc>https://i.ytimg.com/vi/{vid}/mqdefault.jpg</video:thumbnail_loc>",
               f"      <video:title>{esc(title)}</video:title>",
               f"      <video:description>{esc(title)}</video:description>",
               f"      <video:player_loc>https://www.youtube.com/embed/{vid}</video:player_loc>",
               '      <video:uploader info="https://www.youtube.com/@m3lomat-momt3a">معلومات ممتعة | Fun Facts</video:uploader>']
        if date:
            sm.append(f"      <video:publication_date>{date}</video:publication_date>")
        if dur:
            sm.append(f"      <video:duration>{dur}</video:duration>")
        sm += [f"      <video:category>{esc(cat_en)}</video:category>",
               f"      <video:tag>{esc(cat_en)}</video:tag>",
               f"      <video:tag>{esc(cat_ar)}</video:tag>",
               "      <video:tag>معلومات ممتعة</video:tag>",
               "    </video:video>"]
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    sm += ["  </url>",
           "  <url>",
           f"    <loc>{DOMAIN}/videos.html</loc>",
           f"    <lastmod>{today}</lastmod>",
           "    <changefreq>weekly</changefreq>",
           "    <priority>0.9</priority>",
           "  </url>",
           "  <url>",
           f"    <loc>{DOMAIN}/articles.html</loc>",
           f"    <lastmod>{today}</lastmod>",
           "    <changefreq>monthly</changefreq>",
           "    <priority>0.8</priority>",
           "  </url>",
           "  <url>",
           f"    <loc>{DOMAIN}/facts.html</loc>",
           "    <changefreq>monthly</changefreq>",
           "    <priority>0.8</priority>",
           "  </url>",
           "  <url>",
           f"    <loc>{DOMAIN}/books.html</loc>",
           "    <changefreq>monthly</changefreq>",
           "    <priority>0.7</priority>",
           "  </url>",
           "  <url>",
           f"    <loc>{DOMAIN}/books-en.html</loc>",
           "    <changefreq>monthly</changefreq>",
           "    <priority>0.7</priority>",
           f"    <lastmod>{today}</lastmod>",
           "    <changefreq>monthly</changefreq>",
           "    <priority>0.8</priority>",
           "  </url>"]
    # individual article pages (with hero image per page)
    art_src = os.path.join(ROOT, "assets/js/articles.js")
    if os.path.exists(art_src):
        raw = open(art_src, encoding="utf-8").read()
        arts = json.loads(re.search(r"const ARTICLES=(\[.*\]);?\s*$", raw, re.S).group(1))
        for a in arts:
            sm += ["  <url>",
                   f"    <loc>{DOMAIN}/article-{a['i']}.html</loc>",
                   f"    <lastmod>{today}</lastmod>",
                   "    <changefreq>monthly</changefreq>",
                   "    <priority>0.6</priority>",
                   "    <image:image>",
                   f"      <image:loc>{esc(a['img'])}</image:loc>",
                   f"      <image:title>{esc(a['ta'])}</image:title>",
                   "    </image:image>",
                   "  </url>"]
    sm += ["</urlset>", ""]
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm))

if __name__ == "__main__":
    main()
