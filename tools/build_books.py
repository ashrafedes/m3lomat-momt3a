# Generate books.html (Arabic) and books-en.html (English) — top books with covers and links.
# Covers: Open Library Covers API (queried once, cached in tools/covers.json)
# Downloads: Project Gutenberg for public-domain classics; Google Books / Open Library for the rest.
# Usage: python tools/build_books.py
import json, os, re, sys, urllib.request, urllib.parse, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "tools", "covers.json")
UA = {"User-Agent": "m3lomat-books-builder/1.0 (static site generator)"}

def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return None

# ---------------- book data ----------------
# (section, title_en_query, display_title, author, summary, kind)
# kind: "pg" = try Project Gutenberg first | "gb" = Google Books link

AR_SECTIONS = {
    "lit": "روايات وأدب",
    "heritage": "تراث وكلاسيكيات",
    "self": "تنمية وفكر",
}
EN_SECTIONS = {
    "classic": "Classics — Free Downloads",
    "modern": "Modern Bestsellers — Preview & Borrow",
}

AR_BOOKS = [
    # ---------- lit ----------
    ("lit","Awlad Haratina","أولاد حارتنا","نجيب محفوظ","رواية رمزية جريئة تستعيد تاريخ الأديان والبشر في حارة مصرية. من أشهر أعمال نوبل الأدب وأكثرها إثارة للجدل.","gb"),
    ("lit","Umm Saad","أم سعد","غسان كنفاني","من أعمال كنفاني الإنسانية عن الأم الفلسطينية وصمودها أمام التهجير. نص قصير عميق الأثر.","gb"),
    ("lit","Ayam Taha Hussein","الأيام","طه حسين","سيرة ذاتية خالدة لعميد الأدب العربي — من كفيف في صعيد مصر إلى أستاذ الأدب. جزء من وجدان كل قارئ عربي.","gb"),
    ("lit","Bayn al-Qasrayn","بين القصرين","نجيب محفوظ","الجزء الأول من الثلاثية الشهيرة: حياة عائلة مصرية بين الحربين. بداية أعظم ملحمة روائية عربية.","gb"),
    ("lit","Azazeel","عزازيل","يوسف زيدان","رواية فائزة بالبوكر عن راهب يصاحب الترجمات الأولى للمسيحية بين الإسكندرية والقدس. فلسفة وتاريخ وشك.","gb"),
    ("lit","Saq al-Bambu","ساق البامبو","سعود السنعوسي","الفائزة بالبوكر العالمية — هوية منقسمة بين الكويت والفلبين وأسئلة الدين والانتماء.","gb"),
    ("lit","Khawf","خوف","أسامة المسلم","من أنجح روايات الرعب العربية الحديثة — عالم مظلم من الكيانات والأسرار.","gb"),
    ("lit","Ard Zikola","أرض زيكولا","عمرو عبد الحميد","فانتازيا عربية لاقت رواجًا واسعًا — مدينة تحت الأرض تحكمها وحدة العملة الوحيدة: ذكاء الإنسان.","gb"),
    ("lit","Tharthara fawq al-Nil","ثرثرة فوق النيل","نجيب محفوظ","مجموعة مثقفين على عوامة في النيل يعرّي محفوظ عبرهم عبث المثقف وضياعه في الستينات.","gb"),
    ("lit","Bidaya wa Nihaya","بداية ونهاية","نجيب محفوظ","مأساة عائلة مصرية تنهار بعد موت العائل — من أعمق روايات الواقعية عند محفوظ.","gb"),
    ("lit","Shams al-Asr","شمس الأصيل","نادية سلامة","رواية مصرية محبوبة عن عائلة البرنس الباجوري — حب وطبقات وأسرار العاصمة.","gb"),
    ("lit","Mamlakat al-Ghuraba","مملكة الغرباء","علي الوزير","رواية سودانية عن الطموح والمدن والتهميش، لاقت صدى واسعًا بين القراء الشباب.","gb"),
    ("lit","Kul Usbu Yawm Jumaa","كل أسبوع يوم جمعة","إبراهيم عبد المجيد","ثلاثية إسكندرية البديعة — حي شعبي ونساء يبنين بيتًا وحياة خارج الزمن.","gb"),
    ("lit","Ibram al-Aziz","أنثى","علاء الأسواني","من روائع الأسواني الإنسانية عن المرأة المصرية بين العادات والحب والضغط الاجتماعي.","gb"),
    ("lit","Imarat Yaqubian","عمارة يعقوبيان","علاء الأسواني","الرواية الأشهر عربيًا في العقدين الأخيرين — عمارة واحدة تعكس المجتمع المصري كله بفساده وأحلامه.","gb"),
    ("lit","Frankenstein fi Baghdad","فرانكشتاين في بغداد","أحمد سعداوي","الفائزة بالبوكر العالمية — وحش يجمع من أشلاء ضحايا التفجيرات ينتقم في بغداد ما بعد الاحتلال.","gb"),
    ("lit","Shiha","شيخة","عزيز نيسين","من أعمال السخرية العربية — كوميديا سياسية تكشف المجتمع بضحك مرير.","gb"),
    ("lit","Daqat al-Sham","دقات الشام","حمودة حسين","رواية إنسانية عن الحب والحنين لزمن دمشق الجميل قبل الحرب.","gb"),
    ("lit","Al-Walima","الوليمة الأعمى","يوسف إدريس","من قصص أستاذ القصة القصيرة في مصر — إنسانية العامة وحكمة الشارع.","gb"),
    ("lit","The Blue Elephant","الفيل الأزرق","أحمد مراد","رواية تشويق غيّرت خريطة القراءة العربية — طبيب نفسي داخل مستشفى المجانين وألغاز بلا نهاية.","gb"),
    # ---------- heritage ----------
    ("heritage","Muqaddima ibn Khaldun","مقدمة ابن خلدون","ابن خلدون","أهم كتاب عربي في علم الاجتماع والتاريخ — نظرية العمران وصعود الدول وسقوطها قبل أرباستها بقرون.","gb"),
    ("heritage","Kalila wa Dimna","كليلة ودمنة","ابن المقفع","تحفة الأدب الحكمي — قصص حيوانات رمزية عن السياسة والحكمة والدهاء، أثرت في أدب العالم كله.","gb"),
    ("heritage","Al-Bayan wa al-Tabyin","البيان والتبيين","الجاحظ","موسوعة البلاغة والأدب عند أذكى كتّاب العرب — طرائف وبلاغة وعلم في مجلدات ممتعة.","gb"),
    ("heritage","Risalat al-Ghufran","رسالة الغفران","أبو العلاء المعري","رحلة خيالية للسماوات والجحيم قبل دانتي — نقد لاذع لعصره بأسلوب لا يشيخ.","gb"),
    ("heritage","Hayy ibn Yaqzan","حي بن يقظان","ابن طفيل","أول رواية فلسفية في التاريخ — طفل يتربى وحده على جزيرة ويكتشف الكون والإله بعقله.","gb"),
    ("heritage","Al-Aghani","الأغاني","أبو الفرج الأصفهاني","أضخم موسوعة في تاريخ الأغنية والأدب العربي — أخبار الشعراء والمغنين والبلاط عبر قرون.","gb"),
    ("heritage","Tabai al-Istibdad","طبائع الاستبداد","عبد الرحمن الكواكبي","أول كتاب عربي يحلل الاستبداد السياسي علميًا — تشريح مبكر للطغيان وعلاجه.","gb"),
    ("heritage","Al-Kamil fi al-Tarikh","الكامل في التاريخ","ابن الأثير","من أعظم كتب التاريخ عند العرب — سرد شامل لأحداث العالم الإسلامي حتى عصره.","gb"),
    ("heritage","Maqamat al-Hariri","مقامات الحريري","بديع الزمان الهمذاني","روائع الأدب المسجوع — شخصية أبي زيد السروجي في حكايات بلاغية فكاهية خالدة.","gb"),
    ("heritage","Sahih al-Bukhari","صحيح البخاري","الإمام البخاري","أصح كتاب بعد القرآن عند أهل السنة — موسوعة الحديث النبوي مصنفة بالأبواب.","gb"),
    ("heritage","Tafsir Ibn Kathir","تفسير ابن كثير","ابن كثير","أشهر التفاسير قراءةً — تفسير القرآن بالمأثور بأسلوب ميسر ومصادر موثقة.","gb"),
    ("heritage","Riyad al-Salihin","رياض الصالحين","النووي","جامع الأحاديث في الأخلاق والآداب — من أكثر الكتب تداولًا في العالم الإسلامي.","gb"),
    ("heritage","Zad al-Ma'ad","زاد المعاد","ابن القيم","هداية النبي في العبادات والمعاملات والطب — سيرة عملية تفصيلية.","gb"),
    ("heritage","Al-Muwatta","الموطأ","الإمام مالك","أول مدوَّن في الفقه والحديث — أساس المذهب المالكي ومكتبة وقفية أصلية.","gb"),
    ("heritage","Nahj al-Balagha","نهج البلاغة","الإمام علي بن أبي طالب","خطبه ورسائله وحكمه — ذروة البيان العربي وكنز البلاغيين على مر العصور.","gb"),
    ("heritage","Ayyam al-Arab","أيام العرب قبل الإسلام","محمد أحمد جاد المولى","توثيق ممتع لحياة العرب الجاهلية — ملاحمها وعاداتها ودياناتها قبل الإسلام.","gb"),
    ("heritage","Awdat al-Ruh","عودة الروح","توفيق الحكيم","رواية فلسفية عن الأسرة المصرية بين الحربين تبحث عن روح مصر الكامنة.","gb"),
    ("heritage","Futuhat Makkah","الفتوحات المكية","ابن عربي","موسوعة التصوف عند محيي الدين ابن عربي — أعمق نص روحي فلسفي في التراث.","gb"),
    ("heritage","Adab al-Dunya wa al-Din","أدب الدنيا والدين","الماوردي","كلاسيكية الأخلاق العملية — جدول السلوك بين الدين والدنيا عند فقيه كبير.","gb"),
    ("heritage","Fadail al-Quran","فضائل القرآن","ابن كثير","جامع ما ورد في فضل القرآن وحملته — للحفظ والتدبر.","gb"),
    # ---------- self ----------
    ("self","Ila al-Safina","أبجديات البحث عن المعنى","مصطفى محمود","تأملات محبوبة عن الغيب والروح والوجود بأسلوب الدكتور الأقرب للقلوب.","gb"),
    ("self","Rihla ibn Battuta","رحلة ابن بطوطة","ابن بطوطة","أعظم كتاب رحلات في التاريخ — 30 سنة من الصين إلى مالي بعين رحالة فضولي.","gb"),
    ("self","Kilab Sina","نظرية الفستق","فهد عامر الأحمدي","من أشهر كتب التنمية العربية — أسئلة الحياة والنجاح بأسلوب خفيف محبب.","gb"),
    ("self","Sanawat al-Jaish","أعقد أنواع السعادة","أحمد الغزي","كتاب نفسي اجتماعي شائع عن البحث عن السعادة الداخلية وتوازن النفس.","gb"),
    ("self","Sulayman al-Hakim","أنا وأنت","مصطفى محمود","حوارات ذاتية عن النفس البشرية وتناقضاتها — محمود في أنقى لحظاته.","gb"),
    ("self","Al-Wajh al-Akhar","عقل بلا جسد","مصطفى محمود","تأملات في الروح والعلم والغيب — من أكثر كتبه مبيعًا على الإطلاق.","gb"),
    ("self","Tafakkur","على حافة الانتحار","مصطفى محمود","قصة تحوله من الطب والمادية إلى البحث الروحي — سيرة فكرية ممتعة.","gb"),
    ("self","Khawatir Fata","خواطر فتى","محمد الغزالي","من أجمل كتب التوجيه النفسي والإيماني في القرن العشرين.","gb"),
    ("self","Kayfa Tatakalam","كيف تحدث الناس","مهدي الموسوي","مهارات الحوار والإقناع اليومية — من أكثر كتب التنمية العربية انتشارًا.","gb"),
    ("self","Al-Jasad","النبي الخاتم","علي الوردي","من روائع الاجتماع العراقي — تحليل شخصية الرسول وحركة التاريخ النبوي.","gb"),
    ("self","La Tahzan","لا تحزن","عائض القرني","الكتاب الأكثر مبيعًا عربيًا — فن التفاؤل والتعامل مع الهموم بروح شرعية وواقعية.","gb"),
    ("self","Inni Akhbartak","رجال حول الرسول","خالد محمد خالد","سير صحابة بقلم أديب — لمحات إنسانية تاريخية محببة لكل بيت عربي.","gb"),
    ("self","Nida al-Rahman","الحب في زمن الكوليرا","غابرييل ماركيز (ترجمة)","ملحمة حب تمتد نصف قرن — من أجمل ما كُتب عن الانتظار والشيخوخة، مترجمة بعناية.","gb"),
    ("self","Al-Munadara","مئة عام من العزلة","غابرييل ماركيز (ترجمة)","الرائعة التي فتحت الواقعية السحرية للعالم — قرون ماكندو وأجيال بوينديا.","gb"),
    ("self","Aqwal al-Nisa","حكايات زرنقة","نزار قباني","ديوان الحب الأشهر عربيًا — الشاعر الذي علّم العربية أن تحب بشعرها اليومي.","gb"),
]

