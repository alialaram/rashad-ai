import React, { useState, useEffect } from 'react';
import { X, UserPlus, Users, Plus, Trash2, Sparkles, AlertCircle } from 'lucide-react';
import { api } from '../services/api';
import type { HousingType, IdType } from '../types';

interface AddHouseholdModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreated: (newHouseholdId: string) => void;
}

interface MemberInput {
  full_name: string;
  relationship: string;
  gender: string;
  approximate_age: number;
  health_status: string;
  employment_status: string;
}

export const AddHouseholdModal: React.FC<AddHouseholdModalProps> = ({ isOpen, onClose, onCreated }) => {
  const [villages, setVillages] = useState<Array<{ id: string; name: string; full_label: string }>>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form State
  const [headFullName, setHeadFullName] = useState('');
  const [idType, setIdType] = useState<IdType>('NATIONAL_ID');
  const [idNumber, setIdNumber] = useState('');
  const [attestationSource, setAttestationSource] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [villageId, setVillageId] = useState('');
  const [housingType, setHousingType] = useState<HousingType>('RENTED');
  const [monthlyIncome, setMonthlyIncome] = useState<number>(30000);
  const [addressDetails, setAddressDetails] = useState('');

  // Members State
  const [members, setMembers] = useState<MemberInput[]>([
    {
      full_name: '',
      relationship: 'HEAD',
      gender: 'MALE',
      approximate_age: 42,
      health_status: 'HEALTHY',
      employment_status: 'UNEMPLOYED',
    },
    {
      full_name: '',
      relationship: 'WIFE',
      gender: 'FEMALE',
      approximate_age: 38,
      health_status: 'HEALTHY',
      employment_status: 'UNEMPLOYED',
    },
    {
      full_name: '',
      relationship: 'SON',
      gender: 'MALE',
      approximate_age: 12,
      health_status: 'HEALTHY',
      employment_status: 'STUDENT',
    },
  ]);

  useEffect(() => {
    if (isOpen) {
      api.getVillages()
        .then((data) => {
          setVillages(data);
          if (data.length > 0 && !villageId) {
            setVillageId(data[0].id);
          }
        })
        .catch(() => {
          // ignore or fallback
        });
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleAddMember = () => {
    setMembers([
      ...members,
      {
        full_name: '',
        relationship: 'SON',
        gender: 'MALE',
        approximate_age: 8,
        health_status: 'HEALTHY',
        employment_status: 'STUDENT',
      },
    ]);
  };

  const handleRemoveMember = (index: number) => {
    if (members.length <= 1) return;
    setMembers(members.filter((_, i) => i !== index));
  };

  const handleMemberChange = (index: number, field: keyof MemberInput, value: any) => {
    const updated = [...members];
    updated[index] = { ...updated[index], [field]: value };
    setMembers(updated);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!headFullName.trim()) {
      setError('يرجى إدخال اسم رب الأسرة الكامل');
      return;
    }

    if (idType === 'NATIONAL_ID' && !idNumber.trim()) {
      setError('يرجى إدخال الرقم الوطني للبطاقة الشخصية');
      return;
    }

    if (idType === 'TEMPORARY_ID' && (!attestationSource || attestationSource.length < 10)) {
      setError('يرجى تحديد مصدر إفادة عاقل الحارة أو اللجنة المجتمعية بوضوح للمعرف المؤقت');
      return;
    }

    if (!villageId) {
      setError('يرجى اختيار القرية أو الحي السكني');
      return;
    }

    setIsSubmitting(true);
    try {
      // Auto-set the head member name if empty
      const preparedMembers = members.map((m, idx) => ({
        ...m,
        full_name: m.full_name.trim() || (idx === 0 ? headFullName : `فرد من أسرة ${headFullName.split(' ')[0]}`),
      }));

      const payload = {
        head_full_name: headFullName,
        id_type: idType,
        id_number: idType === 'NATIONAL_ID' ? idNumber : null,
        attestation_source: idType === 'TEMPORARY_ID' ? attestationSource : null,
        phone_number: phoneNumber || null,
        village_id: villageId,
        address_details: addressDetails || null,
        housing_type: housingType,
        monthly_income: Number(monthlyIncome),
        members: preparedMembers,
      };

      const res = await api.createHousehold(payload);
      onCreated(res.id);
      onClose();
    } catch (err: any) {
      setError(err.message || 'حدث خطأ أثناء حفظ الأسرة');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs">
      <div className="bg-white rounded-3xl max-w-3xl w-full max-h-[92vh] overflow-y-auto shadow-2xl border border-slate-100 p-6 animate-in fade-in zoom-in-95 duration-150 text-right">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div className="flex items-center gap-2.5">
            <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center">
              <UserPlus className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-900">تسجيل أسرة جديدة وتحليل استحقاق الذكاء الاصطناعي</h3>
              <p className="text-xs text-slate-500 font-medium">
                إدخال بيانات الأسرة والموقع وأفراد الأسرة للتنبؤ الفوري بالحالة والعنقود ومطابقة التكرار
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

        {error && (
          <div className="mt-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="mt-5 space-y-6">
          {/* 1. بيانات رب الأسرة والهوية */}
          <div className="bg-slate-50/80 p-4 rounded-2xl border border-slate-200/80 space-y-4">
            <h4 className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
              <span>1. البيانات الأساسية والهوية:</span>
            </h4>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">اسم رب الأسرة الرباعي *</label>
                <input
                  type="text"
                  required
                  placeholder="مثال: يحيى صالح مسعد الهمداني"
                  value={headFullName}
                  onChange={(e) => setHeadFullName(e.target.value)}
                  className="w-full px-3 py-2 bg-white border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">نوع وثيقة الهوية *</label>
                <select
                  value={idType}
                  onChange={(e) => setIdType(e.target.value as IdType)}
                  className="w-full px-3 py-2 bg-white border border-slate-200 rounded-xl text-xs font-medium text-slate-800 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500"
                >
                  <option value="NATIONAL_ID">بطاقة شخصية رسمية (رقم وطني)</option>
                  <option value="TEMPORARY_ID">معرف مؤقت (فاقدو الوثائق - إفادة عاقل الحارة)</option>
                </select>
              </div>

              {idType === 'NATIONAL_ID' ? (
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">الرقم الوطني (11 رقم) *</label>
                  <input
                    type="text"
                    required
                    maxLength={11}
                    placeholder="مثال: 01020304050"
                    value={idNumber}
                    onChange={(e) => setIdNumber(e.target.value)}
                    className="w-full px-3 py-2 bg-white border border-slate-200 rounded-xl text-xs font-mono focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500"
                  />
                </div>
              ) : (
                <div>
                  <label className="block text-xs font-bold text-amber-900 mb-1">مصدر إفادة عاقل الحارة / اللجنة *</label>
                  <input
                    type="text"
                    required
                    placeholder="إفادة عاقل حارة القاع: الشيخ يحيى محمد - 771234501"
                    value={attestationSource}
                    onChange={(e) => setAttestationSource(e.target.value)}
                    className="w-full px-3 py-2 bg-amber-50/50 border border-amber-200 rounded-xl text-xs text-amber-950 focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500"
                  />
                </div>
              )}

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">رقم الهاتف للتواصل</label>
                <input
                  type="text"
                  placeholder="مثال: 771234567"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  className="w-full px-3 py-2 bg-white border border-slate-200 rounded-xl text-xs font-mono focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500"
                />
              </div>
            </div>
          </div>

          {/* 2. المسكن والدخل والموقع */}
          <div className="bg-slate-50/80 p-4 rounded-2xl border border-slate-200/80 space-y-4">
            <h4 className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
              <span>2. الموقع والظروف المعيشية:</span>
            </h4>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">القرية / الحي السكني *</label>
                <select
                  value={villageId}
                  onChange={(e) => setVillageId(e.target.value)}
                  className="w-full px-3 py-2 bg-white border border-slate-200 rounded-xl text-xs font-medium text-slate-800 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500"
                >
                  {villages.map((v) => (
                    <option key={v.id} value={v.id}>
                      {v.full_label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">طبيعة المسكن والمأوى *</label>
                <select
                  value={housingType}
                  onChange={(e) => setHousingType(e.target.value as HousingType)}
                  className="w-full px-3 py-2 bg-white border border-slate-200 rounded-xl text-xs font-medium text-slate-800 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500"
                >
                  <option value="RENTED">إيجار شهري</option>
                  <option value="OWNED">ملك للأسرة</option>
                  <option value="DISPLACED_CAMP">مخيم نزوح / لجوء</option>
                  <option value="SHARED">سكن مشترك مع أسرة أخرى</option>
                  <option value="MAKSHA">مقشة / عشة / سكن عشوائي هش</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">الدخل الشهري الإجمالي (YER)</label>
                <input
                  type="number"
                  min={0}
                  step={5000}
                  value={monthlyIncome}
                  onChange={(e) => setMonthlyIncome(Number(e.target.value))}
                  className="w-full px-3 py-2 bg-white border border-slate-200 rounded-xl text-xs font-bold text-slate-900 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">تفاصيل العنوان</label>
              <input
                type="text"
                placeholder="مثال: جوار مدرسة الفتح - حارة السلام"
                value={addressDetails}
                onChange={(e) => setAddressDetails(e.target.value)}
                className="w-full px-3 py-2 bg-white border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500"
              />
            </div>
          </div>

          {/* 3. أفراد الأسرة والحالات الصحية */}
          <div className="bg-slate-50/80 p-4 rounded-2xl border border-slate-200/80 space-y-4">
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                <Users className="w-4 h-4 text-emerald-600" />
                <span>3. أفراد الأسرة والحالات الصحية والعملية ({members.length} أفراد):</span>
              </h4>
              <button
                type="button"
                onClick={handleAddMember}
                className="px-3 py-1 bg-white hover:bg-slate-100 border border-slate-200 text-emerald-700 rounded-lg text-xs font-bold flex items-center gap-1 transition"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>إضافة فرد</span>
              </button>
            </div>

            <div className="space-y-3">
              {members.map((member, index) => (
                <div key={index} className="bg-white p-3 rounded-xl border border-slate-200/80 grid grid-cols-1 sm:grid-cols-6 gap-2.5 items-center text-xs">
                  <div className="sm:col-span-2">
                    <input
                      type="text"
                      placeholder={index === 0 ? 'اسم رب الأسرة' : `اسم الفرد ${index + 1}`}
                      value={member.full_name}
                      onChange={(e) => handleMemberChange(index, 'full_name', e.target.value)}
                      className="w-full px-2.5 py-1.5 border border-slate-200 rounded-lg text-xs"
                    />
                  </div>

                  <div>
                    <select
                      value={member.relationship}
                      onChange={(e) => handleMemberChange(index, 'relationship', e.target.value)}
                      className="w-full px-2 py-1.5 border border-slate-200 rounded-lg text-xs"
                    >
                      <option value="HEAD">رب الأسرة</option>
                      <option value="WIFE">زوجة</option>
                      <option value="SON">ابن</option>
                      <option value="DAUGHTER">ابنة</option>
                      <option value="PARENT">والد/والدة</option>
                      <option value="OTHER">قريب آخر</option>
                    </select>
                  </div>

                  <div>
                    <input
                      type="number"
                      min={0}
                      max={110}
                      placeholder="العمر"
                      value={member.approximate_age}
                      onChange={(e) => handleMemberChange(index, 'approximate_age', Number(e.target.value))}
                      className="w-full px-2 py-1.5 border border-slate-200 rounded-lg text-xs"
                    />
                  </div>

                  <div>
                    <select
                      value={member.health_status}
                      onChange={(e) => handleMemberChange(index, 'health_status', e.target.value)}
                      className={`w-full px-2 py-1.5 border rounded-lg text-xs font-medium ${
                        member.health_status === 'DISABILITY'
                          ? 'border-purple-300 bg-purple-50 text-purple-900 font-bold'
                          : member.health_status === 'CHRONIC_DISEASE'
                          ? 'border-rose-300 bg-rose-50 text-rose-900 font-bold'
                          : 'border-slate-200'
                      }`}
                    >
                      <option value="HEALTHY">سليم معافى</option>
                      <option value="CHRONIC_DISEASE">مرض مزمن</option>
                      <option value="DISABILITY">إعاقة مستديمة</option>
                    </select>
                  </div>

                  <div className="flex items-center gap-1">
                    <select
                      value={member.employment_status}
                      onChange={(e) => handleMemberChange(index, 'employment_status', e.target.value)}
                      className="w-full px-2 py-1.5 border border-slate-200 rounded-lg text-xs"
                    >
                      <option value="UNEMPLOYED">عاطل / بلا عمل</option>
                      <option value="EMPLOYED">يعمل بأجر</option>
                      <option value="STUDENT">طالب / طفل</option>
                      <option value="UNABLE_TO_WORK">عاجز عن العمل</option>
                    </select>

                    {members.length > 1 && (
                      <button
                        type="button"
                        onClick={() => handleRemoveMember(index)}
                        className="p-1.5 text-rose-500 hover:bg-rose-50 rounded-md transition"
                        title="حذف الفرد"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Footer Actions */}
          <div className="flex items-center justify-between pt-4 border-t border-slate-100">
            <span className="text-xs text-slate-500">
              * سيقوم الذكاء الاصطناعي بتحليل الاستحقاق وفحص الازدواجية فور الحفظ.
            </span>

            <div className="flex gap-2">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 border border-slate-200 text-slate-600 rounded-xl text-xs font-bold hover:bg-slate-50 transition"
              >
                إلغاء
              </button>
              <button
                type="submit"
                disabled={isSubmitting}
                className="px-5 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-xs font-bold flex items-center gap-2 shadow-xs transition disabled:opacity-50"
              >
                <Sparkles className="w-4 h-4 text-emerald-200" />
                <span>{isSubmitting ? 'جاري الحفظ والتحليل...' : 'حفظ الأسرة وتشغيل تنبؤ الذكاء الاصطناعي'}</span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};
