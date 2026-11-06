import React, { useState } from 'react';
import { X, FileText, AlertTriangle, ShieldCheck, Eye, Edit3 } from 'lucide-react';
import type { DocumentData } from '../types';

interface DocumentReviewModalProps {
  document: DocumentData | null;
  onClose: () => void;
  onVerify: (documentId: string, verifiedFields: Record<string, string>, notes: string) => Promise<void>;
}

export const DocumentReviewModal: React.FC<DocumentReviewModalProps> = ({
  document,
  onClose,
  onVerify,
}) => {
  if (!document || !document.ocr_extraction) return null;

  const extraction = document.ocr_extraction;
  const initialFields: Record<string, string> = {};
  Object.entries(extraction.extracted_data).forEach(([key, field]) => {
    initialFields[key] = field.value || '';
  });

  const [formFields, setFormFields] = useState<Record<string, string>>(initialFields);
  const [notes, setNotes] = useState('تمت المطابقة البصرية مع أصل الوثيقة والمصادقة على صحتها.');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleFieldChange = (key: string, val: string) => {
    setFormFields((prev) => ({ ...prev, [key]: val }));
  };

  const handleSaveVerification = async () => {
    setIsSubmitting(true);
    try {
      await onVerify(document.id, formFields, notes);
      alert('تم اعتماد التحقق البشري بنجاح وتحديث حالة الوثيقة إلى [معتمد بشرياً]');
      onClose();
    } catch (err: any) {
      alert(err.message || 'فشل اعتماد الوثيقة');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs">
      <div className="bg-white rounded-3xl max-w-5xl w-full max-h-[92vh] overflow-hidden shadow-2xl border border-slate-100 flex flex-col animate-in fade-in zoom-in-95 duration-150">
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-teal-50 text-teal-700 flex items-center justify-center">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-slate-900">شاشة التحقق البشري والمراجعة الثنائية (OCR Review)</h3>
                {extraction.human_verified ? (
                  <span className="px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[10px] font-bold">
                    معتمد بشرياً
                  </span>
                ) : (
                  <span className="px-2 py-0.5 rounded-full bg-amber-100 text-amber-800 text-[10px] font-bold">
                    بانتظار التحقق والمصادقة
                  </span>
                )}
              </div>
              <p className="text-xs text-slate-500 font-medium">
                متوسط ثقة الاستخراج الآلي: <strong className="text-slate-800">{extraction.overall_confidence}%</strong>
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-200/60 rounded-full transition"
            aria-label="إغلاق"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body: Side-by-Side Review */}
        <div className="flex-1 overflow-y-auto p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* الجانب الأيمن: معاينة صورة الوثيقة الأصلية */}
          <div className="bg-slate-100 rounded-2xl p-4 border border-slate-200 flex flex-col items-center justify-center min-h-[380px]">
            <span className="text-xs font-bold text-slate-500 mb-3 flex items-center gap-1.5 self-start">
              <Eye className="w-4 h-4" />
              معاينة صورة الوثيقة الأصلية المحمية:
            </span>
            <div className="w-full flex-1 flex items-center justify-center bg-white rounded-xl overflow-hidden shadow-xs border border-slate-200/80 p-2">
              <img
                src={`http://127.0.0.1:8000/api/v1/documents/${document.id}/file`}
                alt="Document Preview"
                className="max-h-[360px] w-auto object-contain rounded-lg shadow-xs"
              />
            </div>
            <span className="text-[10px] text-slate-400 mt-2">
              نوع المستند: {document.doc_type} | الحجم: {(document.file_size_bytes / 1024).toFixed(1)} KB
            </span>
          </div>

          {/* الجانب الأيسر: الحقول المستخرجة مع نسب الثقة والتعديل اليدوي */}
          <div className="flex flex-col justify-between space-y-4">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
                  <Edit3 className="w-4 h-4 text-emerald-600" />
                  الحقول المستخرجة آلياً (قابلة للتصحيح اليدوي):
                </span>
                <span className="text-[11px] text-slate-400">الحقول &lt; 80% تتطلب تدقيقاً خاصاً</span>
              </div>

              <div className="space-y-3.5">
                {Object.entries(extraction.extracted_data).map(([key, field]) => {
                  const isHighConf = field.confidence >= 80;
                  return (
                    <div key={key} className="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
                      <div className="flex items-center justify-between mb-1.5">
                        <label className="text-xs font-bold text-slate-800">{field.label_ar}:</label>
                        <span
                          className={`text-[10px] px-2 py-0.5 rounded-md font-bold ${
                            isHighConf
                              ? 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                              : 'bg-amber-100 text-amber-800 border border-amber-200'
                          }`}
                        >
                          ثقة: {field.confidence}% {isHighConf ? '✓' : '⚠️ يتطلب تدقيق'}
                        </span>
                      </div>
                      <input
                        type="text"
                        value={formFields[key] || ''}
                        onChange={(e) => handleFieldChange(key, e.target.value)}
                        className={`w-full px-3 py-2 bg-white border rounded-lg text-xs font-medium text-slate-900 focus:outline-hidden focus:ring-2 focus:ring-emerald-500/20 ${
                          !isHighConf ? 'border-amber-400' : 'border-slate-300'
                        }`}
                      />
                    </div>
                  );
                })}

                <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
                  <label className="text-xs font-bold text-slate-700 block mb-1">
                    ملاحظات وتوثيق المراجع البشري:
                  </label>
                  <textarea
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    rows={2}
                    className="w-full px-3 py-2 bg-white border border-slate-300 rounded-lg text-xs font-medium text-slate-900 focus:outline-hidden focus:ring-2 focus:ring-emerald-500/20"
                  />
                </div>
              </div>
            </div>

            {/* إشعار السياسة الرقابية */}
            <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-[11px] text-amber-900 flex items-start gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
              <span>
                <strong>ضمانة المسؤولية:</strong> باعتمادك هذه الوثيقة، يُثبت اسمك وتوقيعك الرقمي في سجل التدقيق غير القابل للتعديل كمسؤول عن مطابقة البيانات مع المستند الأصلي.
              </span>
            </div>
          </div>
        </div>

        {/* Modal Footer */}
        <div className="px-6 py-4 border-t border-slate-100 flex items-center justify-between bg-slate-50">
          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-bold text-slate-600 hover:bg-slate-200 rounded-xl transition"
          >
            إلغاء
          </button>

          <button
            onClick={handleSaveVerification}
            disabled={isSubmitting}
            className="inline-flex items-center gap-1.5 px-6 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-xs font-bold transition shadow-xs"
          >
            <ShieldCheck className="w-4 h-4" />
            {isSubmitting ? 'جاري الحفظ...' : 'اعتماد التحقق البشري والمصادقة على الوثيقة'}
          </button>
        </div>
      </div>
    </div>
  );
};
