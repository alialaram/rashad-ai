# RASHAD AI -- رشاد AI
## منظومة الذكاء الاصطناعي لإدارة وتحليل الاحتياج الزكوي وتوجيه الموارد

> **حالة المشروع:** `قيد التحليل والتجهيز (Phase 2 - Development Setup)`  
> **الجهة المستهدفة:** الهيئة العامة للزكاة -- الجمهورية اليمنية  
> **طبيعة المنتج:** منصة ويب مؤسسية لدعم اتخاذ القرار والتحليل الإحصائي المساند.

---

### المبدأ الحاكم للمنصة
المنصة **أداة دعم قرار وتحليل إحصائي مساند**، وليست جهة تصدر أحكاماً شرعية أو قانونية، ولا تتخذ قرارات قبول أو رفض أو حرمان المستفيد بصورة آلية. تظل القرارات النهائية بيد اللجان والمختصين البشريين وفق الضوابط واللوائح المعتمدة رسمياً.

---

### الهيكل التنظيمي للمستودع
```text
rashad-ai/
├── backend/            # FastAPI REST API, SQLAlchemy, Pydantic, Security
├── frontend/           # React 18+, TypeScript, Vite, Tailwind CSS (RTL)
├── ai/                 # Synthetic Data Generators, Rule Engines, OCR Pipelines
├── database/           # Migrations (Alembic), Schemas, Geographic Seeds
├── docs/               # Requirements, Architecture, Data Dictionary, Guides
├── storage/            # Local protected sandbox for documents
├── .env.example        # Environment configuration template
├── .gitignore          # Version control ignore rules
└── README.md           # Project Documentation
```

---

### متطلبات التشغيل الأساسية (Prerequisites)
- **Python:** 3.12+ (النظام الحالي: Python 3.14)
- **Node.js:** 20+ (النظام الحالي: Node 24.15)
- **PostgreSQL:** 16+ (النظام الحالي: PostgreSQL 18.6)
- **Git:** 2.40+

---

### سياسة البيانات والخصوصية
- لا تُستخدم أي بيانات حقيقية أو شخصية في هذه المرحلة.
- جميع بيانات التطوير والاختبار هي **بيانات اصطناعية مولدة برمجياً (Synthetic Data)** برقم عشوائي ثابت (Seed: 42).
- تخضع بيانات المستفيدين لمبدأ الحماية الصارمة وتجهيل الهويات للتحليلات الإحصائية.
