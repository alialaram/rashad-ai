@echo off
chcp 65001 >nul
echo ========================================================
echo        تشغيل منظومة رشاد AI - الهيئة العامة للزكاة
echo ========================================================
echo.
echo [1/2] جاري تشغيل الخادم الخلفي (Backend - FastAPI)...
start "RASHAD AI - Backend API" cmd /k "cd /d %~dp0backend && .venv\Scripts\activate && uvicorn app.main:app --reload --port 8000"

echo انتظر ثوانٍ لتهيئة الخادم...
timeout /t 3 /nobreak >nul

echo [2/2] جاري تشغيل الواجهة الأمامية (Frontend - React)...
start "RASHAD AI - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo انتظر ثوانٍ لفتح لوحة التحكم...
timeout /t 2 /nobreak >nul

echo جاري فتح المتصفح على لوحة التحكم...
start http://localhost:5173

echo.
echo ========================================================
echo  تم تشغيل المنظومة بنجاح!
echo  الواجهة الأمامية: http://localhost:5173
echo  توثيق الـ API:     http://localhost:8000/docs
echo ========================================================
pause
