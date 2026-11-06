# معلومات ممتعة — m3lomat-momt3a.bestsell.site

موقع ثابت (static site) باللغة العربية لعرض معلومات وحقائق ممتعة مصنّفة حسب الفئة، مع بحث وزر "معلومة جديدة".

## الملفات

| الملف | الوصف |
|---|---|
| `index.html` | الصفحة الرئيسية |
| `assets/css/style.css` | التنسيقات |
| `assets/js/facts.js` | بيانات المعلومات والتصنيفات — أضف معلومات جديدة هنا |
| `assets/js/app.js` | منطق الموقع (بحث، فلترة، نسخ، معلومة عشوائية) |
| `render.yaml` | إعدادات النشر على Render |

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

## التشغيل محليًا

افتح `index.html` مباشرة في المتصفح، أو شغّل خادمًا محليًا:

```bash
npx serve .
```
