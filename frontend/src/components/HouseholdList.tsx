import React, { useState } from 'react';
import { Search, Filter, Sparkles, ShieldAlert, FileText, CheckCircle2 } from 'lucide-react';
import type { HouseholdListItem } from '../types';

interface HouseholdListProps {
  households: HouseholdListItem[];
  isLoading: boolean;
  onSearch: (term: string) => void;
  onFilterIdType: (type: string) => void;
  onInspectNeeds: (householdId: string) => void;
  selectedIdType: string;
}

export const HouseholdList: React.FC<HouseholdListProps> = ({
  households,
  isLoading,
  onSearch,
  onFilterIdType,
  onInspectNeeds,
  selectedIdType,
}) => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
    onSearch(e.target.value);
  };

  const housingLabels: Record<string, string> = {
    RENTED: 'مستأجر',
    OWNED: 'ملك',
    DISPLACED_CAMP: 'مخيم نزوح',
    SHARED: 'مشترك',
    MAKSHA: 'مقشة/عشوائي',
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-hidden">
      {/* Search and Filters Bar */}
      <div className="p-4 sm:p-5 border-b border-slate-100 flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-50/50">
        <div className="relative flex-1 max-w-md">
          <Search className="w-4 h-4 text-slate-400 absolute right-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchTerm}
            onChange={handleSearchChange}
            placeholder="بحث بالاسم، رقم الملف، أو رقم الهوية..."
            className="w-full pl-4 pr-10 py-2.5 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-hidden focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition"
          />
        </div>

        {/* Filter Chips */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1 md:pb-0 text-xs">
          <span className="text-slate-400 text-xs flex items-center gap-1 shrink-0">
            <Filter className="w-3.5 h-3.5" />
            تصفية:
          </span>
          <button
            onClick={() => onFilterIdType('')}
            className={`px-3 py-1.5 rounded-lg font-medium transition shrink-0 ${!selectedIdType ? 'bg-slate-900 text-white font-bold' : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'}`}
          >
            الكل ({households.length})
          </button>
          <button
            onClick={() => onFilterIdType('NATIONAL_ID')}
            className={`px-3 py-1.5 rounded-lg font-medium transition shrink-0 ${selectedIdType === 'NATIONAL_ID' ? 'bg-emerald-700 text-white font-bold' : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'}`}
          >
            بطاقة شخصية
          </button>
          <button
            onClick={() => onFilterIdType('TEMPORARY_ID')}
            className={`px-3 py-1.5 rounded-lg font-medium transition shrink-0 ${selectedIdType === 'TEMPORARY_ID' ? 'bg-amber-600 text-white font-bold' : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'}`}
          >
            معرف مؤقت (فاقدو الوثائق)
          </button>
        </div>
      </div>

      {/* Households Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-right text-xs">
          <thead className="bg-slate-50 text-slate-700 font-bold border-b border-slate-200/80">
            <tr>
              <th className="px-5 py-3.5">رقم الملف</th>
              <th className="px-5 py-3.5">اسم رب الأسرة</th>
              <th className="px-5 py-3.5">نوع الهوية والرقم</th>
              <th className="px-5 py-3.5">حالة التحقق</th>
              <th className="px-5 py-3.5">المسكن</th>
              <th className="px-5 py-3.5">الدخل الشهري</th>
              <th className="px-5 py-3.5">الأفراد</th>
              <th className="px-5 py-3.5 text-center">دعم القرار (الذكاء الاصطناعي)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 font-medium">
            {isLoading ? (
              <tr>
                <td colSpan={8} className="text-center py-12 text-slate-400">
                  جاري تحميل البيانات...
                </td>
              </tr>
            ) : households.length === 0 ? (
              <tr>
                <td colSpan={8} className="text-center py-12 text-slate-400">
                  لا توجد نتائج مطابقة لشروط البحث
                </td>
              </tr>
            ) : (
              households.map((h) => (
                <tr key={h.id} className="hover:bg-slate-50/70 transition">
                  {/* رقم الملف والمعرف المستعار */}
                  <td className="px-5 py-4 whitespace-nowrap">
                    <div className="font-bold text-slate-900">{h.file_number}</div>
                    <div className="text-[10px] text-slate-400 font-mono mt-0.5">{h.pseudo_id}</div>
                  </td>

                  {/* اسم رب الأسرة */}
                  <td className="px-5 py-4 whitespace-nowrap">
                    {h.head_full_name === '[مستفيد مجهل الهوية]' ? (
                      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-100 text-slate-600 text-xs font-mono">
                        <ShieldAlert className="w-3.5 h-3.5 text-slate-400" />
                        {h.head_full_name}
                      </span>
                    ) : (
                      <span className="font-semibold text-slate-800">{h.head_full_name}</span>
                    )}
                  </td>

                  {/* نوع الهوية والرقم */}
                  <td className="px-5 py-4 whitespace-nowrap">
                    <div className="flex items-center gap-1.5">
                      {h.id_type === 'TEMPORARY_ID' ? (
                        <span className="px-2 py-0.5 rounded-md bg-amber-50 text-amber-700 text-[10px] font-bold border border-amber-200">
                          معرف مؤقت
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 text-[10px] font-bold border border-emerald-200">
                          رقم وطني
                        </span>
                      )}
                      <span className="font-mono text-slate-600 text-xs">{h.id_number}</span>
                    </div>
                  </td>

                  {/* حالة التحقق */}
                  <td className="px-5 py-4 whitespace-nowrap">
                    {h.id_verification_status === 'VERIFIED_OFFICIAL' && (
                      <span className="text-emerald-700 flex items-center gap-1 text-[11px]">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        رسمي محقق
                      </span>
                    )}
                    {h.id_verification_status === 'LOCAL_ATTESTATION' && (
                      <span className="text-amber-700 flex items-center gap-1 text-[11px]">
                        <FileText className="w-3.5 h-3.5" />
                        إفادة عاقل الحارة
                      </span>
                    )}
                    {h.id_verification_status === 'PENDING_REVIEW' && (
                      <span className="text-slate-700 text-[11px]">قيد المراجعة</span>
                    )}
                  </td>

                  {/* نوع السكن */}
                  <td className="px-5 py-4 whitespace-nowrap text-slate-600">
                    {housingLabels[h.housing_type] || h.housing_type}
                  </td>

                  {/* الدخل */}
                  <td className="px-5 py-4 whitespace-nowrap">
                    {h.monthly_income === 0 ? (
                      <span className="text-rose-600 font-bold">0 ريال (معدوم)</span>
                    ) : (
                      <span className="text-slate-800">{h.monthly_income.toLocaleString()} ريال</span>
                    )}
                  </td>

                  {/* الأفراد */}
                  <td className="px-5 py-4 whitespace-nowrap text-slate-600">
                    {h.members_count} أفراد
                  </td>

                  {/* زر فحص مؤشر الاحتياج */}
                  <td className="px-5 py-4 whitespace-nowrap text-center">
                    <button
                      onClick={() => onInspectNeeds(h.id)}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-purple-50 hover:bg-purple-100 text-purple-700 rounded-xl text-xs font-bold border border-purple-200 transition shadow-2xs"
                    >
                      <Sparkles className="w-3.5 h-3.5 text-purple-600" />
                      فحص مؤشر الاحتياج
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
