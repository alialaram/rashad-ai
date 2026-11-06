import React from 'react';
import { ShieldCheck, LogOut, AlertTriangle } from 'lucide-react';
import type { AuthResponse } from '../types';

interface HeaderProps {
  currentUser: AuthResponse | null;
  onLogout: () => void;
  onQuickRoleSwitch: (username: string) => void;
}

export const Header: React.FC<HeaderProps> = ({
  currentUser,
  onLogout,
  onQuickRoleSwitch,
}) => {
  const roleLabels: Record<string, { label: string; color: string }> = {
    SYSTEM_ADMIN: { label: 'مدير النظام التقني', color: 'bg-purple-100 text-purple-800 border-purple-200' },
    FIELD_RESEARCHER: { label: 'باحث ميداني (صنعاء)', color: 'bg-blue-100 text-blue-800 border-blue-200' },
    BENEFICIARY_OFFICER: { label: 'موظف تسجيل مستفيدين', color: 'bg-emerald-100 text-emerald-800 border-emerald-200' },
    PROGRAMS_OFFICER: { label: 'موظف البرامج والمساعدات', color: 'bg-amber-100 text-amber-800 border-amber-200' },
    AUDITOR: { label: 'مدقق ومراجع رقابي', color: 'bg-rose-100 text-rose-800 border-rose-200' },
    DATA_ANALYST: { label: 'محلل بيانات (بيانات مجهلة)', color: 'bg-cyan-100 text-cyan-800 border-cyan-200' },
  };

  const currentRoleInfo = currentUser
    ? roleLabels[currentUser.role] || { label: currentUser.role, color: 'bg-slate-100 text-slate-800 border-slate-200' }
    : null;

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-xs">
      {/* شريط الإشعار المؤسسي وإخلاء المسؤولية */}
      <div className="bg-amber-50 border-b border-amber-200 px-4 py-1.5 text-xs text-amber-900 flex items-center justify-between">
        <div className="flex items-center gap-1.5 font-medium">
          <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
          <span>
            <strong>منصة مؤسسية تجريبية:</strong> جميع البيانات المعروضة اصطناعية 100% لأغراض التقييم والنمذجة -- مخرجات الذكاء الاصطناعي استرشادية ولا تمثل حكماً شرعياً أو قانونياً.
          </span>
        </div>
        <span className="hidden md:inline-block px-2 py-0.5 bg-amber-200 text-amber-900 rounded-full font-bold text-[10px]">
          DEMO v0.1.0-alpha
        </span>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        {/* الشعار والهوية */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-700 to-teal-500 flex items-center justify-center text-white shadow-md shadow-emerald-700/20">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-slate-900 tracking-tight">رشاد AI</h1>
              <span className="text-xs px-2 py-0.5 bg-emerald-50 text-emerald-700 rounded-md font-semibold border border-emerald-200">
                RASHAD AI
              </span>
            </div>
            <p className="text-xs text-slate-700 font-medium hidden sm:block">
              منظومة الذكاء الاصطناعي لإدارة وتحليل الاحتياج الزكوي وتوجيه الموارد
            </p>
          </div>
        </div>

        {/* معلومات المستخدم ومبدل الأدوار السريع */}
        {currentUser && (
          <div className="flex items-center gap-3">
            {/* مبدل الأدوار السريع للتجربة */}
            <div className="hidden lg:flex items-center gap-1 text-xs">
              <span className="text-slate-700 font-medium ml-1">تجربة دور:</span>
              <button
                onClick={() => onQuickRoleSwitch('admin')}
                className={`px-2 py-1 rounded transition text-xs ${currentUser.username === 'admin' ? 'bg-purple-600 text-white font-bold' : 'bg-slate-100 hover:bg-slate-200 text-slate-700'}`}
              >
                مدير النظام
              </button>
              <button
                onClick={() => onQuickRoleSwitch('beneficiary_officer')}
                className={`px-2 py-1 rounded transition text-xs ${currentUser.username === 'beneficiary_officer' ? 'bg-emerald-600 text-white font-bold' : 'bg-slate-100 hover:bg-slate-200 text-slate-700'}`}
              >
                موظف تسجيل
              </button>
              <button
                onClick={() => onQuickRoleSwitch('researcher_sanaa')}
                className={`px-2 py-1 rounded transition text-xs ${currentUser.username === 'researcher_sanaa' ? 'bg-blue-600 text-white font-bold' : 'bg-slate-100 hover:bg-slate-200 text-slate-700'}`}
              >
                باحث ميداني
              </button>
              <button
                onClick={() => onQuickRoleSwitch('programs_officer')}
                className={`px-2 py-1 rounded transition text-xs ${currentUser.username === 'programs_officer' ? 'bg-amber-600 text-white font-bold' : 'bg-slate-100 hover:bg-slate-200 text-slate-700'}`}
              >
                موظف برامج
              </button>
              <button
                onClick={() => onQuickRoleSwitch('auditor')}
                className={`px-2 py-1 rounded transition text-xs ${currentUser.username === 'auditor' ? 'bg-rose-600 text-white font-bold' : 'bg-slate-100 hover:bg-slate-200 text-slate-700'}`}
              >
                مدقق
              </button>
              <button
                onClick={() => onQuickRoleSwitch('analyst')}
                className={`px-2 py-1 rounded transition text-xs ${currentUser.username === 'analyst' ? 'bg-cyan-600 text-white font-bold' : 'bg-slate-100 hover:bg-slate-200 text-slate-700'}`}
              >
                محلل بيانات
              </button>
            </div>

            {/* الحساب الحالي */}
            <div className="flex items-center gap-2 pr-3 border-r border-slate-200">
              <div className="text-right hidden sm:block">
                <div className="text-xs font-bold text-slate-800">{currentUser.full_name}</div>
                <div className={`text-[10px] px-2 py-0.5 rounded-full inline-block font-semibold border ${currentRoleInfo?.color}`}>
                  {currentRoleInfo?.label}
                </div>
              </div>
              <button
                onClick={onLogout}
                title="تسجيل الخروج"
                aria-label="تسجيل الخروج"
                className="p-2 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};
