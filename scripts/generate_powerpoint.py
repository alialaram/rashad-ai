"""
RASHAD AI - Professional PowerPoint Presentation Generator
Creates an executive 10-slide widescreen presentation (.pptx)
for the General Authority of Zakat in Yemen.
"""
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "RASHAD_AI_Executive_Presentation.pptx"
DOCS_OUTPUT_PATH = Path(__file__).resolve().parent.parent / "docs" / "executive-presentation" / "RASHAD_AI_Executive_Presentation.pptx"

# Corporate Color Palette
COLOR_NAVY = RGBColor(15, 23, 42)       # Slate 900
COLOR_EMERALD = RGBColor(4, 120, 87)    # Emerald 700
COLOR_LIGHT_BG = RGBColor(248, 250, 252) # Slate 50
COLOR_CARD_BG = RGBColor(255, 255, 255)  # White
COLOR_MUTED = RGBColor(100, 116, 139)    # Slate 500
COLOR_GOLD = RGBColor(217, 119, 6)       # Amber 600
COLOR_DARK_TEXT = RGBColor(30, 41, 59)   # Slate 800
COLOR_ACCENT = RGBColor(16, 185, 129)    # Emerald 500


def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="منظومة رشاد AI • الهيئة العامة للزكاة"):
        # Top brand bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
        bar.fill.solid()
        bar.fill.fore_color.rgb = COLOR_EMERALD
        bar.line.fill.background()

        # Category subtitle
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_EMERALD

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_NAVY

        # Subtle bottom border line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(226, 232, 240)
        line.line.fill.background()

    # =========================================================================
    # SLIDE 1: Cover Slide
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)

    # Background
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.fill.background()

    # Accent decorative block
    accent_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.2), Inches(3.6))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = COLOR_ACCENT
    accent_bar.line.fill.background()

    # Title Box
    title_box = slide1.shapes.add_textbox(Inches(1.2), Inches(1.6), Inches(11), Inches(3.8))
    tf1 = title_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "الهيئة العامة للزكاة — الجمهورية اليمنية"
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_ACCENT
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "منظومة رشاد AI (RASHAD AI)"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)
    p1.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "منظومة الذكاء الاصطناعي لإدارة وتحليل الاحتياج الزكوي وتوجيه الموارد"
    p2.font.size = Pt(20)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_after = Pt(20)

    p3 = tf1.add_paragraph()
    p3.text = "العرض الفني والمؤسسي الشامل للنسخة الأولى MVP • نوفمبر 2026"
    p3.font.size = Pt(13)
    p3.font.color.rgb = RGBColor(148, 163, 184)

    # Footer note on Cover
    note_box = slide1.shapes.add_textbox(Inches(1.2), Inches(6.2), Inches(11), Inches(0.6))
    p_note = note_box.text_frame.paragraphs[0]
    p_note.text = "ميثاق الذكاء الاصطناعي المسؤول • دعم قرار بشري (Human-in-the-Loop) • سيادة رقمية كاملة"
    p_note.font.size = Pt(11)
    p_note.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 2: Executive Vision & Core Principles
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "الرؤية الاستراتيجية والمبادئ الحاكمة للمشروع")

    cards_data_s2 = [
        ("الهدف المؤسسي للمنظومة", "أتمتة ودعم قرارات توجيه الموارد الزكوية للمستحقين الأكثر هشاشة، وكشف التكرار، واستخراج بيانات وثائق الهوية بدقة علمية."),
        ("المبدأ الشرعي الحاكم (Human-in-the-Loop)", "المنظومة أداة تحليل ودعم قرار مساند، وليست جهة إصدار أحكام. لا يتم اتخاذ أي قرار قبول أو حرمان آلي دون اعتماد بشري."),
        ("السيادة الرقمية وخصوصية البيانات", "فصل بيانات الهوية الصريحة عن التحليلات الإحصائية، وتجهيل المعرفات لمحللي البيانات، وتشغيل كامل محلياً (On-Premises)."),
    ]

    for i, (head, body) in enumerate(cards_data_s2):
        top_pos = Inches(1.8 + i * 1.7)
        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(1.4))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_BG
        card.line.color.rgb = RGBColor(203, 213, 225)

        tb = slide2.shapes.add_textbox(Inches(1.1), top_pos + Inches(0.15), Inches(11.1), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p_h = tf.paragraphs[0]
        p_h.text = f"• {head}"
        p_h.font.size = Pt(15)
        p_h.font.bold = True
        p_h.font.color.rgb = COLOR_NAVY
        p_h.space_after = Pt(6)

        p_b = tf.add_paragraph()
        p_b.text = body
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = COLOR_DARK_TEXT

    # =========================================================================
    # SLIDE 3: Architecture & Technology Stack
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "البنية المعمارية ومنظومة التقنيات المستخدمة (Tech Stack)")

    cols = [
        ("الخادم الخلفي (Backend)", [
            "Python 3.14 + FastAPI 0.162",
            "SQLAlchemy 2.1 ORM + Psycopg 3",
            "Pydantic v2 للتحقق الصارم",
            "JWT & Bcrypt للمصادقة وتشفير الكلمات",
            "22 اختباراً آلياً (Pytest) بنسبة 100%"
        ], COLOR_EMERALD),
        ("الواجهة الأمامية (Frontend)", [
            "React 19 + TypeScript + Vite 8",
            "Tailwind CSS v4 بتصميم مؤسسي متجاوب",
            "دعم كامل وأصيل للغة العربية (RTL)",
            "شريط تبديل سريع بين الأدوار (Quick Switcher)",
            "بناء فائق السرعة في 560 ملي ثانية"
        ], COLOR_NAVY),
        ("قاعدة البيانات والجغرافيا", [
            "PostgreSQL 18.6 محلياً",
            "امتداد pg_trgm للمطابقة العربية التقريبية",
            "15 جدولاً علائقياً محكماً (ERD)",
            "5 محافظات، 12 مديرية، 13 عزلة، 43 قرية",
            "150 أسرة اصطناعية و761 فرداً"
        ], COLOR_GOLD),
    ]

    for i, (title, items, color) in enumerate(cols):
        left = Inches(0.8 + i * 4.0)
        card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.8), Inches(3.733), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tb = slide3.shapes.add_textbox(left + Inches(0.25), Inches(2.0), Inches(3.233), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = color
        p_t.space_after = Pt(14)

        for item in items:
            p_i = tf.add_paragraph()
            p_i.text = f"✔ {item}"
            p_i.font.size = Pt(11)
            p_i.font.color.rgb = COLOR_DARK_TEXT
            p_i.space_after = Pt(10)

    # =========================================================================
    # SLIDE 4: Machine Learning Suite
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "حزمة نماذج تعلم الآلة المطبقة فعلياً (Machine Learning Suite)")

    ml_models = [
        ("1. عنقدة الأسر واكتشاف الهشاشة (K-Means Clustering)", [
            "خوارزمية تعلم غير موجه (Unsupervised) تقسم الأسر إلى 4 عناقيد احتياج واقعية دون فرض تسميات مسبقة.",
            "العنقود 0: أسر نازحة ومعدمة شديدة الهشاشة (إغاثة عاجلة وسلة غذائية).",
            "العنقود 1: أسر ذات أعباء صحية وإعاقات مزمنة (كفالة علاجية وإعانة معاقين).",
            "العنقود 2: أسر كبيرة بدخل شحيح وإعالة مرتفعة (مساعدات نقدية موسعة).",
            "العنقود 3: أسر محدودة الدخل بسكن مستقر (مشاريع تمكين اقتصادي وقروض حسنة)."
        ]),
        ("2. مصنف أولوية الاحتياج (Random Forest Classifier)", [
            "خوارزمية تعلم إشرافي (100 شجرة قرار) تتنبأ بفئة الأولوية (CRITICAL, HIGH, MEDIUM, LOW).",
            "دقة اختبار مقاسة: 74.4% على عينة اختبار معزولة من الأسر.",
            "حساب نسبة الثقة التنبؤية لكل أسرة (مثلاً: ثقة 88%)."
        ]),
        ("3. التنبؤ بالطلب وحجم المساعدة (Random Forest Regressor)", [
            "يتنبأ بحجم المنحة النقدية الطارئة بالريال اليمني (YER) لكل أسرة لسد فجوة الفقر المعيشية.",
            "معامل تحديد قوي R² = 0.888 ومتوسط خطأ مطلق 9,292 ريال يمني فقط."
        ])
    ]

    for i, (title, items) in enumerate(ml_models):
        top_pos = Inches(1.8 + i * 1.7)
        card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(1.5))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_BG
        card.line.color.rgb = RGBColor(203, 213, 225)

        tb = slide4.shapes.add_textbox(Inches(1.05), top_pos + Inches(0.12), Inches(11.2), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_EMERALD
        p_t.space_after = Pt(4)

        for it in items:
            p_b = tf.add_paragraph()
            p_b.text = f"• {it}"
            p_b.font.size = Pt(10.5)
            p_b.font.color.rgb = COLOR_DARK_TEXT
            p_b.space_after = Pt(2)

    # =========================================================================
    # SLIDE 5: Explainability & Feature Importances
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "الشفافية والتفسير: خط الأساس مقابل أهمية المتغيرات (Feature Importance)")

    # Left: Rule Baseline
    card_l = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1))
    card_l.fill.solid()
    card_l.fill.fore_color.rgb = COLOR_LIGHT_BG
    card_l.line.color.rgb = COLOR_NAVY

    tb_l = slide5.shapes.add_textbox(Inches(1.05), Inches(2.0), Inches(5.1), Inches(4.7))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p_tl = tf_l.paragraphs[0]
    p_tl.text = "خط الأساس الإرشادي الشفاف (Rule Baseline)"
    p_tl.font.size = Pt(15)
    p_tl.font.bold = True
    p_tl.font.color.rgb = COLOR_NAVY
    p_tl.space_after = Pt(12)

    weights = [
        ("الدخل الشهري ونصيب الفرد", "30%", "قياس الفجوة المالية مقارنة بخط الفقر الحرج"),
        ("نسبة الإعالة والتركيبة الأسرية", "25%", "عدد المعالين من الأطفال وكبار السن إلى العاملين"),
        ("الظروف الصحية والإعاقات", "25%", "حالات الأمراض المزمنة والإعاقات المستديمة"),
        ("طبيعة واستقرار المسكن", "20%", "مخيم نزوح، عشش ومقاش، إيجار، أو ملك")
    ]
    for w_name, w_pct, w_desc in weights:
        p_w = tf_l.add_paragraph()
        p_w.text = f"• {w_name} ({w_pct}): {w_desc}"
        p_w.font.size = Pt(11)
        p_w.font.color.rgb = COLOR_DARK_TEXT
        p_w.space_after = Pt(8)

    # Right: ML Feature Importance
    card_r = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1))
    card_r.fill.solid()
    card_r.fill.fore_color.rgb = COLOR_LIGHT_BG
    card_r.line.color.rgb = COLOR_EMERALD

    tb_r = slide5.shapes.add_textbox(Inches(7.15), Inches(2.0), Inches(5.1), Inches(4.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p_tr = tf_r.paragraphs[0]
    p_tr.text = "أهم المتغيرات الموجهة لتنبؤ تعلم الآلة (Gini)"
    p_tr.font.size = Pt(15)
    p_tr.font.bold = True
    p_tr.font.color.rgb = COLOR_EMERALD
    p_tr.space_after = Pt(12)

    importances = [
        ("هشاشة السكن والمأوى (housing_vulnerability)", "17.50%"),
        ("نصيب الفرد من الدخل (income_per_capita)", "16.39%"),
        ("إجمالي عدد أفراد الأسرة (num_members)", "13.85%"),
        ("حالات الإعاقة المستديمة (disability_count)", "10.44%"),
        ("حالات الأمراض المزمنة (chronic_illness_count)", "9.02%"),
        ("نسبة الإعالة الأسرية (dependency_ratio)", "8.65%"),
    ]
    for f_name, f_pct in importances:
        p_f = tf_r.add_paragraph()
        p_f.text = f"📊 {f_name}: {f_pct}"
        p_f.font.size = Pt(11)
        p_f.font.color.rgb = COLOR_DARK_TEXT
        p_f.space_after = Pt(8)

    # =========================================================================
    # SLIDE 6: Document Intelligence & OCR Pipeline
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "ذكاء الوثائق العربية والتحقق البشري جنباً إلى جنب (Document OCR)")

    ocr_steps = [
        ("1. المعالجة الرقمية للصورة (Computer Vision)", "تطبيق فلاتر تحسين التباين، تحويل الصورة للرمادي، وإزالة التشويش والعتبة الثنائية (Binarization) باستخدام مكتبة Pillow لرفع قابلية قراءة الخط العربي."),
        ("2. استخراج الحقول ومؤشر الثقة الاحتمالي", "استخراج الحقول الأساسية (الاسم الكامل، الرقم الوطني، تاريخ الميلاد، مكان الإصدار) مع حساب مؤشر ثقة رقمي ملون (Confidence Score) وتنبيه الحقول المشبوهة."),
        ("3. المراجعة الثنائية البصرية (Side-by-Side Review)", "عرض صورة الوثيقة الأصلية إلى جانب البيانات المستخرجة، لتمكين الموظف من تصحيح أي خطأ قراءة آلي وتأكيد المصادقة والاعتماد البشري الرسمي."),
    ]

    for i, (st, desc) in enumerate(ocr_steps):
        top_pos = Inches(1.8 + i * 1.7)
        card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(1.4))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_BG
        card.line.color.rgb = RGBColor(203, 213, 225)

        tb = slide6.shapes.add_textbox(Inches(1.1), top_pos + Inches(0.15), Inches(11.1), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p_h = tf.paragraphs[0]
        p_h.text = st
        p_h.font.size = Pt(14)
        p_h.font.bold = True
        p_h.font.color.rgb = COLOR_NAVY
        p_h.space_after = Pt(4)

        p_b = tf.add_paragraph()
        p_b.text = desc
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = COLOR_DARK_TEXT

    # =========================================================================
    # SLIDE 7: Duplicate Detection & Human Arbitration
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "محرك كشف الازدواجية والتكرار والتحكيم البشري (Entity Resolution)")

    dup_boxes = [
        ("المطابقة التامة القطعية (Deterministic)", "مطابقة فورية على الرقم الوطني الموحد ورقم هاتف التواصل للقبض على التكرار المباشر فور إدخاله بالنظام."),
        ("المطابقة الاحتمالية المعيارية (Probabilistic)", "استخدام خوارزمية الرموز الثلاثية للأسماء العربية (pg_trgm) ومسافة Levenshtein بعد إزالة علامات التشكيل وتوحيد الهمزات مقترنة بالجوار المكاني."),
        ("التحكيم والاعتماد البشري الثنائي", "النظام يولد «تنبيه اشتباه» فقط ولا يحذف أو يدمج أي ملف آلياً. يقرر الموظف المخول إما (تأكيد الدمج) أو (استبعاد الاشتباه واعتباره تشابه أسماء طبيعي)."),
    ]

    for i, (head, body) in enumerate(dup_boxes):
        top_pos = Inches(1.8 + i * 1.7)
        card = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(1.4))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_BG
        card.line.color.rgb = RGBColor(203, 213, 225)

        tb = slide7.shapes.add_textbox(Inches(1.1), top_pos + Inches(0.15), Inches(11.1), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p_h = tf.paragraphs[0]
        p_h.text = f"🔍 {head}"
        p_h.font.size = Pt(14)
        p_h.font.bold = True
        p_h.font.color.rgb = COLOR_NAVY
        p_h.space_after = Pt(4)

        p_b = tf.add_paragraph()
        p_b.text = body
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = COLOR_DARK_TEXT

    # =========================================================================
    # SLIDE 8: Roles, Access Control & Privacy
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "مصفوفة الأدوار والصلاحيات المؤسسية وحماية الخصوصية (RBAC)")

    roles = [
        ("مسؤول النظام التقني (Admin)", "إدارة الإعدادات وصيانة السيرفر (محظور من الوصول الاستطلاعي لبيانات المستفيدين)."),
        ("أخصائي تسجيل المستفيدين", "إدخال وتدقيق الملفات، معالجة الوثائق بالـ OCR، وتسجيل فاقدي الوثائق بمعرف مؤقت وإفادة محلية."),
        ("الباحث الميداني (صنعاء)", "نطاق جغرافي مقيد بمحافظة صنعاء لإدخال الزيارات الميدانية ومتابعة الحالات المحلية."),
        ("مسؤول برامج الزكاة", "مراجعة تقييمات الذكاء الاصطناعي، اعتماد المساعدات، وفض حالات الازدواجية المشبوهة."),
        ("محلل البيانات والتخطيط", "واجهة محجوبة الهويات بالكامل تظهر فيها فقط المعرفات المستعارة (ANON-YE-...) لحماية الخصوصية."),
        ("مدقق الرقابة والتفتيش", "صلاحيات قراءة شاملة لكافة السجلات والقرارات لتتبع الامتثال المالي والشرعي.")
    ]

    for i, (r_title, r_desc) in enumerate(roles):
        row = i // 2
        col = i % 2
        left = Inches(0.8 + col * 6.0)
        top_pos = Inches(1.8 + row * 1.7)

        card = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top_pos, Inches(5.7), Inches(1.4))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_BG
        card.line.color.rgb = RGBColor(203, 213, 225)

        tb = slide8.shapes.add_textbox(left + Inches(0.2), top_pos + Inches(0.12), Inches(5.3), Inches(1.15))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = f"👤 {r_title}"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_EMERALD
        p_t.space_after = Pt(4)

        p_d = tf.add_paragraph()
        p_d.text = r_desc
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = COLOR_DARK_TEXT

    # =========================================================================
    # SLIDE 9: Testing, Quality & Live Demo Capabilities
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "الجودة والاختبار والتشغيل المباشر للمنظومة (Quality & Testing)")

    stats_boxes = [
        ("22 / 22 اختبار ناجح", "100% نسبة نجاح الاختبارات الآلية (Pytest) للـ API والنماذج وقواعد البيانات."),
        ("560 ملي ثانية", "زمن بناء الواجهة الأمامية بالكامل (React 19 + TypeScript + Rolldown)."),
        ("150 أسرة اصطناعية", "بيانات تدريب وتجربة مطابقة للتوزيع الديموغرافي اليمني مع 761 فرداً و29 معرفاً مؤقتاً."),
        ("تشغيل بنقرة واحدة", "ملف تشغيل ذكي (start_rashad.bat) يطلق الخادمين ويفتح المتصفح تلقائياً.")
    ]

    for i, (st_title, st_desc) in enumerate(stats_boxes):
        row = i // 2
        col = i % 2
        left = Inches(0.8 + col * 6.0)
        top_pos = Inches(1.8 + row * 2.5)

        card = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top_pos, Inches(5.7), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_BG
        card.line.color.rgb = COLOR_NAVY
        card.line.width = Pt(1.5)

        tb = slide9.shapes.add_textbox(left + Inches(0.3), top_pos + Inches(0.25), Inches(5.1), Inches(1.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = st_title
        p_t.font.size = Pt(20)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_EMERALD
        p_t.space_after = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = st_desc
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = COLOR_DARK_TEXT

    # =========================================================================
    # SLIDE 10: Future Roadmap & Next Steps
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "خارطة الطريق المؤسسية للانتقال للتشغيل الميداني الفعلي")

    roadmap = [
        ("المرحلة 1: المعايرة على بيانات حقيقية", "إعادة ضبط أوزان نماذج تعلم الآلة بالتعاون مع لجان قطاع المصارف والفقراء بالهيئة فور اعتماد تصنيف البيانات."),
        ("المرحلة 2: تدريب نموذج OCR عربي محلي عميق", "تثبيت وتدريب نموذج PaddleOCR مخصص للمستندات والخطوط اليمنية يعمل محلياً داخل خوادم الهيئة دون أي اتصال بالإنترنت."),
        ("المرحلة 3: التنبؤ الزمني بالطلب الموسمي", "بناء نماذج تنبؤ بالطلب الموسمي لتخصيص ميزانيات المساعدات مسبقاً قبل مواسم رمضان والكوارث والزروع."),
        ("المرحلة 4: التوسع الجغرافي والربط الشبكي", "تعميم المنظومة على كافة فروع الهيئة في عموم محافظات الجمهورية وربطها بأنظمة الصرف واللجان المجتمعية.")
    ]

    for i, (step_t, step_d) in enumerate(roadmap):
        top_pos = Inches(1.8 + i * 1.35)
        card = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(1.15))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_BG
        card.line.color.rgb = RGBColor(203, 213, 225)

        tb = slide10.shapes.add_textbox(Inches(1.1), top_pos + Inches(0.12), Inches(11.1), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = step_t
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_EMERALD
        p_t.space_after = Pt(3)

        p_d = tf.add_paragraph()
        p_d.text = step_d
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = COLOR_DARK_TEXT

    # Save presentation
    prs.save(OUTPUT_PATH)
    DOCS_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    prs.save(DOCS_OUTPUT_PATH)
    print(f"Presentation successfully created at:\n - {OUTPUT_PATH}\n - {DOCS_OUTPUT_PATH}")


if __name__ == "__main__":
    create_presentation()
