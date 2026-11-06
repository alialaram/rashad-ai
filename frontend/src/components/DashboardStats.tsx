import React from 'react';
import { Users, FileQuestion, Copy, AlertCircle } from 'lucide-react';
import type { HouseholdListItem, DuplicateSuspicion } from '../types';

interface DashboardStatsProps {
  households: HouseholdListItem[];
  duplicates: DuplicateSuspicion[];
  onTabChange: (tab: 'households' | 'duplicates') => void;
}

export const DashboardStats: React.FC<DashboardStatsProps> = ({
  households,
  duplicates,
  onTabChange,
}) => {
  const totalHouseholds = households.length;
  const temporaryIdCount = households.filter((h) => h.id_type === 'TEMPORARY_ID').length;
  const pendingDuplicatesCount = duplicates.filter((d) => d.resolution_status === 'PENDING').length;
  const zeroIncomeCount = households.filter((h) => h.monthly_income === 0).length;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {/* بطاقة إجمالي الأسر */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs hover:border-slate-300 transition">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-700">إجمالي الأسر المسجلة</p>
            <h3 className="text-2xl font-extrabold text-slate-900 mt-1">{totalHouseholds}</h3>
            <span className="text-[11px] text-emerald-600 font-medium">سجلات معتمدة ومحققة</span>
          </div>
          <div className="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center">
            <Users className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* بطاقة المعرفات المؤقتة */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs hover:border-slate-300 transition">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-700">فاقدو الوثائق الرسمية</p>
            <h3 className="text-2xl font-extrabold text-amber-600 mt-1">{temporaryIdCount}</h3>
            <span className="text-[11px] text-amber-700 font-medium">معرفات مؤقتة بإفادة محلية</span>
          </div>
          <div className="w-12 h-12 bg-amber-50 text-amber-600 rounded-xl flex items-center justify-center">
            <FileQuestion className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* بطاقة السجلات المشتبه بتكرارها */}
      <div
        onClick={() => onTabChange('duplicates')}
        className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs hover:border-rose-300 transition cursor-pointer group"
      >
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-700 group-hover:text-rose-600 transition">
              اشتباه تكرار قيد المراجعة
            </p>
            <h3 className="text-2xl font-extrabold text-rose-600 mt-1">{pendingDuplicatesCount}</h3>
            <span className="text-[11px] text-rose-700 font-medium">تتطلب اعتماداً ثنائياً</span>
          </div>
          <div className="w-12 h-12 bg-rose-50 text-rose-600 rounded-xl flex items-center justify-center group-hover:scale-105 transition">
            <Copy className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* بطاقة الأسر معدومة الدخل */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs hover:border-slate-300 transition">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-700">أسر معدومة الدخل (0 ريال)</p>
            <h3 className="text-2xl font-extrabold text-slate-900 mt-1">{zeroIncomeCount}</h3>
            <span className="text-[11px] text-purple-600 font-medium">أولوية قصوى لتدخل المصارف</span>
          </div>
          <div className="w-12 h-12 bg-purple-50 text-purple-600 rounded-xl flex items-center justify-center">
            <AlertCircle className="w-6 h-6" />
          </div>
        </div>
      </div>
    </div>
  );
};
