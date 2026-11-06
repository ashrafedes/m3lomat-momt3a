# معلومات ممتعة — m3lomat-momt3a.bestsell.site

الموقع الرسمي لقناة [معلومات ممتعة | Fun Facts](https://www.youtube.com/@m3lomat-momt3a) على يوتيوب — موقع ثابت (static) يعرض معلومات وحقائق ممتعة مصنّفة حسب الفئة، مع بحث وزر "معلومة جديدة" وأحدث فيديوهات القناة.

## الملفات

| الملف | الوصف |
|---|---|
| `index.html` | الصفحة الرئيسية (SEO meta + فيديوهات + مكتبة المعلومات) |
| `assets/css/style.css` | التنسيقات |
| `assets/js/facts.js` | بيانات المعلومات والتصنيفات — أضف معلومات جديدة هنا |
| `assets/js/app.js` | منطق الموقع (بحث، فلترة، نسخ، معلومة عشوائية) |
| `robots.txt` / `sitemap.xml` | ملفات الـ SEO لـ Google Search Console |
| `render.yaml` | إعدادات النشر على Render |

## إضافة فيديو جديد

في `index.html` داخل `.video-grid` انسخ بطاقة `video-card` وغيّر:
- رابط الفيديو: `https://www.youtube.com/watch?v=VIDEO_ID`
- الصورة: `https://i.ytimg.com/vi/VIDEO_ID/hqdefault.jpg`

## النشر على Render (مجاني)

1. ارفع الملفات إلى مستودع على GitHub.
2. في [Render Dashboard](https://dashboard.render.com):
   - **New → Static Site**
   - اربط مستودع GitHub
   - Build Command: اتركه فارغًا
   - Publish Directory: `.`
3. في **Settings → Custom Domains** أضف:
   `m3lomat-momt3a.bestsell.site`
4. في DNS الخاص بالنطاق `bestsell.site` أضف سجل:
   ```
   CNAME  m3lomat-momt3a  →  <your-service>.onrender.com
   ```
   Render يوفّر شهادة HTTPS تلقائيًا بعد إضافة السجل.

## Google Search Console

بعد النشر: أضف الموقع في Search Console وقدّم `sitemap.xml`.

## التشغيل محليًا

افتح `index.html` مباشرة في المتصفح، أو شغّل خادمًا محليًا:

```bash
npx serve .
```
