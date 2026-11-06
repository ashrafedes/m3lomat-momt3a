// Fact categories
const CATEGORIES = {
  space:   { name: "الفضاء",      en: "Space",       color: "#8b5cf6" },
  science: { name: "العلوم",      en: "Science",     color: "#22d3ee" },
  animals: { name: "الحيوانات",   en: "Animals",     color: "#34d399" },
  human:   { name: "جسم الإنسان", en: "Human Body",  color: "#f472b6" },
  history: { name: "التاريخ",     en: "History",     color: "#fbbf24" },
  tech:    { name: "التقنية",     en: "Technology",  color: "#60a5fa" },
  nature:  { name: "الطبيعة",     en: "Nature",      color: "#a3e635" },
  geo:     { name: "الجغرافيا",   en: "Geography",   color: "#fb923c" },
};

// Facts: { t: Arabic text, e: English text, c: category key }
const FACTS = [
  // Space
  { t: "يوم واحد على كوكب الزهرة أطول من سنته الكاملة؛ فهو يدور حول محوره ببطء شديد.", e: "A single day on Venus is longer than its entire year — it spins on its axis incredibly slowly.", c: "space" },
  { t: "الشمس تحتوي على 99.86% من كتلة المجموعة الشمسية بأكملها.", e: "The Sun holds 99.86% of the entire solar system's mass.", c: "space" },
  { t: "القمر يبتعد عن الأرض بنحو 3.8 سنتيمتر كل عام.", e: "The Moon drifts about 3.8 centimeters away from Earth every year.", c: "space" },
  { t: "الفضاء صامت تمامًا لأنه لا يوجد وسط ينقل الصوت مثل الهواء.", e: "Space is completely silent — there's no air to carry sound.", c: "space" },
  { t: "أكبر بركان في المجموعة الشمسية يقع على المريخ ويُسمى أوليمبوس مونس، وارتفاعه يعادل ثلاثة أضعاف قمة إفرست.", e: "The biggest volcano in the solar system, Olympus Mons on Mars, is three times taller than Everest.", c: "space" },
  { t: "الضوء القادم من الشمس يستغرق حوالي 8 دقائق و20 ثانية للوصول إلى الأرض.", e: "Sunlight takes about 8 minutes and 20 seconds to reach Earth.", c: "space" },
  { t: "يوجد نجم نيوتروني واحد بحجم مدينة تبلغ كتلته أكثر من كتلة الشمس.", e: "A neutron star the size of a city can weigh more than the Sun.", c: "space" },
  { t: "عدد النجوم في الكون المرصود أكبر من عدد حبات الرمل على جميع شواطئ الأرض.", e: "There are more stars in the observable universe than grains of sand on all Earth's beaches.", c: "space" },

  // Science
  { t: "الماء الساخن قد يتجمد أسرع من الماء البارد في ظروف معينة، وتُعرف هذه الظاهرة بتأثير مبيمبا.", e: "Hot water can freeze faster than cold water under certain conditions — the Mpemba effect.", c: "science" },
  { t: "البرق أشد حرارة من سطح الشمس بحوالي خمس مرات.", e: "Lightning is about five times hotter than the surface of the Sun.", c: "science" },
  { t: "الهليوم هو العنصر الوحيد الذي لا يمكن تجميده بالتبريد وحده عند الضغط العادي.", e: "Helium is the only element that can't be frozen by cooling alone at normal pressure.", c: "science" },
  { t: "الصوت ينتقل في الماء أسرع بحوالي أربع مرات من انتقاله في الهواء.", e: "Sound travels about four times faster in water than in air.", c: "science" },
  { t: "الذهب معدن قابل للأكل فعلًا؛ يُستخدم في بعض الحلويات الفاخرة.", e: "Gold is actually edible — it's used in some luxury desserts.", c: "science" },
  { t: "الباندا العملاقة تنتمي إلى فصيلة الدببة الحقيقية رغم طعامها النباتي.", e: "The giant panda is a true bear despite its plant-based diet.", c: "science" },
  { t: "جزيئات الماء الموجودة في كوب ماء واحد أكثر من عدد أكواب الماء في كل محيطات الأرض.", e: "One glass of water holds more molecules than there are glasses of water in all Earth's oceans.", c: "science" },
  { t: "الألماس والجرافيت (مادة القلم الرصاص) مصنوعان من العنصر نفسه: الكربون.", e: "Diamond and pencil graphite are made of the very same element: carbon.", c: "science" },

  // Animals
  { t: "قلب الأخطبوط ثلاثة قلوب، ودمه أزرق اللون.", e: "An octopus has three hearts, and its blood is blue.", c: "animals" },
  { t: "النحل يستطيع التعرف على وجوه البشر وتذكرها.", e: "Bees can recognize and remember human faces.", c: "animals" },
  { t: "الفراشات تتذوق الطعام بأرجلها.", e: "Butterflies taste their food with their feet.", c: "animals" },
  { t: "الدلافين تنام ونصف دماغها مستيقظ لتراقب الخطر.", e: "Dolphins sleep with half their brain awake to watch for danger.", c: "animals" },
  { t: "البومة لا تستطيع تحريك عينيها، لذلك تدير رأسها حتى 270 درجة.", e: "Owls can't move their eyes — so they turn their heads up to 270 degrees.", c: "animals" },
  { t: "نجم البحر يملك خمسة أدمغة صغيرة بدلًا من دماغ واحد.", e: "A starfish has five tiny brains instead of one.", c: "animals" },
  { t: "النمل لا ينام أبدًا، لكنه يأخذ مئات القيلولات القصيرة يوميًا.", e: "Ants never truly sleep — they take hundreds of tiny power naps a day.", c: "animals" },
  { t: "أظافر اليدين تنمو أسرع من أظافر القدمين بأربع مرات تقريبًا.", e: "Fingernails grow about four times faster than toenails.", c: "animals" },

  // Human body
  { t: "عظام الإنسان أقوى من الخرسانة بالوزن نفسه بأربع مرات تقريبًا.", e: "Human bone is roughly four times stronger than concrete for the same weight.", c: "human" },
  { t: "جسمك ينتج حوالي 25 مليون خلية جديدة كل ثانية.", e: "Your body produces about 25 million new cells every second.", c: "human" },
  { t: "العطسة الواحدة تخرج الهواء بسرعة قد تصل إلى 160 كيلومترًا في الساعة.", e: "A single sneeze can blast air out at up to 160 km/h.", c: "human" },
  { t: "لا يمكنك التنفس والبلع في اللحظة نفسها.", e: "You can't breathe and swallow at the same moment.", c: "human" },
  { t: "الإنسان البالغ يملك حوالي 100,000 كيلومتر من الأوعية الدموية، تكفي للف حول الأرض مرتين ونصف.", e: "An adult's blood vessels stretch ~100,000 km — enough to wrap around Earth two and a half times.", c: "human" },
  { t: "العين البشرية تستطيع التمييز بين نحو عشرة ملايين لون مختلف.", e: "The human eye can distinguish around ten million different colors.", c: "human" },
  { t: "المخ يستهلك حوالي 20% من طاقة الجسم رغم أن وزنه 2% فقط من وزن الجسم.", e: "The brain uses ~20% of the body's energy despite being only 2% of its weight.", c: "human" },
  { t: "أنت أطول صباحًا من مساء اليوم نفسه بحوالي سنتيمتر واحد بسبب ضغط العمود الفقري.", e: "You're about a centimeter taller in the morning than at night, thanks to spinal compression.", c: "human" },

  // History
  { t: "أكسفورد الجامعة أقدم من الإمبراطورية الأزتيكية بأكثر من مئتي عام.", e: "Oxford University is over 200 years older than the Aztec Empire.", c: "history" },
  { t: "أول جهاز كمبيوتر في العالم وزنه أكثر من 27 طنًا وشغل غرفة كاملة.", e: "The world's first computer weighed over 27 tons and filled a whole room.", c: "history" },
  { t: "أهرامات الجيزة كانت مغطاة بطبقة لامعة من الحجر الجيري الأبيض جعلتها تتلألأ تحت الشمس.", e: "The Giza pyramids were once covered in gleaming white limestone that sparkled in the sun.", c: "history" },
  { t: "نينتندو تأسست عام 1889 كشركة لصنع أوراق اللعب، قبل أكثر من قرن من ألعاب الفيديو.", e: "Nintendo was founded in 1889 as a playing-card company — a century before video games.", c: "history" },
  { t: "آخر محارب من الساموراي عاش حتى عام 1877، أي بعد اختراع الهاتف.", e: "The last samurai lived until 1877 — after the telephone was invented.", c: "history" },
  { t: "كليوپاترا عاشت زمنيًا أقرب إلى هبوط الإنسان على القمر منها إلى بناء الهرم الأكبر.", e: "Cleopatra lived closer in time to the Moon landing than to the building of the Great Pyramid.", c: "history" },
  { t: "الحكومة البريطانية استخدمت الحمام الزاجل رسميًا لنقل الرسائل حتى عام 2006.", e: "The British government officially used carrier pigeons for messages until 2006.", c: "history" },
  { t: "أقدم جامعة في العالم ما زالت تعمل هي جامعة القرويين في فاس بالمغرب، تأسست عام 859م.", e: "The world's oldest operating university, al-Qarawiyyin in Fez, Morocco, was founded in 859 CE.", c: "history" },

  // Technology
  { t: "أول رسالة بريد إلكتروني أُرسلت عام 1971، قبل ظهور الإنترنت التجاري بعقدين.", e: "The first email was sent in 1971 — two decades before the commercial internet.", c: "tech" },
  { t: "هاتفك الذكي أقوى حسابيًا بملايين المرات من الحاسوب الذي أرسل الإنسان إلى القمر.", e: "Your smartphone is millions of times more powerful than the computer that flew humans to the Moon.", c: "tech" },
  { t: "كلمة Robot جاءت من كلمة تشيكية تعني العمل الشاق الإجباري.", e: "The word 'robot' comes from a Czech word meaning forced labor.", c: "tech" },
  { t: "أول كاميرا رقمية صُنعت عام 1975 وكانت تستغرق 23 ثانية لتسجيل صورة واحدة.", e: "The first digital camera, built in 1975, took 23 seconds to record a single photo.", c: "tech" },
  { t: "اسم Bluetooth مستوحى من ملك دنماركي وحّد القبائل، كما توحّد التقنية الأجهزة.", e: "Bluetooth is named after a Danish king who united tribes — just as it unites devices.", c: "tech" },
  { t: "متوسط ما يُرفع على يوتيوب يبلغ حوالي 500 ساعة فيديو كل دقيقة.", e: "Around 500 hours of video are uploaded to YouTube every single minute.", c: "tech" },
  { t: "أول موقع ويب في التاريخ ما زال موجودًا حتى اليوم على الإنترنت.", e: "The very first website ever made is still online today.", c: "tech" },
  { t: "شعار USB مستوحى من رمح نبتون إله البحر، يرمز للقوة والسيطرة.", e: "The USB symbol is inspired by Neptune's trident, symbolizing power and control.", c: "tech" },

  // Nature
  { t: "العسل لا يفسد أبدًا؛ وُجد عسل في مقابر مصرية عمره 3000 عام وما زال صالحًا للأكل.", e: "Honey never spoils — 3,000-year-old honey found in Egyptian tombs is still edible.", c: "nature" },
  { t: "الموز ينمو على نبات عشبي عملاق وليس على شجرة.", e: "Bananas grow on a giant herb, not a tree.", c: "nature" },
  { t: "الفول السوداني ليس من المكسرات بل من البقوليات كالعدس والفاصوليا.", e: "Peanuts aren't nuts — they're legumes like lentils and beans.", c: "nature" },
  { t: "رمال الصحراء الكبرى تغطي أرضًا كانت خضراء مزروعة قبل آلاف السنين.", e: "The Sahara's sands cover land that was green and planted just thousands of years ago.", c: "nature" },
  { t: "البرق يضرب الأرض حوالي 100 مرة كل ثانية في أنحاء العالم.", e: "Lightning strikes Earth about 100 times every second worldwide.", c: "nature" },
  { t: "الكيوي يحتوي على فيتامين C أكثر من البرتقال بالوزن نفسه.", e: "Gram for gram, kiwi packs more vitamin C than oranges.", c: "nature" },
  { t: "الفراولة ليست من التوت نباتيًا، بينما الموز يُصنف من التوت.", e: "Strawberries aren't botanically berries — but bananas are.", c: "nature" },
  { t: "أطول شجرة في العالم يتجاوز ارتفاعها 115 مترًا، أطول من تمثال الحرية.", e: "The world's tallest tree tops 115 meters — taller than the Statue of Liberty.", c: "nature" },

  // Geography
  { t: "روسيا واسعة لدرجة أنها تضم 11 منطقة زمنية مختلفة.", e: "Russia is so vast it spans 11 different time zones.", c: "geo" },
  { t: "قارة أفريقيا أكبر من الولايات المتحدة والصين والهند وأوروبا مجتمعة تقريبًا.", e: "Africa is roughly bigger than the US, China, India, and Europe combined.", c: "geo" },
  { t: "يوجد في تركيا مدينة كاملة تحت الأرض اسمها ديرينكويو، كانت تتسع لعشرين ألف شخص.", e: "Turkey has an entire underground city, Derinkuyu, that could hold 20,000 people.", c: "geo" },
  { t: "النيل ليس أطول نهر في العالم حسب بعض القياسات الحديثة؛ الأمازون يتفوق عليه.", e: "By some modern measurements the Amazon — not the Nile — is the world's longest river.", c: "geo" },
  { t: "كندا تملك بحيرات أكثر من بقية دول العالم مجتمعة.", e: "Canada has more lakes than the rest of the world combined.", c: "geo" },
  { t: "أقصر رحلة طيران تجارية في العالم تستغرق أقل من دقيقتين بين جزيرتين في أسكتلندا.", e: "The world's shortest commercial flight takes under two minutes, between two Scottish islands.", c: "geo" },
  { t: "صحراء أنتاركتيكا أكبر صحراء في العالم، رغم أنها مغطاة بالجليد.", e: "Antarctica is the world's largest desert — despite being covered in ice.", c: "geo" },
  { t: "مدينة إسطنبول هي المدينة الوحيدة في العالم الواقعة على قارتين: آسيا وأوروبا.", e: "Istanbul is the only city in the world that sits on two continents: Asia and Europe.", c: "geo" },
];
