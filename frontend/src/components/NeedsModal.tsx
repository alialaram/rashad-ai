import React from 'react';
import { X, Sparkles, AlertTriangle, ShieldCheck, HeartPulse, Home, Users, DollarSign } from 'lucide-react';
import type { NeedsAssessmentData } from '../types';

interface NeedsModalProps {
  data: NeedsAssessmentData | null;
  onClose: () => void;
}

export const NeedsModal: React.FC<NeedsModalProps> = ({ data, onClose }) => {
  if (!data) return null;

  const tierColors: Record<string, { bg: string; text: string; border: string }> = {
    CRITICAL: { bg: 'bg-rose-50', text: 'text-rose-700', border: 'border-rose-200' },
    HIGH: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200' },
    MEDIUM: { bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200' },
    LOW: { bg: 'bg-slate-50', text: 'text-slate-700', border: 'border-slate-200' },
  };

  const currentTier = tierColors[data.priority_tier] || tierColors.MEDIUM;

  const factorIcons: Record<string, React.ReactNode> = {
    income_vulnerability: <DollarSign className="w-5 h-5 text-emerald-600" />,
    dependency_vulnerability: <Users className="w-5 h-5 text-blue-600" />,
    health_vulnerability: <HeartPulse className="w-5 h-5 text-rose-600" />,
    housing_vulnerability: <Home className="w-5 h-5 text-amber-600" />,
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs">
      <div className="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl border border-slate-100 p-6 animate-in fade-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-900">بطاقة التفسير التحليلي للاحتياج</h3>
              <p className="text-xs text-slate-700 font-medium">إصدار النموذج: {data.model_version}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-full transition"
            aria-label="إغلاق"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* النتيجة الإجمالية وفئة الأولوية */}
        <div className={`mt-5 p-5 rounded-2xl border ${currentTier.bg} ${currentTier.border} flex flex-col sm:flex-row items-center justify-between gap-4`}>
          <div>
            <span className="text-xs font-semibold text-slate-700">مؤشر الاحتياج الإحصائي المحسوب:</span>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-4xl font-extrabold text-slate-900">{data.calculated_score}</span>
              <span className="text-sm font-bold text-slate-700">من 100</span>
            </div>
          </div>
          <div className="text-center sm:text-left">
            <span className={`px-4 py-2 rounded-xl text-sm font-bold inline-block border ${currentTier.bg} ${currentTier.text} ${currentTier.border}`}>
              {data.tier_label_ar}
            </span>
          </div>
        </div>

        {/* تفصيل العوامل المساهمة (Explainability Breakdown) */}
        <div className="mt-6 space-y-4">
          <h4 className="text-sm font-bold text-slate-800 flex items-center gap-1.5">
            <span>العوامل المساهمة في تكوين المؤشر (الأوزان التفسيرية):</span>
          </h4>

          {Object.entries(data.factors_breakdown).map(([key, factor]) => {
            const pct = Math.round((factor.awarded_points / factor.weight_max) * 100);
            return (
              <div key={key} className="bg-slate-50 p-4 rounded-xl border border-slate-200/70">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    {factorIcons[key] || <ShieldCheck className="w-5 h-5 text-slate-500" />}
                    <span className="text-sm font-bold text-slate-900">{factor.name_ar}</span>
                  </div>
                  <div className="text-xs font-bold text-slate-700">
                    <span className="text-emerald-700">{factor.awarded_points}</span> / {factor.weight_max} نقطة ({pct}%)
                  </div>
                </div>

                {/* Progress bar */}
                <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden mb-2">
                  <div
                    className="bg-emerald-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${pct}%` }}
                  ></div>
                </div>

                <p className="text-xs text-slate-700 font-medium">{factor.reason_ar}</p>
              </div>
            );
          })}
        </div>

        {/* شارة الحوكمة والإشعار الأخلاقي والشرعي */}
        <div className="mt-6 p-4 rounded-xl bg-amber-50/80 border border-amber-200 text-xs text-amber-900 flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <div className="font-bold">المبدأ الشرعي والقانوني الحاكم:</div>
            <p className="leading-relaxed text-amber-800 font-medium">
              {data.disclaimer_text_ar}
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 pt-4 border-t border-slate-100 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2.5 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-xs font-bold transition shadow-xs"
          >
            إغلاق البطاقة
          </button>
        </div>
      </div>
    </div>
  );
};