EN_BOOKS = [
    # ---------- classics (Project Gutenberg direct downloads) ----------
    ("classic","Pride and Prejudice","Pride and Prejudice","Jane Austen","Elizabeth Bennet versus her own pride and Mr Darcy's prejudice — the wittiest courtship in English literature.","pg"),
    ("classic","Moby Dick","Moby-Dick","Herman Melville","Captain Ahab's obsessive hunt for the white whale — a towering American epic of obsession and the sea.","pg"),
    ("classic","Frankenstein","Frankenstein","Mary Shelley","A scientist builds life then abandons it — the original science-fiction novel and still its most haunting.","pg"),
    ("classic","Dracula","Dracula","Bram Stoker","Count Dracula leaves Transylvania for London — the gothic novel that defined the modern vampire.","pg"),
    ("classic","Adventures of Sherlock Holmes","The Adventures of Sherlock Holmes","Arthur Conan Doyle","Twelve cases of the world's greatest detective — logic, disguise, and Victorian London at its best.","pg"),
    ("classic","A Tale of Two Cities","A Tale of Two Cities","Charles Dickens","'It was the best of times' — love and sacrifice across London and revolutionary Paris.","pg"),
    ("classic","Great Expectations","Great Expectations","Charles Dickens","Pip's rise from the marshes to a gentleman — a haunting tale of ambition, love, and a bride frozen in time.","pg"),
    ("classic","Jane Eyre","Jane Eyre","Charlotte Brontë","An orphaned governess finds love and a terrible secret at Thornfield Hall — fierce, gothic, unforgettable.","pg"),
    ("classic","Wuthering Heights","Wuthering Heights","Emily Brontë","Heathcliff and Catherine's savage love on the moors — the most tempestuous romance in English.","pg"),
    ("classic","Crime and Punishment","Crime and Punishment","Fyodor Dostoevsky","A student commits murder to prove he's extraordinary — and guilt becomes his true sentence.","pg"),
    ("classic","The Brothers Karamazov","The Brothers Karamazov","Fyodor Dostoevsky","Three brothers, a murdered father, and every question of faith and doubt ever asked — Dostoevsky's summit.","pg"),
    ("classic","War and Peace","War and Peace","Leo Tolstoy","Napoleon invades Russia through aristocratic salons and battlefields — the great novel of an era.","pg"),
    ("classic","Anna Karenina","Anna Karenina","Leo Tolstoy","'Happy families are all alike' — passion, society, and the most famous train in literature.","pg"),
    ("classic","Don Quixote","Don Quixote","Miguel de Cervantes","A gentleman mad on chivalry tilts at windmills — the first modern novel and still among the funniest.","pg"),
    ("classic","The Picture of Dorian Gray","The Picture of Dorian Gray","Oscar Wilde","A portrait ages while its sitter stays beautiful — Wilde's glittering meditation on vanity and corruption.","pg"),
    ("classic","The Great Gatsby","The Great Gatsby","F. Scott Fitzgerald","Jay Gatsby's green light across the bay — the Jazz Age's glittering tragedy of the American dream.","pg"),
    ("classic","Little Women","Little Women","Louisa May Alcott","Meg, Jo, Beth and Amy March grow up through the Civil War — beloved for 150 years.","pg"),
    ("classic","Alice's Adventures in Wonderland","Alice's Adventures in Wonderland","Lewis Carroll","Down the rabbit hole into logic-twisting nonsense — pure imagination that shaped fantasy forever.","pg"),
    ("classic","The Time Machine","The Time Machine","H.G. Wells","A Victorian inventor travels to 802,701 AD — the book that invented time-travel fiction.","pg"),
    ("classic","The War of the Worlds","The War of the Worlds","H.G. Wells","Martian tripods devastate Surrey — the alien-invasion story every later one borrows from.","pg"),
    ("classic","Treasure Island","Treasure Island","R.L. Stevenson","A boy, a treasure map, and Long John Silver — the pirate adventure every generation rediscovers.","pg"),
    ("classic","The Count of Monte Cristo","The Count of Monte Cristo","Alexandre Dumas","Betrayed into prison, Edmond Dantès returns as an avenging count — the ultimate revenge epic.","pg"),
    ("classic","The Three Musketeers","The Three Musketeers","Alexandre Dumas","'All for one, one for all' — d'Artagnan and the king's musketeers in swashbuckling France.","pg"),
    ("classic","Les Miserables","Les Misérables","Victor Hugo","Ex-convict Valjean and relentless Javert across revolutionary France — the great novel of mercy.","pg"),
    ("classic","Walden","Walden","Henry David Thoreau","Two years alone in a cabin by Walden Pond — the founding text of simple living and self-reliance.","pg"),
    ("classic","Meditations","Meditations","Marcus Aurelius","A Roman emperor's private notes on duty, death, and peace of mind — Stoicism at the source.","pg"),
    ("classic","The Prince","The Prince","Niccolò Machiavelli","The original handbook of political power — feared, studied, and still argued over 500 years later.","pg"),
    ("classic","The Art of War","The Art of War","Sun Tzu","Thirteen chapters of strategy from ancient China — read by generals, CEOs, and coaches ever since.","pg"),
    ("classic","The Metamorphosis","The Metamorphosis","Franz Kafka","Gregor Samsa wakes as a giant insect — modern alienation in its most famous image.","pg"),
    ("classic","Dr Jekyll and Mr Hyde","Strange Case of Dr Jekyll and Mr Hyde","R.L. Stevenson","A doctor unleashes his evil second self — the original split-personality thriller.","pg"),
    ("classic","Heart of Darkness","Heart of Darkness","Joseph Conrad","Up the Congo to meet Kurtz — colonialism's nightmare told in hypnotic prose.","pg"),
    ("classic","The Odyssey","The Odyssey","Homer","Ten years home from Troy — monsters, gods, and the most famous journey ever written.","pg"),
    ("classic","The Republic","The Republic","Plato","What is justice? Plato's dialogue that founded Western political philosophy.","pg"),
    ("classic","Thus Spoke Zarathustra","Thus Spoke Zarathustra","Friedrich Nietzsche","'God is dead' — Nietzsche's poetic prophecy of the Übermensch and self-overcoming.","pg"),
    ("classic","Utopia","Utopia","Thomas More","The 1516 book that named a genre — a traveller's account of the perfect impossible island society.","pg"),
    # ---------- modern (legal preview/borrow) ----------
    ("modern","Atomic Habits","Atomic Habits","James Clear","Tiny changes, remarkable results — the bestselling system of identity-based habits and 1% improvements.","gb"),
    ("modern","Rich Dad Poor Dad","Rich Dad Poor Dad","Robert Kiyosaki","Two fathers, two money mindsets — the book that changed how millions think about assets vs. liabilities.","gb"),
    ("modern","Sapiens","Sapiens","Yuval Noah Harari","How Homo sapiens conquered the world — a sweeping, witty history from cognitive to technological revolution.","gb"),
    ("modern","Thinking Fast and Slow","Thinking, Fast and Slow","Daniel Kahneman","The Nobel laureate's map of the two systems driving your mind — biases, choices, and judgment.","gb"),
    ("modern","Deep Work","Deep Work","Cal Newport","Focus is a superpower — rules for producing elite work in a distracted world.","gb"),
    ("modern","7 Habits","The 7 Habits of Highly Effective People","Stephen Covey","From dependence to interdependence — the classic personal-effectiveness framework.","gb"),
    ("modern","How to Win Friends","How to Win Friends and Influence People","Dale Carnegie","The 1936 classic on people skills — still the most reprinted human-relations book ever.","gb"),
    ("modern","The Subtle Art","The Subtle Art of Not Giving a F*ck","Mark Manson","A counterintuitive approach to a good life — pick what matters and let the rest go.","gb"),
    ("modern","Psychology of Money","The Psychology of Money","Morgan Housel","Doing well with money has less to do with intelligence than behavior — 20 short lessons on wealth.","gb"),
    ("modern","Ikigai","Ikigai","Héctor García & Francesc Miralles","The Japanese secret to a long, meaningful life — from the island of centenarians.","gb"),
    ("modern","Educated","Educated","Tara Westover","A memoir of a girl who left a survivalist home for Cambridge — about family, memory, and self-invention.","gb"),
    ("modern","The Alchemist","The Alchemist","Paulo Coelho","A shepherd follows his dream across the desert — the fable about listening to your heart's legend.","gb"),
    ("modern","Power of Now","The Power of Now","Eckhart Tolle","The spiritual classic about presence — quieting the mind by living entirely in the now.","gb"),
    ("modern","Man's Search for Meaning","Man's Search for Meaning","Viktor Frankl","A psychiatrist's Holocaust survival and the birth of logotherapy — meaning as the deepest human drive.","gb"),
    ("modern","Start with Why","Start with Why","Simon Sinek","Great leaders inspire by starting with purpose — the Golden Circle behind Apple and the Wright brothers.","gb"),
]

