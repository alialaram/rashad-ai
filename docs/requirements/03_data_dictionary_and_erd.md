# Data Dictionary & Entity Relationship Diagram (ERD)
## قاموس البيانات ومخطط العلاقات الكينونية - رشاد AI

### الهيكل الكينوني
```mermaid
erDiagram
    GOVERNORATES ||--o{ DISTRICTS : "contains"
    DISTRICTS ||--o{ UZLAHS : "contains"
    UZLAHS ||--o{ VILLAGES : "contains"

    USERS ||--o{ USER_SCOPES : "assigned"
    DISTRICTS ||--o{ USER_SCOPES : "covers"

    USERS ||--o{ AUDIT_LOGS : "performs"
    USERS ||--o{ ASSISTANCE_REQUESTS : "manages"

    VILLAGES ||--o{ HOUSEHOLDS : "located_in"
    HOUSEHOLDS ||--o{ HOUSEHOLD_MEMBERS : "includes"
    HOUSEHOLDS ||--o{ DOCUMENTS : "owns"
    HOUSEHOLDS ||--o{ ASSISTANCE_REQUESTS : "submits"
    HOUSEHOLDS ||--o{ NEEDS_ASSESSMENTS : "evaluated_by"

    HOUSEHOLDS ||--o{ DUPLICATE_SUSPICIONS : "source_household"
    HOUSEHOLDS ||--o{ DUPLICATE_SUSPICIONS : "matched_household"

    ASSISTANCE_REQUESTS ||--o{ REQUEST_APPROVALS : "reviewed_by"
    DOCUMENTS ||--o{ OCR_EXTRACTIONS : "processed_by"
```

### الجداول الأساسية المعتمدة
1. `governorates`: المحافظات اليمنية.
2. `districts`: المديريات التابعة لكل محافظة.
3. `uzlahs`: العزل الإدارية.
4. `villages`: القرى والأحياء والحارات.
5. `users`: المستخدمين والموظفين والباحثين.
6. `user_scopes`: النطاق الجغرافي المصرح به لكل موظف.
7. `households`: الأسر والمستفيدين مع دعم المعرفات المؤقتة والمعرفات التحليلية المستعارة (Pseudo IDs).
8. `household_members`: أفراد الأسرة وصلة القرابة والحالة الصحية والتعليمية والعمل.
9. `documents`: وثائق الإثبات المرفوعة ومساراتها المحمية.
10. `ocr_extractions`: نتائج استخراج النصوص العربية ونسب الثقة وحالة التحقق البشري.
11. `needs_assessments`: مؤشرات الاحتياج المحسوبة والعوامل التفسيرية والشارة الاسترشادية.
12. `duplicate_suspicions`: حالات الاشتباه بالازدواجية والتكرار ونسب التشابه والاعتماد الثنائي للدمج.
13. `assistance_requests`: طلبات المساعدات ومصارف الزكاة المستهدفة وحالة الطلب.
14. `request_approvals`: سجل التوصيات والاعتمادات المتسلسلة أو اللجانية.
15. `audit_logs`: سجل التدقيق المحمي غير القابل للتعديل أو الحذف (Append-Only).
