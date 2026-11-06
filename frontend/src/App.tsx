import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { DashboardStats } from './components/DashboardStats';
import { HouseholdList } from './components/HouseholdList';
import { NeedsModal } from './components/NeedsModal';
import { DuplicatesView } from './components/DuplicatesView';
import { api } from './services/api';
import type {
  AuthResponse,
  HouseholdListItem,
  DuplicateSuspicion,
  NeedsAssessmentData,
} from './types';
import { Users, Copy, RefreshCw, ShieldAlert } from 'lucide-react';

export const App: React.FC = () => {
  const [currentUser, setCurrentUser] = useState<AuthResponse | null>(null);
  const [activeTab, setActiveTab] = useState<'households' | 'duplicates'>('households');
  const [households, setHouseholds] = useState<HouseholdListItem[]>([]);
  const [duplicates, setDuplicates] = useState<DuplicateSuspicion[]>([]);
  const [selectedNeedsData, setSelectedNeedsData] = useState<NeedsAssessmentData | null>(null);
  const [selectedIdType, setSelectedIdType] = useState<string>('');
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Pre-configured demo accounts for quick evaluation
  const defaultCredentials: Record<string, string> = {
    admin: 'Admin@2026',
    researcher_sanaa: 'Sanaa@2026',
    beneficiary_officer: 'Register@2026',
    programs_officer: 'Officer@2026',
    auditor: 'Auditor@2026',
    analyst: 'Analyst@2026',
  };

  // Initial load: authenticate as registration officer by default
  useEffect(() => {
    handleQuickRoleSwitch('beneficiary_officer');
  }, []);

  const handleQuickRoleSwitch = async (username: string) => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      const password = defaultCredentials[username] || 'Admin@2026';
      const authData = await api.login(username, password);
      setCurrentUser(authData);
      await loadDashboardData();
    } catch (err: any) {
      setErrorMessage(err.message || 'تعذر الاتصال بالخادم. يرجى التأكد من تشغيل FastAPI على المنفذ 8000');
    } finally {
      setIsLoading(false);
    }
  };

  const loadDashboardData = async () => {
    setIsLoading(true);
    try {
      const [householdsData, duplicatesData] = await Promise.all([
        api.getHouseholds({ search: searchTerm, id_type: selectedIdType || undefined }),
        api.getDuplicates().catch(() => []),
      ]);
      setHouseholds(householdsData);
      setDuplicates(duplicatesData);
    } catch (err: any) {
      setErrorMessage(err.message || 'حدث خطأ في تحميل البيانات');
    } finally {
      setIsLoading(false);
    }
  };

  // Reload when filters change
  useEffect(() => {
    if (currentUser) {
      loadDashboardData();
    }
  }, [selectedIdType, searchTerm]);

  const handleInspectNeeds = async (householdId: string) => {
    try {
      const data = await api.getNeedsAssessment(householdId);
      setSelectedNeedsData(data);
    } catch (err: any) {
      alert(err.message || 'تعذر استرجاع بطاقة تقييم الاحتياج');
    }
  };

  const handleResolveDuplicate = async (
    suspicionId: string,
    status: 'CONFIRMED_MERGED' | 'FALSE_POSITIVE',
    reason: string,
    primaryId?: string
  ) => {
    await api.resolveDuplicate(suspicionId, {
      resolution_status: status,
      resolution_reason: reason,
      primary_household_id: primaryId,
    });
    // Refresh duplicates
    const updated = await api.getDuplicates();
    setDuplicates(updated);
  };

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col font-sans">
      <Header
        currentUser={currentUser}
        onLogout={() => {
          api.removeToken();
          setCurrentUser(null);
        }}
        onQuickRoleSwitch={handleQuickRoleSwitch}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error notification if Backend is offline */}
        {errorMessage && (
          <div className="mb-6 p-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center justify-between">
            <div className="flex items-center gap-2">
              <ShieldAlert className="w-5 h-5 text-rose-600 shrink-0" />
              <span>{errorMessage}</span>
            </div>
            <button
              onClick={() => handleQuickRoleSwitch('admin')}
              className="px-3 py-1 bg-rose-600 text-white rounded-lg font-bold hover:bg-rose-700 transition"
            >
              إعادة المحاولة
            </button>
          </div>
        )}

        {/* Dashboard Statistics */}
        <DashboardStats
          households={households}
          duplicates={duplicates}
          onTabChange={(tab) => setActiveTab(tab)}
        />

        {/* Main Tabs Navigation */}
        <div className="flex items-center justify-between border-b border-slate-200 mb-6">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveTab('households')}
              className={`pb-3 px-4 text-xs font-bold transition flex items-center gap-2 relative ${
                activeTab === 'households'
                  ? 'text-emerald-700 border-b-2 border-emerald-600'
                  : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              <Users className="w-4 h-4" />
              سجل الأسر والمستفيدين ({households.length})
            </button>
            <button
              onClick={() => setActiveTab('duplicates')}
              className={`pb-3 px-4 text-xs font-bold transition flex items-center gap-2 relative ${
                activeTab === 'duplicates'
                  ? 'text-rose-700 border-b-2 border-rose-600'
                  : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              <Copy className="w-4 h-4" />
              مراجعة التكرارات والازدواجية ({duplicates.filter((d) => d.resolution_status === 'PENDING').length})
            </button>
          </div>

          <button
            onClick={loadDashboardData}
            title="تحديث البيانات"
            className="p-2 text-slate-400 hover:text-slate-600 hover:bg-white rounded-xl transition border border-transparent hover:border-slate-200"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin text-emerald-600' : ''}`} />
          </button>
        </div>

        {/* Tab Content */}
        {activeTab === 'households' ? (
          <HouseholdList
            households={households}
            isLoading={isLoading}
            onSearch={(term) => setSearchTerm(term)}
            onFilterIdType={(type) => setSelectedIdType(type)}
            onInspectNeeds={handleInspectNeeds}
            selectedIdType={selectedIdType}
          />
        ) : (
          <DuplicatesView
            duplicates={duplicates}
            onResolve={handleResolveDuplicate}
          />
        )}
      </main>

      {/* Needs Assessment Explainability Modal */}
      <NeedsModal
        data={selectedNeedsData}
        onClose={() => setSelectedNeedsData(null)}
      />

      {/* Institutional Footer */}
      <footer className="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-700">
        <p className="font-semibold">
          رشاد AI -- منظومة الذكاء الاصطناعي لإدارة وتحليل الاحتياج الزكوي وتوجيه الموارد
        </p>
        <p className="mt-1 text-[11px] text-slate-700">
          مشروع تطوير مؤسسي تجريبي مستند إلى هندسة برمجيات رصينة ومبادئ الذكاء الاصطناعي المسؤول.
        </p>
      </footer>
    </div>
  );
};

export default App;
