# دليل التشغيل والتثبيت الفني (Deployment & Operations Guide)
## منظومة رشاد AI -- الهيئة العامة للزكاة

> **النسخة:** `0.1.0-alpha (MVP Prototype)`  
> **حالة المنظومة:** منفذة ومختبرة محلياً ببيانات اصطناعية 100%.

---

## 1. المتطلبات البرمجية للبنية التحتية (System Prerequisites)

* **نظام التشغيل:** Windows 10/11 أو Linux (Ubuntu 22.04 LTS+ / Debian 12).
* **خادم قواعد البيانات:** PostgreSQL 16+ (تم الاختبار بنجاح على PostgreSQL 18.6).
* **لغة الواجهة الخلفية:** Python 3.12+ (تم الاختبار بنجاح على Python 3.14).
* **بيئة الواجهة الأمامية:** Node.js 20+ (تم الاختبار بنجاح على Node.js 24.15) مع npm.
* **إدارة الإصدارات:** Git 2.40+.

---

## 2. خطوات التثبيت والإعداد من الصفر (Step-by-Step Setup)

### الخطوة 1: استنساخ المستودع وتجهيز المتغيرات البيئية
```bash
git clone <repository-url> rashad-ai
cd rashad-ai

# إنشاء ملف البيئة من القالب
cp .env.example .env
```
*قم بتعديل قيم `.env` الخاصة برابط قاعدة البيانات ومفتاح التشفير `SECRET_KEY`.*

### الخطوة 2: تهيئة قاعدة بيانات PostgreSQL
افتح طرفية PostgreSQL وأنشئ قاعدة البيانات والإضافات المطلوبة:
```sql
CREATE DATABASE rashad_ai_dev;
\c rashad_ai_dev
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

### الخطوة 3: تجهيز بيئة الـ Backend
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # على ويندوز (أو source .venv/bin/activate على لينكس)
pip install -r requirements.txt
pip install pillow
```

### الخطوة 4: بذر البيانات الأولية (Seeding)
```powershell
# 1. بذر التقسيم الجغرافي اليمني (محافظات، مديريات، عزل، قرى)
python ../database/seeds/seed_geography.py

# 2. إنشاء وبذر المستخدمين الافتراضيين للأدوار الستة
python ../database/seeds/seed_users.py

# 3. توليد 150 أسرة اصطناعية متنوعة مع حالات التكرار للاختبار
python ../ai/src/synthetic_generator.py
```

### الخطوة 5: التحقق من نجاح الاختبارات الآلية
```powershell
pytest tests -v
# النتيجة المتوقعة: 19 passed in ~3.8s
```

### الخطوة 6: تجهيز وبناء الواجهة الأمامية (Frontend)
```powershell
cd ../frontend
npm install
npm run build
```

---

## 3. تشغيل المنظومة محلياً (Running Services)

### تشغيل الواجهة الخلفية (Backend API)
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
* التوثيق التفاعلي Swagger: `http://127.0.0.1:8000/api/v1/docs`

### تشغيل الواجهة الأمامية (Frontend UI)
```powershell
cd frontend
npm run dev
```
* رابط المنظومة التفاعلية: `http://localhost:5173`

---

## 4. إرشادات الانتقال إلى بيئة الإنتاج المؤسسية (Production Hardening)

1. **الخادم العكسي (Reverse Proxy):** تشغيل `Nginx` مع ضبط التوجيه التلقائي لـ SSL/TLS، وضبط `Strict-Transport-Security` و `X-Frame-Options: DENY`.
2. **عزل مستودع الوثائق:** تخزين الوثائق في وسيط تخزين مشفر (S3 متوافق أو مجلد محمي بنظام أذونات POSIX 700) وعدم إتاحة الملفات مباشرة إلا عبر روابط موقوتة ومصادق عليها.
3. **الحماية من الهجمات:** تفعيل `Rate Limiting` على مسار تسجيل الدخول `/api/v1/auth/login` لمنع هجمات التخمين.
4. **النسخ الاحتياطي:** ضبط جدول زمني (Cron) لعمل `pg_dump` يومي لقاعدة البيانات وتشفير ملفات النسخ ونقلها لموقع معزول (Offsite Backup).
