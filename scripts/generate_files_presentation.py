"""
RASHAD AI - Comprehensive Codebase & Files PowerPoint Presentation Generator
Creates a 16-slide widescreen presentation (.pptx) detailing every single
file, module, and architecture layer of RASHAD AI.
"""
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "RASHAD_AI_Project_Files_Presentation.pptx"

# Color Palette
COLOR_NAVY = RGBColor(15, 23, 42)        # Slate 900
COLOR_EMERALD = RGBColor(4, 120, 87)     # Emerald 700
COLOR_LIGHT_BG = RGBColor(248, 250, 252) # Slate 50
COLOR_MUTED = RGBColor(100, 116, 139)    # Slate 500
COLOR_GOLD = RGBColor(217, 119, 6)       # Amber 600
COLOR_DARK_TEXT = RGBColor(30, 41, 59)   # Slate 800
COLOR_ACCENT = RGBColor(16, 185, 129)    # Emerald 500
COLOR_BLUE = RGBColor(30, 58, 138)       # Blue 900


def create_comprehensive_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="منظومة رشاد AI • دليل ملفات وهيكلية المشروع الكاملة"):
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
        bar.fill.solid()
        bar.fill.fore_color.rgb = COLOR_EMERALD
        bar.line.fill.background()

        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_EMERALD

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.7), Inches(0.75))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_NAVY

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(226, 232, 240)
        line.line.fill.background()

    def add_cards_grid(slide, cards, cols=2):
        n = len(cards)
        rows = (n + cols - 1) // cols
        col_width = (11.733 - (cols - 1) * 0.3) / cols
        row_height = (5.3 - (rows - 1) * 0.25) / rows

        for i, (title, items, color) in enumerate(cards):
            r = i // cols
            c = i % cols
            left = Inches(0.8 + c * (col_width + 0.3))
            top_pos = Inches(1.75 + r * (row_height + 0.25))

            card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top_pos, Inches(col_width), Inches(row_height))
            card.fill.solid()
            card.fill.fore_color.rgb = COLOR_LIGHT_BG
            card.line.color.rgb = color
            card.line.width = Pt(1.5)

            tb = slide.shapes.add_textbox(left + Inches(0.2), top_pos + Inches(0.15), Inches(col_width - 0.4), Inches(row_height - 0.3))
            tf = tb.text_frame
            tf.word_wrap = True

            p_t = tf.paragraphs[0]
            p_t.text = title
            p_t.font.size = Pt(13)
            p_t.font.bold = True
            p_t.font.color.rgb = color
            p_t.space_after = Pt(6)

            for item in items:
                p_i = tf.add_paragraph()
                p_i.text = f"• {item}"
                p_i.font.size = Pt(10)
                p_i.font.color.rgb = COLOR_DARK_TEXT
                p_i.space_after = Pt(3)

    # -------------------------------------------------------------
    # SLIDE 1: Title Cover
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.fill.background()

    accent = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.2), Inches(3.8))
    accent.fill.solid()
    accent.fill.fore_color.rgb = COLOR_ACCENT
    accent.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.6), Inches(11), Inches(4.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "الهيئة العامة للزكاة — الجمهورية اليمنية"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.space_after = Pt(12)

    p = tf1.add_paragraph()
    p.text = "دليل وشرح كافة ملفات منظومة رشاد AI"
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.space_after = Pt(8)

    p = tf1.add_paragraph()
    p.text = "تشريح فني وهندسي لكل مسار، نموذج، واجهة برمجة، ومكون ذكي في المستودع البرمجي"
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_after = Pt(16)

    p = tf1.add_paragraph()
    p.text = "RASHAD AI Enterprise Codebase Architecture & File Walkthrough"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(148, 163, 184)

    # -------------------------------------------------------------
    # SLIDE 2: Project Root Directory Structure
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "الهيكل العام للمستودع البرمجي وتوزيع الحزم (Project Directory Tree)")
    add_cards_grid(s2, [
        ("مجلد الخادم الخلفي: backend/", [
            "app/ : قلب التطبيق البرمجي وقواعد البيانات ونماذج الـ API.",
            "core/ : إعدادات السيرفر، الاتصال بقاعدة البيانات، والتشفير والأمان.",
            "models/ : 15 نموذجاً لجدوال قاعدة البيانات عبر SQLAlchemy 2.0.",
            "services/ : محركات التقييم الذكي، فحص التكرار، والـ OCR وتعلم الآلة.",
            "api/v1/ : مسارات REST API (التوثيق، الأسر، الوثائق، التكرارات).",
            "tests/ : 22 اختباراً آلياً شاملاً للتحقق من كافة العمليات."
        ], COLOR_EMERALD),
        ("مجلد الذكاء الاصطناعي: ai/", [
            "data/synthetic/ : مجموعات البيانات الاصطناعية المعتمدة (Seed: 42).",
            "src/synthetic_generator.py : مولد الأسر والأفراد المتقدم.",
            "src/feature_engineering.py : استخراج 12 متغيراً ومؤشراً للهشاشة.",
            "src/train_models.py : سكريبت تدريب نماذج Scikit-Learn الثلاثة.",
            "models/ : النماذج المحفوظة بصيغة .joblib وتقرير الأوزان .json."
        ], COLOR_NAVY),
        ("مجلد الواجهة الأمامية: frontend/", [
            "src/components/ : واجهات العرض (الأسر، التقييم، الوثائق، التكرار).",
            "src/services/api.ts : عميل الاتصال الموحد بالخادم الخلفي.",
            "src/types/index.ts : العقود البرمجية للبيانات والـ TypeScript Interfaces.",
            "App.tsx : نقطة التجميع والتحكم العامة باللوحة.",
            "vite.config.ts & tailwind.config : إعدادات البناء والتنسيق العربي."
        ], COLOR_BLUE),
        ("مجلدات التوثيق وقواعد البيانات: docs/ & database/", [
            "docs/deployment/ : دليل التشغيل والنشر المؤسسي الشامل.",
            "docs/user-guide/ : دليل المستخدمين ومصفوفة الأدوار والصلاحيات.",
            "docs/ai-models/ : تقرير تقييم نماذج الذكاء الاصطناعي والميثاق الشرعي.",
            "database/seeds/ : سكريبتات تحميل الجغرافيا الرسمية والمستخدمين.",
            "start_rashad.bat : مشغل المنظومة التلقائي بنقرة واحدة."
        ], COLOR_GOLD),
    ], cols=2)

    # -------------------------------------------------------------
    # SLIDE 3: Backend Core Modules
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "ملفات النواة والإعدادات والأمان: backend/app/core/")
    add_cards_grid(s3, [
        ("config.py (الإعدادات العامة للبيئة)", [
            "قراءة متغيرات البيئة عبر Pydantic-Settings.",
            "ضبط مسار قاعدة بيانات PostgreSQL (postgresql+psycopg://...).",
            "تحديد المفتاح السري لتوقيع رموز JWT وخوارزمية التشفير HS256.",
            "ضبط مجلد تخزين الوثائق المعالجة (storage/documents)."
        ], COLOR_EMERALD),
        ("database.py (إدارة جلسات قاعدة البيانات)", [
            "إنشاء محرك الاتصال SQLAlchemy Engine مع ضبط Connection Pooling.",
            "إنشاء sessionmaker لإنشاء جلسات معزولة لكل طلب (SessionLocal).",
            "توفير الكيان الأساسي Declarative Base لكافة جداول المنظومة."
        ], COLOR_NAVY),
        ("security.py (التشفير وإدارة الهويات)", [
            "تشفير كلمات المرور باستخدام مكتبة bcrypt الصافية (hashpw/checkpw).",
            "توليد رموز الوصول المشفرة (create_access_token) مع ضبط زمن الانتهاء.",
            "معالجة متطلبات الأمان المؤسسي الصارم لمنع تسريب الهويات."
        ], COLOR_BLUE),
        ("deps.py (وسائط التحقق والصلاحيات - Dependencies)", [
            "دالة get_db: حقن جلسة قاعدة البيانات وغلقها التلقائي بعد انتهاء الطلب.",
            "دالة get_current_user: استخراج المستخدم من توكن الـ Bearer.",
            "دالة require_role: التحقق الصارم من صلاحيات الدور المؤسسي لكل مسار."
        ], COLOR_GOLD),
    ], cols=2)

    # -------------------------------------------------------------
    # SLIDE 4: Database Models
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "ملفات نماذج قاعدة البيانات: backend/app/models/")
    add_cards_grid(s4, [
        ("household.py (كيان الأسرة وأفرادها)", [
            "Household: رقم الملف، المعرف المستعار، اسم العائل، المسكن، الدخل.",
            "دعم المعرف المؤقت (TEMPORARY_ID) ومصدر إفادة عاقل الحارة لفاقدي الهوية.",
            "HouseholdMember: أفراد الأسرة، صلة القرابة، الحالة الصحية، والعمل.",
            "حالات السكن: RENTED, OWNED, DISPLACED_CAMP, SHARED, MAKSHA."
        ], COLOR_EMERALD),
        ("geography.py (الهيكل الإداري اليمني الرسمي)", [
            "Governorate: المحافظة (صنعاء، الأمانة، الحديدة، تعز، عدن).",
            "District: المديريات التابعة لكل محافظة.",
            "Uzlah: العزل الإدارية المعتمدة رسمياً.",
            "Village: القرى والأحياء السكنية (43 قرية وحارة محملة بالنظام)."
        ], COLOR_NAVY),
        ("needs_assessment.py (سجلات تقييم الاحتياج)", [
            "NeedsAssessment: النتيجة المحسوبة، فئة الأولوية (PriorityTier).",
            "تفصيل العوامل (JSONB Factors Breakdown) لتخزين أسباب النقاط.",
            "حقول الاعتماد البشري وملاحظات لجان المراجعة الشرعية."
        ], COLOR_BLUE),
        ("duplicate_suspicion.py & document.py", [
            "DuplicateSuspicion: حالات الاشتباه بالتكرار، نوع التطابق، ودرجة الشبه.",
            "حالة الفض: PENDING, CONFIRMED_MERGED, FALSE_POSITIVE.",
            "Document: الوثيقة المرفوعة أو المولدة ونوعها.",
            "OCRExtraction: البيانات المستخرجة آلياً، نسب الثقة، وحالة التحقق البشري."
        ], COLOR_GOLD),
    ], cols=2)

    # -------------------------------------------------------------
    # SLIDE 5: AI & Machine Learning Files
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "ملفات هندسة البيانات وتعلم الآلة: ai/src/ & ai/models/")
    add_cards_grid(s5, [
        ("feature_engineering.py (استخراج المتغيرات)", [
            "استخراج 12 متغيراً ومؤشراً إحصائياً من ملف الأسرة وأفرادها.",
            "حساب نصيب الفرد من الدخل (income_per_capita).",
            "حساب نسبة الإعالة (dependency_ratio) وعدد المرضى والمعاقين.",
            "ترميز هشاشة السكن رقمياً (المقاش 5، المخيمات 4.5، الإيجار 2)."
        ], COLOR_EMERALD),
        ("train_models.py (خط أنابيب التدريب الآلي)", [
            "تدريب نموذج العنقودية K-Means (K=4) لاكتشاف أنماط الهشاشة.",
            "تدريب نموذج Random Forest Classifier لتصنيف أولوية الاستحقاق.",
            "تدريب نموذج Random Forest Regressor للتنبؤ بحجم المساعدة النقدية.",
            "توليد تقرير الدقة والمقاييس model_metadata.json."
        ], COLOR_NAVY),
        ("ملفات النماذج المدربة (ai/models/*.joblib)", [
            "vulnerability_kmeans.joblib: نموذج العناقيد الأربعة المحفوظ.",
            "needs_random_forest.joblib: نموذج الغابات العشوائية المصنف.",
            "demand_regressor.joblib: نموذج الانحدار والتنبؤ المالي.",
            "scaler.joblib: أداة توحيد مقاييس المتغيرات القياسية StandardScaler."
        ], COLOR_BLUE),
        ("synthetic_generator.py (مولد البيانات الاصطناعية)", [
            "توليد 150 أسرة يمنية اصطناعية و761 فرداً برقم عشوائي موحد (Seed: 42).",
            "توليد أسماء يمنية رباعية واقعية وتوزيع ديموغرافي جغرافي حقيقي.",
            "حقن حالات تكرار ومقاربات لاختبار محركات كشف الازدواجية."
        ], COLOR_GOLD),
    ], cols=2)

    # -------------------------------------------------------------
    # SLIDE 6: Intelligent Backend Services
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "ملفات الخدمات ومحركات الذكاء الاصطناعي: backend/app/services/")
    add_cards_grid(s6, [
        ("needs_service.py (محرك خط الأساس الإرشادي)", [
            "خوارزمية شفافة متعددة المعايير: دخل 30%، إعالة 25%، صحة 25%، سكن 20%.",
            "توليد بطاقة تفسيرية تشرح أسباب احتساب كل نقطة للمستفيد.",
            "تضمين إشعار الحوكمة الشرعي والإداري الملزم لكل تقييم."
        ], COLOR_EMERALD),
        ("ml_service.py (خدمة تشغيل نماذج تعلم الآلة)", [
            "تحميل النماذج الثلاثة وتغذيتها ببيانات الأسرة في الوقت الفعلي.",
            "التنبؤ بفئة الأولوية ونسبة الثقة الاحتمالية (Confidence %).",
            "تحديد عنقود الهشاشة والتدخل المؤسسي الموصى به.",
            "حساب حجم المساعدة النقدية التقديرية (YER) وأهم العوامل المؤثرة."
        ], COLOR_NAVY),
        ("duplicate_service.py (محرك كشف الازدواجية)", [
            "فحص التطابق التام للرقم الوطني ورقم الهاتف المحمول.",
            "فحص التطابق الاحتمالي عبر الرموز الثلاثية (pg_trgm) ومسافة التحرير.",
            "دمج مؤشر الجوار المكاني (نفس المحافظة والمديرية) لرفع دقة الاشتباه."
        ], COLOR_BLUE),
        ("ocr_service.py (خط استخراج نصوص الوثائق)", [
            "معالجة الصور الرقمية: رفع التباين، التدرج الرمادي، والعتبة الثنائية.",
            "استخراج الحقول (الاسم، الرقم الوطني، تاريخ الميلاد) مع نسب الثقة.",
            "توليد بطاقات هوية تجريبية واقعية لأغراض الاختبار والعرض."
        ], COLOR_GOLD),
    ], cols=2)

    # -------------------------------------------------------------
    # SLIDE 7: REST API Endpoints
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "ملفات واجهات البرمجة وREST API: backend/app/api/v1/endpoints/")
    add_cards_grid(s7, [
        ("households.py (إدارة الأسر والقرى)", [
            "GET /households: استعراض الأسر مع البحث والتصفية وتجهيل المحلل.",
            "POST /households: تسجيل أسرة جديدة وتشغيل فحص التكرار التلقائي.",
            "GET /households/{id}: استرجاع الملف التفصيلي للأسرة.",
            "GET /households/geography/villages: تزويد الواجهة بقائمة القرى."
        ], COLOR_EMERALD),
        ("needs.py (تقييم الاحتياج ومقاييس الذكاء)", [
            "GET /needs/{household_id}: استرجاع التقييم المزدوج (Baseline + ML).",
            "GET /needs/metrics/ml-summary: تزويد الواجهة بتقرير دقة وأوزان النماذج.",
            "دعم اعتماد التعديلات اليدوية وملاحظات لجان المراجعة."
        ], COLOR_NAVY),
        ("duplicates.py (فض حالات الازدواجية)", [
            "GET /duplicates: استعراض سجلات الاشتباه المعلقة.",
            "POST /duplicates/{id}/resolve: اعتماد الفض والدمج البشري الثنائي.",
            "توثيق سبب القرار (تأكيد الدمج أو استبعاد الاشتباه)."
        ], COLOR_BLUE),
        ("documents.py & auth.py (الوثائق والمصادقة)", [
            "POST /documents/generate-demo/{id}: توليد وثيقة ومعالجتها بالـ OCR.",
            "POST /documents/{id}/verify: اعتماد المصادقة البشرية للوثيقة.",
            "POST /auth/login: تسجيل الدخول وتوليد رمز JWT.",
            "GET /auth/me: جلب بيانات المستخدم وصلاحياته الجغرافية."
        ], COLOR_GOLD),
    ], cols=2)

    # -------------------------------------------------------------
    # SLIDE 8: Frontend Core & App State
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "ملفات الواجهة الأمامية الأساسية: frontend/src/")
    add_cards_grid(s8, [
        ("App.tsx (المكون الرئيسي ولوحة التحكم)", [
            "إدارة الحالة العامة للتطبيق (المستخدم، الأسر، التكرارات، النوافذ).",
            "تنسيق التنقل بين تبويب الأسر وتبويب فض الازدواجية المشبوهة.",
            "معالجة انقطاع الخادم وعرض تنبيه الاتصال وإعادة المحاولة.",
            "ربط زر إضافة أسرة جديدة وزر مراجعة الوثائق وتحديث القوائم."
        ], COLOR_EMERALD),
        ("services/api.ts (عميل الـ API المركزي)", [
            "تغليف كافة طلبات fetch وإرفاق ترويسة التوثيق Bearer Token تلقائياً.",
            "دوال المصادقة، جلب الأسر، إنشاء الأسرة، وتقييم الاحتياج.",
            "دوال فض التكرار واستخراج نصوص الوثائق واعتماد المراجعة.",
            "معالجة الأخطاء وإعادتها بنصوص عربية واضحة."
        ], COLOR_NAVY),
        ("types/index.ts (عقود البيانات والـ Interfaces)", [
            "تعريف أنواع الأدوار المؤسسية (UserRole) وحالات الوثائق والسكن.",
            "واجهات HouseholdListItem, NeedsAssessmentData, MLInsights.",
            "واجهات DuplicateSuspicion, DocumentData, OCRField.",
            "ضمان تكامل الأنواع 100% بين الـ Frontend والـ Backend."
        ], COLOR_BLUE),
        ("main.tsx & index.css (التهيئة والتنسيق)", [
            "نقطة انطلاق تطبيق React 19 وتثبيت شجرة العناصر في الـ DOM.",
            "تطبيق إعدادات Tailwind CSS v4 والخطوط والاتجاه من اليمين لليسار (RTL).",
            "ضبط تدرجات الألوان المؤسسية (كحلي، زمردي، رمادي سلايت)."
        ], COLOR_GOLD),
    ], cols=2)

    # -------------------------------------------------------------
    # SLIDE 9: Frontend Interactive Components
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "ملفات مكونات واجهة المستخدم التفاعلية: frontend/src/components/")
    add_cards_grid(s9, [
        ("Header.tsx (الشريط العلوي ومبدل الأدوار)", [
            "عرض شعار المنظومة واسم المستخدم الحالي ودوره المؤسسي.",
            "شريط التبديل السريع بنقرة واحدة (Quick Switcher) بين 6 حسابات.",
            "زر تسجيل الخروج الآمن وتفريغ الجلسة."
        ], COLOR_EMERALD),
        ("HouseholdList.tsx (جدول استعراض وبحث الأسر)", [
            "شريط بحث فوري بالاسم، رقم الملف، أو الرقم الوطني.",
            "فلاتر سريعة للبطاقات الرسمية مقابل المعرفات المؤقتة.",
            "جدول تفاعلي بأزرار عرض التفسير الذكي ومعالجة الوثيقة بالـ OCR."
        ], COLOR_NAVY),
        ("NeedsModal.tsx (بطاقة التفسير الذكي المزدوج)", [
            "تبويب تنبؤات تعلم الآلة (Random Forest + K-Means + المنحة المقدرة).",
            "تبويب خط الأساس الإرشادي (شرح أوزان الدخل، الإعالة، الصحة، السكن).",
            "إبراز المبدأ الحاكم وإخلاء المسؤولية الشرعي الملزم."
        ], COLOR_BLUE),
        ("AddHouseholdModal.tsx (تسجيل أسرة جديدة)", [
            "نموذج إدخال متكامل للبيانات الشخصية، السكن، والدخل.",
            "قائمة منسدلة فورية لكافة القرى والأحياء اليمنية المعتمدة.",
            "إضافة ديناميكية لأفراد الأسرة وحالاتهم الصحية، وتشغيل التحليل فور الحفظ."
        ], COLOR_GOLD),
    ], cols=2)

    # -------------------------------------------------------------
    # SLIDE 10: Review & Verification Components
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "ملفات المراجعة الثنائية والتحقق البشري (Human-in-the-Loop UI)")
    add_cards_grid(s10, [
        ("DocumentReviewModal.tsx (شاشة مراجعة OCR)", [
            "عرض صورة الوثيقة الأصلية المحسنة في جانب.",
            "عرض الحقول المستخرجة آلياً ونسب الثقة في الجانب المقابل.",
            "تمكين الموظف من تصحيح أي حقل وكتابة ملاحظات التدقيق.",
            "زر اعتماد المصادقة لتحويل الوثيقة إلى [معتمد بشرياً]."
        ], COLOR_EMERALD),
        ("DuplicatesView.tsx (شاشة فض التكرار والازدواجية)", [
            "عرض بطاقات السجلات المشتبه بازدواجيتها جنباً إلى جنب.",
            "توضيح سبب الاشتباه (تطابق الهاتف، أو نسبة تشابه الاسم والموقع).",
            "أزرار الإجراء: تأكيد الدمج كملف واحد، أو استبعاد الاشتباه كتشابه أسماء."
        ], COLOR_NAVY),
        ("DashboardStats.tsx (لوحة المؤشرات والرسوم البيانية)", [
            "بطاقات إحصائية رئيسية: إجمالي الأسر، المعرفات المؤقتة، الحالات الحرجة.",
            "توزيع الأسر جغرافياً حسب المحافظات والمديريات.",
            "مؤشر حالات الازدواجية المعلقة ومتابعة إنجاز الفرق الميدانية."
        ], COLOR_BLUE),
        ("تطبيق مبدأ حماية البيانات والتجهيل الصارم", [
            "عند تسجيل دخول محلل البيانات (analyst)، يتم تلقائياً استبدال الأسماء والأرقام الوطنية بمعرفات مستعارة (ANON-YE-...).",
            "حظر وصول مدير النظام التقني إلى تفاصيل المستفيدين الشخصية روتينياً."
        ], COLOR_GOLD),
    ], cols=2)

    # -------------------------------------------------------------
    # SLIDE 11: Automated Test Suite Files
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "ملفات حزمة الاختبارات الآلية الشاملة: backend/tests/")
    add_cards_grid(s11, [
        ("test_health.py & test_database.py", [
            "فحص سلامة نقطة النهاية /health واستجابة الخادم.",
            "التحقق من الاتصال بقاعدة بيانات PostgreSQL وجاهزية الجداول.",
            "التأكد من تفعيل امتداد المطابقة النصية pg_trgm."
        ], COLOR_EMERALD),
        ("test_models.py & test_synthetic_data.py", [
            "اختبار إنشاء وحفظ كيانات الأسر والأفراد في قاعدة البيانات.",
            "فحص قيود المعرفات المؤقتة وإلزامية إفادة عاقل الحارة.",
            "التحقق من سلامة المولد الاصطناعي وثبات النتائج (Seed: 42)."
        ], COLOR_NAVY),
        ("test_ai_services.py & test_ml_service.py", [
            "اختبار حساب مؤشر الاحتياج الإرشادي ودقة الأوزان الأربعة.",
            "اختبار تحميل نماذج تعلم الآلة (K-Means, Random Forest, Regressor).",
            "فحص مخرجات التنبؤ والعناقيد والمنحة النقدية المقدرة."
        ], COLOR_BLUE),
        ("test_api_endpoints.py & test_ocr_pipeline.py", [
            "اختبار مسارات تسجيل الدخول، حماية الـ JWT، وتقييد الصلاحيات RBAC.",
            "اختبار إضافة أسرة جديدة وفحص التكرار التلقائي في الخلفية.",
            "اختبار خط معالجة صور الوثائق، استخراج الحقول، والمصادقة البشرية."
        ], COLOR_GOLD),
    ], cols=2)

    # -------------------------------------------------------------
    # SLIDE 12: Documentation Pack Files
    # -------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "ملفات الحزمة التوثيقية المؤسسية: docs/")
    add_cards_grid(s12, [
        ("01_deployment_and_ops_guide.md", [
            "دليل النشر والتشغيل المؤسسي على خوادم الهيئة المحلية (On-Premises).",
            "متطلبات العتاد (CPU, RAM, Storage) وخطة النسخ الاحتياطي لقاعدة البيانات.",
            "إجراءات المراقبة وحماية المنافذ وجدار الحماية."
        ], COLOR_EMERALD),
        ("02_user_and_roles_guide.md", [
            "دليل المستخدم الشامل لكل دور من الأدوار الستة.",
            "شرح سيناريوهات العمل اليومية للباحث الميداني وأخصائي التسجيل ومسؤول البرامج.",
            "مصفوفة الصلاحيات الدقيقة وحالات الاستخدام المعتمدة."
        ], COLOR_NAVY),
        ("03_model_evaluation_and_governance.md", [
            "تقرير تقييم نماذج الذكاء الاصطناعي ومقاييس الأداء التنبؤي.",
            "ميثاق الذكاء الاصطناعي المسؤول والضوابط الشرعية لعدم الحرمان الآلي.",
            "خارطة طريق تدريب نماذج التعلم العميق على بيانات الهيئة الرسمية."
        ], COLOR_BLUE),
        ("04_executive_pitch_presentation.md", [
            "العرض التقديمي التنفيذي الموجه لقيادة ومجلس إدارة الهيئة.",
            "إبراز القيمة الاستراتيجية والوفر المالي والعدالة الاجتماعية للمنظومة.",
            "مقارنة الوضع الحالي اليدوي بالوضع المستقبلي المؤتمت بالذكاء الاصطناعي."
        ], COLOR_GOLD),
    ], cols=2)

    # -------------------------------------------------------------
    # SLIDE 13: Operational Launcher
    # -------------------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "أدوات التشغيل السريع: start_rashad.bat & README.md")
    add_cards_grid(s13, [
        ("start_rashad.bat (المشغل التلقائي بنقرة واحدة)", [
            "سكريبت تشغيل دفعي مخصص لبيئة Windows.",
            "الخطوة 1: تفعيل بيئة البايثون وتشغيل خادم FastAPI على المنفذ 8000.",
            "الخطوة 2: تشغيل خادم الواجهة الأمامية React على المنفذ 5173.",
            "الخطوة 3: فتح المتصفح تلقائياً على لوحة التحكم بمجرد استقرار الخادمين."
        ], COLOR_EMERALD),
        ("README.md (الدليل الفني الرئيسي للمستودع)", [
            "توثيق شامل لما تم استخدامه في المنظومة ومواصفات كل حزمة برمجية.",
            "أوامر التشغيل اليدوية خطوة بخطوة للـ Backend والـ Frontend.",
            "جدول حسابات الدخول التجريبية لكافة الأدوار.",
            "سيناريوهات التجربة العملية المفصلة."
        ], COLOR_NAVY),
        ("database/seeds/seed_geography.py", [
            "تحميل الهيكل الجغرافي الرسمي: 5 محافظات، 12 مديرية، 13 عزلة، 43 قرية.",
            "ضمان وجود معرفات مكانية ثابتة لكافة العمليات والتحليلات."
        ], COLOR_BLUE),
        ("database/seeds/seed_users.py", [
            "تحميل المستخدمين النموذجيين الستة مع تشفير كلمات مرورهم عبر Bcrypt.",
            "ربط المستخدمين بنطاقاتهم الجغرافية وصلاحياتهم الوظيفية."
        ], COLOR_GOLD),
    ], cols=2)

    # -------------------------------------------------------------
    # SLIDE 14: Quality Metrics Summary
    # -------------------------------------------------------------
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "مؤشرات الجودة والجاهزية الفنية للنسخة الأولى MVP")

    metrics = [
        ("22 / 22", "اختبار آلي ناجح (100% Pass Rate)", "تغطية كاملة للـ API، نماذج الذكاء، واستخراج الوثائق"),
        ("560 ms", "سرعة بناء الواجهة الأمامية", "بناء فائق الكفاءة باستخدام محرك Rolldown وVite 8"),
        ("74.4%", "دقة مصنف تعلم الآلة", "دقة نموذج Random Forest في التنبؤ بفئة الاحتياج"),
        ("0.888", "معامل تحديد نموذج المنح R²", "دقة التنبؤ بحجم المساعدات النقدية المقدرة بالريال اليمني")
    ]

    for i, (val, title, desc) in enumerate(metrics):
        r = i // 2
        c = i % 2
        left = Inches(0.8 + c * 6.0)
        top_pos = Inches(1.8 + r * 2.5)

        card = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top_pos, Inches(5.7), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_BG
        card.line.color.rgb = COLOR_EMERALD
        card.line.width = Pt(1.5)

        tb = s14.shapes.add_textbox(left + Inches(0.3), top_pos + Inches(0.2), Inches(5.1), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p_v = tf.paragraphs[0]
        p_v.text = val
        p_v.font.size = Pt(28)
        p_v.font.bold = True
        p_v.font.color.rgb = COLOR_EMERALD
        p_v.space_after = Pt(4)

        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_NAVY
        p_t.space_after = Pt(4)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = COLOR_DARK_TEXT

    # -------------------------------------------------------------
    # SLIDE 15: Execution & Demonstration Guide
    # -------------------------------------------------------------
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "طريقة تشغيل وتجربة المنظومة خطوة بخطوة")

    steps = [
        ("الخيار 1: التشغيل التلقائي بنقرة واحدة (موصى به)", "الضغط المزدوج على ملف start_rashad.bat في مجلد المشروع، وسيقوم بتشغيل الخادمين وفتح المتصفح على http://localhost:5173 تلقائياً."),
        ("الخيار 2: تشغيل الخادم الخلفي يدوياً عبر CMD/PowerShell", "cd backend  -->  .\\.venv\\Scripts\\python.exe -m uvicorn app.main:app --reload --port 8000  (التوثيق التفاعلي متاح على http://localhost:8000/docs)."),
        ("الخيار 3: تشغيل الواجهة الأمامية يدوياً", "cd frontend  -->  npm run dev  (لوحة التحكم تعمل على http://localhost:5173)."),
        ("تجربة السيناريوهات الميدانية", "تسجيل أسرة جديدة، استعراض بطاقة تنبؤات الذكاء الاصطناعي، معالجة وثيقة هوية بالـ OCR والمصادقة عليها، وفض الازدواجية المشبوهة.")
    ]

    for i, (st_t, st_d) in enumerate(steps):
        top_pos = Inches(1.8 + i * 1.35)
        card = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(1.15))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_BG
        card.line.color.rgb = RGBColor(203, 213, 225)

        tb = s15.shapes.add_textbox(Inches(1.1), top_pos + Inches(0.12), Inches(11.1), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = f"🚀 {st_t}"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_EMERALD
        p_t.space_after = Pt(3)

        p_d = tf.add_paragraph()
        p_d.text = st_d
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = COLOR_DARK_TEXT

    # -------------------------------------------------------------
    # SLIDE 16: Conclusion & Institutional Readiness
    # -------------------------------------------------------------
    s16 = prs.slides.add_slide(blank_layout)
    bg16 = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg16.fill.solid()
    bg16.fill.fore_color.rgb = COLOR_NAVY
    bg16.line.fill.background()

    tb16 = s16.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11), Inches(4.5))
    tf16 = tb16.text_frame
    tf16.word_wrap = True

    p = tf16.paragraphs[0]
    p.text = "منظومة رشاد AI • جاهزية مؤسسية وتقنية كاملة"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.space_after = Pt(20)

    p = tf16.add_paragraph()
    p.text = "تم بناء وتوثيق المنظومة وفق ميثاق الذكاء الاصطناعي المسؤول والنزاهة المؤسسية، لتمثل نموذجاً تقنياً وسيادياً رائداً في خدمة مصارف الزكاة بالجمهورية اليمنية."
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_after = Pt(24)

    p = tf16.add_paragraph()
    p.text = "✔ بنية كود معيارية نظيفة  |  ✔ نماذج تعلم آلة فعالة وموثقة  |  ✔ توثيق قيادي وتنفيذي متكامل"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT

    prs.save(OUTPUT_PATH)
    print(f"Comprehensive 16-slide presentation saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_comprehensive_presentation()
