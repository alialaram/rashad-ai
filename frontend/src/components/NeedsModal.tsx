import React, { useState } from 'react';
import {
  X,
  Sparkles,
  AlertTriangle,
  ShieldCheck,
  HeartPulse,
  Home,
  Users,
  DollarSign,
  BrainCircuit,
  Layers,
  TrendingUp,
  Sliders,
} from 'lucide-react';
import type { NeedsAssessmentData } from '../types';

interface NeedsModalProps {
  data: NeedsAssessmentData | null;
  onClose: () => void;
}

export const NeedsModal: React.FC<NeedsModalProps> = ({ data, onClose }) => {
  const [activeTab, setActiveTab] = useState<'baseline' | 'ml'>('ml');

  if (!data) return null;

  const tierColors: Record<string, { bg: string; text: string; border: string }> = {
    CRITICAL: { bg: 'bg-rose-50', text: 'text-rose-700', border: 'border-rose-200' },
    HIGH: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200' },
    MEDIUM: { bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200' },
    LOW: { bg: 'bg-slate-50', text: 'text-slate-700', border: 'border-slate-200' },
  };

  const currentTier = tierColors[data.priority_tier] || tierColors.MEDIUM;
  const ml = data.ml_insights;
  const mlTierColor = ml?.predicted_tier ? (tierColors[ml.predicted_tier] || tierColors.MEDIUM) : currentTier;

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
              <h3 className="text-lg font-bold text-slate-900">بطاقة التفسير الذكي ومؤشرات الاحتياج</h3>
              <p className="text-xs text-slate-700 font-medium">
                محرك التقييم: {data.model_version} {ml?.status === 'AVAILABLE' && '• مدعوم بنماذج ML متزامنة'}
              </p>
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

        {/* View Switcher Tabs */}
        <div className="flex gap-2 mt-4 p-1 bg-slate-100 rounded-xl">
          <button
            onClick={() => setActiveTab('ml')}
            className={`flex-1 py-2 rounded-lg text-xs font-bold flex items-center justify-center gap-2 transition ${
              activeTab === 'ml'
                ? 'bg-white text-purple-700 shadow-xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <BrainCircuit className="w-4 h-4" />
            <span>تنبؤات وعناقيد تعلم الآلة (ML Intelligence)</span>
          </button>
          <button
            onClick={() => setActiveTab('baseline')}
            className={`flex-1 py-2 rounded-lg text-xs font-bold flex items-center justify-center gap-2 transition ${
              activeTab === 'baseline'
                ? 'bg-white text-slate-900 shadow-xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Sliders className="w-4 h-4" />
            <span>خط الأساس الإرشادي الشفاف (Rule Baseline)</span>
          </button>
        </div>

        {activeTab === 'ml' && ml?.status === 'AVAILABLE' ? (
          /* ML Tab Content */
          <div className="mt-5 space-y-5 animate-in fade-in duration-150">
            {/* ML Summary Card */}
            <div className={`p-5 rounded-2xl border ${mlTierColor.bg} ${mlTierColor.border} flex flex-col sm:flex-row items-center justify-between gap-4`}>
              <div>
                <span className="text-xs font-semibold text-slate-700">تنبؤ نموذج الغابات العشوائية (Random Forest):</span>
                <div className="flex items-baseline gap-2 mt-1">
                  <span className="text-2xl font-black text-slate-900">
                    {ml.predicted_tier === 'CRITICAL' ? 'أولوية قصوى حرجة' :
                     ml.predicted_tier === 'HIGH' ? 'أولوية مرتفعة' :
                     ml.predicted_tier === 'MEDIUM' ? 'أولوية متوسطة' : 'أولوية دورية'}
                  </span>
                  <span className="text-xs font-bold text-emerald-700 bg-emerald-100/70 px-2 py-0.5 rounded-full">
                    ثقة النموذج: {ml.confidence_pct}%
                  </span>
                </div>
              </div>
              <div className="text-center sm:text-left bg-white/80 backdrop-blur-xs p-3 rounded-xl border border-slate-200/50">
                <span className="text-[11px] font-bold text-slate-600 block">تقدير المساعدة الطارئة:</span>
                <span className="text-lg font-black text-slate-900">
                  {ml.demand_forecast?.estimated_aid_amount_yer.toLocaleString()} YER
                </span>
              </div>
            </div>

            {/* K-Means Cluster Archetype */}
            {ml.cluster && (
              <div className="bg-purple-50/60 p-4 rounded-2xl border border-purple-200">
                <div className="flex items-center gap-2 mb-2 text-purple-900">
                  <Layers className="w-5 h-5 text-purple-700" />
                  <span className="text-sm font-bold">عنقود الهشاشة المكتشف آلياً (K-Means Clustering):</span>
                </div>
                <div className="bg-white p-3.5 rounded-xl border border-purple-100 shadow-xs">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-black text-purple-950">{ml.cluster.title_ar}</span>
                    <span className="text-[11px] font-bold px-2 py-0.5 bg-purple-100 text-purple-800 rounded-md">
                      عنقود #{ml.cluster.id}
                    </span>
                  </div>
                  <p className="text-xs text-slate-600 mt-1 leading-relaxed">{ml.cluster.description}</p>
                  <div className="mt-3 pt-2.5 border-t border-purple-50 flex items-center gap-1.5 text-xs">
                    <span className="font-bold text-slate-800">التدخل المؤسسي الموصى به:</span>
                    <span className="text-purple-800 font-medium">{ml.cluster.recommended_intervention}</span>
                  </div>
                </div>
              </div>
            )}

            {/* Top Influencing Features (Feature Importances) */}
            {ml.top_contributing_factors && ml.top_contributing_factors.length > 0 && (
              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200">
                <div className="flex items-center gap-2 mb-3 text-slate-800">
                  <TrendingUp className="w-4 h-4 text-emerald-600" />
                  <h4 className="text-xs font-bold">المتغيرات الأكثر تأثيراً في تنبؤ الذكاء الاصطناعي (Feature Importance):</h4>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  {ml.top_contributing_factors.map((f, i) => (
                    <div key={i} className="bg-white p-3 rounded-xl border border-slate-200/80 shadow-2xs">
                      <div className="flex justify-between items-center text-xs mb-1.5">
                        <span className="font-bold text-slate-800">{f.label_ar}</span>
                        <span className="font-extrabold text-emerald-700">{f.importance_pct}% أثر</span>
                      </div>
                      <div className="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                        <div
                          className="bg-emerald-500 h-1.5 rounded-full"
                          style={{ width: `${Math.min(100, f.importance_pct * 3)}%` }}
                        ></div>
                      </div>
                      <span className="text-[11px] text-slate-500 mt-1 block">القيمة المسجلة بالملف: {f.value}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ) : (
          /* Baseline Rule Tab Content */
          <div className="mt-5 space-y-5 animate-in fade-in duration-150">
            {/* النتيجة الإجمالية وفئة الأولوية */}
            <div className={`p-5 rounded-2xl border ${currentTier.bg} ${currentTier.border} flex flex-col sm:flex-row items-center justify-between gap-4`}>
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
            <div className="space-y-3">
              <h4 className="text-xs font-bold text-slate-800">العوامل المساهمة في تكوين المؤشر (الأوزان الإرشادية):</h4>

              {Object.entries(data.factors_breakdown).map(([key, factor]) => {
                const pct = Math.round((factor.awarded_points / factor.weight_max) * 100);
                return (
                  <div key={key} className="bg-slate-50 p-3.5 rounded-xl border border-slate-200/70">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        {factorIcons[key] || <ShieldCheck className="w-5 h-5 text-slate-500" />}
                        <span className="text-sm font-bold text-slate-900">{factor.name_ar}</span>
                      </div>
                      <div className="text-xs font-bold text-slate-700">
                        <span className="text-emerald-700">{factor.awarded_points}</span> / {factor.weight_max} نقطة ({pct}%)
                      </div>
                    </div>

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
          </div>
        )}

        {/* شارة الحوكمة والإشعار الأخلاقي والشرعي */}
        <div className="mt-6 p-4 rounded-xl bg-amber-50/80 border border-amber-200 text-xs text-amber-900 flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <div className="font-bold">المبدأ الشرعي والقانوني الحاكم (Human-In-The-Loop):</div>
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