def gb_link(title, author):
    q = urllib.parse.quote(f"{title} {author}".strip())
    return f"https://books.google.com/books?q={q}"

def pg_link(title, author):
    q = urllib.parse.quote(title)
    d = fetch_json(f"https://gutendex.com/books?search={q}")
    if d and d.get("results"):
        for b in d["results"]:
            if any(author.split()[0].lower() in a.get("name","").lower() for a in b.get("authors",[])) or not b.get("authors"):
                return f"https://www.gutenberg.org/ebooks/{b['id']}", True
    return gb_link(title, author), False

def cover_for(title, author, cache):
    key = f"{title}|{author}"
    if key in cache: return cache[key]
    q = urllib.parse.quote(title)
    a = urllib.parse.quote(author.split()[0]) if author else ""
    url = f"https://openlibrary.org/search.json?q={q}&fields=cover_i&limit=1"
    if a: url += f"&author={a}"
    d = fetch_json(url)
    img = ""
    if d and d.get("docs") and d["docs"][0].get("cover_i"):
        img = f"https://covers.openlibrary.org/b/id/{d['docs'][0]['cover_i']}-M.jpg"
    cache[key] = img
    time.sleep(0.3)
    return img

HEAD = """<!DOCTYPE html>
<html lang="{lang}" dir="{dir}">
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
  <script async src="https://www.googletagmanager.com/gtm.js?id=GTM-WZX4PWH4"></script>
  <script async src="https://www.googletagmanager.com/gtm.js?id=GTM-P8QPQVWR"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
  </script>
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <a href="index.html" class="logo"><img class="logo-mark" src="assets/img/logo.png" alt="معلومات ممتعة"><span>معلومات <strong>ممتعة</strong></span></a>
      <nav class="nav">
        <a href="index.html#random">{home}</a>
        <a href="videos.html">{v}</a>
        <a href="articles.html">{a}</a>
        <a href="books.html">{b}</a>
        <a href="facts.html">{f}</a>
      </nav>
      <a class="btn yt sm" href="https://www.youtube.com/@m3lomat-momt3a?sub_confirmation=1" target="_blank" rel="noopener">▶ {sub}</a>
      <button class="lang-btn" id="langBtn" onclick="window.location.href=location.pathname.endsWith('books-en.html')?'books.html':'books-en.html'">{toggle}</button>
    </div>
  </header>
  <main>
    <section class="videos">
      <div class="container">
"""
FOOT = """      </div>
    </section>
  </main>
  <footer class="site-footer">
    <div class="container footer-inner">
      <p>معلومات ممتعة — m3lomat-momt3a.org</p>
    </div>
  </footer>
  <script>
    try {
      var _l = localStorage.getItem("lang") || "ar";
      document.querySelectorAll('a[href="books.html"], a[href="books-en.html"]').forEach(function (x) {
        x.href = (_l === "en") ? "books-en.html" : "books.html";
      });
    } catch (e) {}
  </script>
</body>
</html>
"""

