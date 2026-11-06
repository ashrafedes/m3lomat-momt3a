# معلومات ممتعة — m3lomat-momt3a.org

الموقع الرسمي لقناة [معلومات ممتعة | Fun Facts](https://www.youtube.com/@m3lomat-momt3a) على يوتيوب — موقع ثابت (static) يعرض معلومات وحقائق ممتعة مصنّفة حسب الفئة، مع بحث وزر "معلومة جديدة" وأحدث فيديوهات القناة.

## الملفات

| الملف | الوصف |
|---|---|
| `index.html` | الصفحة الرئيسية (SEO meta + فيديوهات + مكتبة المعلومات) |
| `assets/css/style.css` | التنسيقات |
| `assets/js/facts.js` | بيانات المعلومات والتصنيفات — أضف معلومات جديدة هنا |
| `assets/js/app.js` | منطق الموقع (بحث، فلترة، نسخ، معلومة عشوائية، فيديوهات) |
| `assets/js/videos.js` | بيانات الفيديوهات — يتولّد تلقائيًا، لا تعدّله يدويًا |
| `tools/build_videos.py` | سكربت يجلب كل فيديوهات القناة (yt-dlp) ويولّد `videos.js` + `sitemap.xml` |
| `tools/build_pages.py` | يولّد الصفحات الثابتة `facts.html` و`videos.html` و`articles.html` وصفحات المقالات `article-N.html` |
| `robots.txt` / `sitemap.xml` | ملفات الـ SEO لـ Google Search Console |
| `render.yaml` | إعدادات النشر على Render |

## تحديث الفيديوهات

```bash
rm channel.json            # امسح الكاش القديم (أول مرة غير مطلوب)
python tools/build_videos.py
python tools/build_pages.py   # لتحديث الصفحات الثابتة أيضًا
git add -A && git commit -m "Update videos" && git push
```

## النشر على Render (مجاني)

1. ارفع الملفات إلى مستودع على GitHub.
2. في [Render Dashboard](https://dashboard.render.com):
   - **New → Static Site**
   - اربط مستودع GitHub
   - Build Command: اتركه فارغًا
   - Publish Directory: `.`
3. في **Settings → Custom Domains** أضف:
   `m3lomat-momt3a.org`
4. في DNS الخاص بالنطاق `m3lomat-momt3a.org` (Namecheap → Advanced DNS) أضف:
   ```
   A Record     @    →  216.24.57.1
   CNAME Record www  →  <your-service>.onrender.com
   ```
   Render يوفّر شهادة HTTPS تلقائيًا بعد إضافة السجل.

## Google Search Console

بعد النشر: أضف الموقع في Search Console وقدّم `sitemap.xml`.

## التشغيل محليًا

افتح `index.html` مباشرة في المتصفح، أو شغّل خادمًا محليًا:

```bash
npx serve .
```
