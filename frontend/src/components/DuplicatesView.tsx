import React, { useState } from 'react';
import { Copy, CheckCircle2, XCircle, ShieldCheck } from 'lucide-react';
import type { DuplicateSuspicion } from '../types';

interface DuplicatesViewProps {
  duplicates: DuplicateSuspicion[];
  onResolve: (
    id: string,
    status: 'CONFIRMED_MERGED' | 'FALSE_POSITIVE',
    reason: string,
    primaryId?: string
  ) => Promise<void>;
}

export const DuplicatesView: React.FC<DuplicatesViewProps> = ({
  duplicates,
  onResolve,
}) => {
  const [selectedSuspicion, setSelectedSuspicion] = useState<DuplicateSuspicion | null>(null);
  const [resolutionType, setResolutionType] = useState<'CONFIRMED_MERGED' | 'FALSE_POSITIVE'>('FALSE_POSITIVE');
  const [reason, setReason] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const pendingDuplicates = duplicates.filter((d) => d.resolution_status === 'PENDING');

  const matchTypeLabels: Record<string, { label: string; color: string }> = {
    EXACT_NATIONAL_ID: { label: 'تطابق قطعي بالرقم الوطني', color: 'bg-rose-100 text-rose-800 border-rose-300' },
    EXACT_PHONE: { label: 'تطابق قطعي برقم الهاتف', color: 'bg-amber-100 text-amber-800 border-amber-300' },
    FUZZY_NAME_GEO: { label: 'تشابه احتمالي بالاسم والجوار المكاني', color: 'bg-blue-100 text-blue-800 border-blue-300' },
  };

  const handleOpenResolve = (susp: DuplicateSuspicion, type: 'CONFIRMED_MERGED' | 'FALSE_POSITIVE') => {
    setSelectedSuspicion(susp);
    setResolutionType(type);
    setReason(
      type === 'CONFIRMED_MERGED'
        ? 'تم التحقق من تطابق هوية الأسرة وثبوت الازدواجية في القيد، واعتماد السجل الأول كسجل أساسي.'
        : 'تم النزول الميداني والمراجعة، وثبت اختلاف الشخصين والأسرتين شرعاً وواقعاً.'
    );
  };

  const handleSubmitResolution = async () => {
    if (!selectedSuspicion) return;
    if (reason.trim().length < 15) {
      alert('يجب كتابة مسوغ بشري تفصيلي لا يقل عن 15 حرفاً.');
      return;
    }

    setIsSubmitting(true);
    try {
      await onResolve(
        selectedSuspicion.id,
        resolutionType,
        reason,
        selectedSuspicion.source_household_id
      );
      setSelectedSuspicion(null);
    } catch (e: any) {
      alert(e.message || 'فشلت معالجة الاشتباه');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* رأس الصفحة والإشعار الرقابي */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <Copy className="w-5 h-5 text-rose-600" />
            <h2 className="text-lg font-bold text-slate-900">مراجعة السجلات المشتبه بازدواجيتها</h2>
          </div>
          <p className="text-xs text-slate-700 font-medium mt-1">
            نظام الكشف الآلي يرصد التطابق القطعي والاحتمالي، وتظل قرارات الدمج خاضعة للاعتماد البشري والرقابي الثنائي.
          </p>
        </div>
        <div className="px-4 py-2 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-xs font-bold">
          حالات قيد البت: {pendingDuplicates.length} حالة
        </div>
      </div>

      {/* قائمة بطاقات المقارنة الثنائية */}
      {pendingDuplicates.length === 0 ? (
        <div className="bg-white p-12 text-center rounded-2xl border border-slate-200 text-slate-400 text-xs">
          لا توجد حالات اشتباه تكرار معلقة حالياً
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6">
          {pendingDuplicates.map((susp) => {
            const matchInfo = matchTypeLabels[susp.match_type] || {
              label: susp.match_type,
              color: 'bg-slate-100 text-slate-800 border-slate-200',
            };

            return (
              <div
                key={susp.id}
                className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden"
              >
                {/* شريط نوع التطابق ودرجة التشابه */}
                <div className="px-6 py-3.5 bg-slate-50 border-b border-slate-200 flex flex-wrap items-center justify-between gap-3">
                  <div className="flex items-center gap-2">
                    <span className={`px-3 py-1 rounded-lg text-xs font-bold border ${matchInfo.color}`}>
                      {matchInfo.label}
                    </span>
                    <span className="text-xs text-slate-700 font-semibold">
                      درجة التشابه المحسوبة: <strong className="text-slate-900">{susp.similarity_score}%</strong>
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleOpenResolve(susp, 'CONFIRMED_MERGED')}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-bold transition shadow-xs"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      تأكيد الدمج والازدواجية
                    </button>
                    <button
                      onClick={() => handleOpenResolve(susp, 'FALSE_POSITIVE')}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white hover:bg-slate-100 text-slate-700 border border-slate-300 rounded-lg text-xs font-bold transition"
                    >
                      <XCircle className="w-3.5 h-3.5 text-slate-400" />
                      إقرار اختلاف الشخصين (إنكار التطابق)
                    </button>
                  </div>
                </div>

                {/* عرض المقارنة الثنائية للبيانات */}
                <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6 bg-slate-50/30">
                  {/* السجل المصدر الأول */}
                  <div className="bg-white p-5 rounded-xl border border-slate-200/80">
                    <div className="flex items-center justify-between border-b border-slate-100 pb-2 mb-3">
                      <span className="text-xs font-bold text-slate-500">السجل المصدر (الملف الأول)</span>
                      <span className="text-xs font-mono font-bold text-slate-800">
                        {susp.match_details.source || 'ملف رقمي'}
                      </span>
                    </div>
                    <div className="space-y-2 text-xs">
                      <div>
                        <span className="text-slate-400">اسم المستفيد:</span>{' '}
                        <strong className="text-slate-900">{susp.match_details.source_name || 'سالم علي محمد'}</strong>
                      </div>
                      <div>
                        <span className="text-slate-400">القيمة المطابقة:</span>{' '}
                        <span className="font-mono bg-amber-50 text-amber-900 px-2 py-0.5 rounded border border-amber-200">
                          {susp.match_details.matched_value || susp.match_details.reason || 'تطابق نصي'}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* السجل المرشح المقارن به */}
                  <div className="bg-white p-5 rounded-xl border border-slate-200/80">
                    <div className="flex items-center justify-between border-b border-slate-100 pb-2 mb-3">
                      <span className="text-xs font-bold text-slate-500">السجل المرشح (الملف الثاني المقارن)</span>
                      <span className="text-xs font-mono font-bold text-slate-800">
                        {susp.match_details.candidate || 'ملف رقمي'}
                      </span>
                    </div>
                    <div className="space-y-2 text-xs">
                      <div>
                        <span className="text-slate-400">اسم المستفيد المقارن:</span>{' '}
                        <strong className="text-slate-900">{susp.match_details.candidate_name || 'سالم علي محمد'}</strong>
                      </div>
                      <div>
                        <span className="text-slate-400">سبب الاشتباه:</span>{' '}
                        <span className="font-medium text-slate-700">
                          {susp.match_details.reason_ar || 'تم رصد تقارب كبير في المعرفات الميدانية'}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Modal البت والاعتماد البشري */}
      {selectedSuspicion && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-100">
            <h3 className="text-base font-bold text-slate-900 mb-2 flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-emerald-600" />
              {resolutionType === 'CONFIRMED_MERGED' ? 'اعتماد الدمج المنطقي للازدواجية' : 'إقرار عدم التطابق (False Positive)'}
            </h3>
            <p className="text-xs text-slate-500 mb-4 leading-relaxed">
              وفق سياسة الحوكمة والنزاهة، يجب تدوين مسوغ بشري تفصيلي يوضح أسباب القرار لتثبيته في سجل التدقيق الرقابي غير القابل للتعديل.
            </p>

            <div className="space-y-3">
              <label className="text-xs font-bold text-slate-700 block">
                المسوغ والمبرر البشري المعتمد (إلزامي):
              </label>
              <textarea
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                rows={3}
                placeholder="اكتب أسباب القرار ونتائج المراجعة الميدانية..."
                className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-hidden focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500"
              ></textarea>
            </div>

            <div className="mt-6 flex items-center justify-end gap-2">
              <button
                onClick={() => setSelectedSuspicion(null)}
                className="px-4 py-2 text-xs font-bold text-slate-600 hover:bg-slate-100 rounded-xl transition"
              >
                إلغاء
              </button>
              <button
                disabled={isSubmitting}
                onClick={handleSubmitResolution}
                className="px-5 py-2 bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold rounded-xl transition shadow-xs"
              >
                {isSubmitting ? 'جاري الحفظ...' : 'تثبيت القرار في السجل الرقابي'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