def esc(s):
    return (s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;"))

def load_extra():
    """Extra books added via books-admin.html -> assets/js/books_extra.js"""
    p = os.path.join(ROOT, "assets/js/books_extra.js")
    if not os.path.exists(p):
        return []
    m = re.search(r"EXTRA_BOOKS=(\[.*\])", open(p, encoding="utf-8").read(), re.S)
    return json.loads(m.group(1)) if m else []


def load_books_js():
    """Canonical book lists edited via books-admin.html -> assets/js/books_data.js"""
    p = os.path.join(ROOT, "assets/js/books_data.js")
    if not os.path.exists(p):
        return None, None
    src = open(p, encoding="utf-8").read()
    ar = re.search(r"BOOKS_AR=(\[.*?\]);", src, re.S)
    en = re.search(r"BOOKS_EN=(\[.*?\]);", src, re.S)
    return (json.loads(ar.group(1)) if ar else [],
            json.loads(en.group(1)) if en else [])


def book_page_filename(lang, idx):
    return f"book-{lang}-{idx}.html"


def update_sitemap(n_ar, n_en):
    """Replace book-N entries in sitemap.xml with the current set."""
    p = os.path.join(ROOT, "sitemap.xml")
    sm = open(p, encoding="utf-8").read()
    sm = re.sub(r"\s*<url>\s*<loc>https://m3lomat-momt3a\.org/book-(?:ar|en)-\d+\.html</loc>.*?</url>", "", sm, flags=re.S)
    add = []
    for lang, n in (("ar", n_ar), ("en", n_en)):
        for i in range(n):
            add += ["  <url>",
                    f"    <loc>https://m3lomat-momt3a.org/{book_page_filename(lang, i)}</loc>",
                    "    <changefreq>monthly</changefreq>",
                    "    <priority>0.6</priority>",
                    "  </url>"]
    open(p, "w", encoding="utf-8").write(sm.replace("</urlset>", "\n".join(add) + "\n</urlset>"))


def card(title, author, summary, link, img, link_label, free, page=None):
    img_html = f'<img loading="lazy" src="{img}" alt="{esc(title)}">' if img else \
               '<div class="thumb" style="display:grid;place-items:center;font-size:2rem">📖</div>'
    badge = ' <span class="chip" style="pointer-events:none;font-size:.7rem;padding:.1rem .5rem">FREE</span>' if free else ""
    title_html = f'<a href="{page}">{esc(title)}</a>' if page else esc(title)
    return f'''          <div class="video-card">
            <a class="thumb book-thumb" href="{page or link}">{img_html}</a>
            <div class="book-info">
              <h3 dir="auto">{title_html}</h3>
              <p class="book-author" dir="auto">{esc(author)}</p>
              <p class="book-summary" dir="auto">{esc(summary)}</p>
              <a class="btn primary sm book-dl" href="{link}" target="_blank" rel="noopener">{link_label}{badge}</a>
            </div>
          </div>
'''

def load_videos_flat():
    src = open(os.path.join(ROOT, "assets/js/videos.js"), encoding="utf-8").read()
    return re.findall(r'\["([^"]+)","(\w+)","((?:[^"\\]|\\.)*)","[^"]*",\d+\]', src)


def video_side(bk_idx, vids, lang):
    """5 channel videos for the sidebar, rotated by book index."""
    if not vids:
        return ""
    picks = [vids[(bk_idx * 13 + k * 7) % len(vids)] for k in range(min(5, len(vids)))]
    title = "فيديوهات القناة" if lang == "ar" else "Channel Videos"
    cards = "".join(
        f'        <a class="video-card" href="https://www.youtube.com/watch?v={v[0]}" target="_blank" rel="noopener">\n'
        f'          <div class="thumb"><img loading="lazy" src="https://i.ytimg.com/vi/{v[0]}/mqdefault.jpg" alt="{esc(v[2])}"><span class="play">▶</span></div>\n'
        f'          <h3 dir="auto">{esc(v[2])}</h3>\n'
        f'        </a>\n' for v in picks)
    return f'      <aside class="book-side">\n        <h2 class="side-title">{title}</h2>\n{cards}      </aside>\n'


def book_page(bk, lang, idx, sections, back_page, dl, free, vids):
    link, img = bk["link"], bk["img"]
    img_html = f'<img class="article-hero" style="max-width:220px" src="{img}" alt="{esc(bk["dt"])}">' if img else ""
    body = f"""        <div class="book-layout">
        <div>
        <nav class="breadcrumb"><a href="{back_page}">{'الكتب' if lang=='ar' else 'Books'}</a> / <a href="{back_page}#{bk['sec']}">{esc(sections[bk['sec']])}</a></nav>
        <article>
          <h1>{esc(bk['dt'])}</h1>
          <p class="book-author">{esc(bk['au'])}</p>
          {img_html}
          <p class="article-body">{esc(bk['sm'])}</p>
          <p><a class="btn primary" href="{link}" target="_blank" rel="noopener">{free if bk["free"] else dl}</a></p>
        </article>
        <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Book","name":"{esc(bk['dt'])}","author":"{esc(bk['au'])}","image":"{img}","inLanguage":"{lang}"}}</script>
        </div>
{video_side(idx, vids, lang)}        </div>
"""
    fname = book_page_filename(lang, idx)
    head = HEAD.format(lang=lang, dir=("rtl" if lang == "ar" else "ltr"),
                       title=f'{bk["dt"]} | معلومات ممتعة', desc=bk["sm"][:150], page=fname,
                       sub="اشترك", home="هل تعلم؟", v="فيديوهات", a="مقالات", b="كتب", f="المعلومات", toggle="EN") \
        if lang == "ar" else HEAD.format(
        lang=lang, dir="ltr", title=f'{bk["dt"]} | M3lomat Momt3a',
        desc=bk["sm"][:150], page=fname, sub="Subscribe", home="Did You Know?",
        v="Videos", a="Articles", b="Books", f="Facts", toggle="عربي")
    open(os.path.join(ROOT, fname), "w", encoding="utf-8").write(head + body + FOOT)


def build(books, sections, lang, page, title, desc, sub, home, v, a, b, f, dl, free_dl, dir_):
    cache = {}
    if os.path.exists(CACHE):
        cache = json.load(open(CACHE, encoding="utf-8"))
    vids = load_videos_flat()
    all_books = []
    for _b in books:
        if isinstance(_b, dict):
            all_books.append(dict(_b))
        else:
            s, q, d, u, m, k = _b
            all_books.append({"sec": s, "qt": q, "dt": d, "au": u, "sm": m, "kind": k})
    groups = {}
    for bk in all_books:
        groups.setdefault(bk["sec"], []).append(bk)
    out = [HEAD.format(lang=lang, dir=dir_, title=title, desc=desc, page=page,
                       sub=sub, home=home, v=v, a=a, b=b, f=f,
                       toggle=("EN" if lang == "ar" else "عربي"))]
    out.append(f'        <h1>{esc(title.split("|")[0].strip())} <span class="count">({len(all_books)})</span></h1>\n')
    out.append(f'        <p class="page-sub">{desc}</p>\n')
    out.append('        <nav class="chips cat-index">\n')
    for sec in sections:
        out.append(f'          <a class="chip" href="#{sec}">{sections[sec]} ({len(groups.get(sec,[]))})</a>\n')
    out.append('        </nav>\n')
    idx = 0
    for sec in sections:
        out.append(f'        <h2 id="{sec}">{sections[sec]} <span class="count">({len(groups.get(sec,[]))})</span></h2>\n        <div class="book-grid">\n')
        for bk in groups[sec]:
            if bk.get("link"):
                bk["free"] = bk.get("free", False)
            elif bk["kind"] == "pg":
                bk["link"], bk["free"] = pg_link(bk["qt"], bk["au"])
            elif bk["kind"] == "direct":
                bk["free"] = True
            else:
                bk["link"], bk["free"] = gb_link(bk["qt"] + " " + bk["au"], ""), False
            if "img" not in bk:
                bk["img"] = cover_for(bk["qt"], bk["au"], cache)
            fname = book_page_filename(lang, idx)
            book_page(bk, lang, idx, sections, page, dl, free_dl, vids)
            out.append(card(bk["dt"], bk["au"], bk["sm"], bk["link"], bk["img"],
                            free_dl if bk["free"] else dl, bk["free"], fname))
            idx += 1
        out.append('        </div>\n')
    out.append(FOOT)
    open(os.path.join(ROOT, page), "w", encoding="utf-8").write("".join(out))
    json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
    print(page, len(all_books), "books")
    return len(all_books)

if __name__ == "__main__":
    js_ar, js_en = load_books_js()
    if js_ar is not None:
        AR, EN = js_ar, js_en
    else:
        AR, EN = AR_BOOKS, EN_BOOKS
    n_ar = build(AR, AR_SECTIONS, "ar", "books.html",
          "أفضل 100 كتاب — مكتبة معلومات ممتعة",
          "أفضل الكتب العربية والمترجمة — روايات وتراث وتنمية، مع ملخص قصير ورابط تحميل أو معاينة قانونية لكل كتاب.",
          "اشترك", "هل تعلم؟", "فيديوهات", "مقالات", "كتب", "المعلومات", "معاينة / تحميل", "تحميل مجاني", "rtl")
    n_en = build(EN, EN_SECTIONS, "en", "books-en.html",
          "Top 100 Books | M3lomat Momt3a",
          "The top 100 must-read books — classics with free legal downloads (Project Gutenberg) and modern bestsellers with preview & borrow links.",
          "Subscribe", "Did You Know?", "Videos", "Articles", "Books", "Facts", "Preview / Download", "Free download", "ltr")
    update_sitemap(n_ar, n_en)
    print("sitemap updated:", n_ar + n_en, "book pages")
