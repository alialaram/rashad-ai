import type {
  AuthResponse,
  HouseholdListItem,
  HouseholdDetails,
  NeedsAssessmentData,
  DuplicateSuspicion,
  DocumentData,
} from '../types';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export const api = {
  getToken(): string | null {
    return localStorage.getItem('rashad_token');
  },

  setToken(token: string) {
    localStorage.setItem('rashad_token', token);
  },

  removeToken() {
    localStorage.removeItem('rashad_token');
    localStorage.removeItem('rashad_user');
  },

  async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const token = this.getToken();
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      let errorMsg = 'حدث خطأ في الاتصال بالخادم';
      try {
        const errorData = await response.json();
        errorMsg = errorData.detail || errorMsg;
      } catch {
        // fallback
      }
      throw new Error(errorMsg);
    }

    return response.json();
  },

  // Auth Endpoints
  async login(username: string, password: string): Promise<AuthResponse> {
    const data = await this.request<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    this.setToken(data.access_token);
    localStorage.setItem('rashad_user', JSON.stringify(data));
    return data;
  },

  async getMe() {
    return this.request('/auth/me');
  },

  // Households Endpoints
  async getHouseholds(params: {
    skip?: number;
    limit?: number;
    search?: string;
    id_type?: string;
    housing_type?: string;
  } = {}): Promise<HouseholdListItem[]> {
    const query = new URLSearchParams();
    if (params.skip !== undefined) query.set('skip', params.skip.toString());
    if (params.limit !== undefined) query.set('limit', params.limit.toString());
    if (params.search) query.set('search', params.search);
    if (params.id_type) query.set('id_type', params.id_type);
    if (params.housing_type) query.set('housing_type', params.housing_type);

    return this.request<HouseholdListItem[]>(`/households?${query.toString()}`);
  },

  async getHousehold(id: string): Promise<HouseholdDetails> {
    return this.request<HouseholdDetails>(`/households/${id}`);
  },

  async getVillages(): Promise<Array<{ id: string; name: string; full_label: string }>> {
    return this.request<Array<{ id: string; name: string; full_label: string }>>('/households/geography/villages');
  },

  async createHousehold(data: any): Promise<HouseholdDetails> {
    return this.request<HouseholdDetails>('/households', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // Needs Assessment
  async getNeedsAssessment(householdId: string): Promise<NeedsAssessmentData> {
    return this.request<NeedsAssessmentData>(`/needs/${householdId}`);
  },

  // Duplicate Suspicions
  async getDuplicates(): Promise<DuplicateSuspicion[]> {
    return this.request<DuplicateSuspicion[]>('/duplicates');
  },

  async resolveDuplicate(
    suspicionId: string,
    data: {
      resolution_status: 'CONFIRMED_MERGED' | 'FALSE_POSITIVE';
      resolution_reason: string;
      primary_household_id?: string;
    }
  ): Promise<DuplicateSuspicion> {
    return this.request<DuplicateSuspicion>(`/duplicates/${suspicionId}/resolve`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // Document Intelligence & OCR
  async generateDemoDocument(householdId: string): Promise<DocumentData> {
    return this.request<DocumentData>(`/documents/generate-demo/${householdId}`, {
      method: 'POST',
    });
  },

  async getDocument(documentId: string): Promise<DocumentData> {
    return this.request<DocumentData>(`/documents/${documentId}`);
  },

  getDocumentFileUrl(documentId: string): string {
    return `${API_BASE_URL}/documents/${documentId}/file`;
  },

  async verifyDocument(
    documentId: string,
    verifiedFields: Record<string, string>,
    reviewerNotes: string = 'تمت المطابقة والاعتماد البشري'
  ): Promise<DocumentData> {
    return this.request<DocumentData>(`/documents/${documentId}/verify`, {
      method: 'POST',
      body: JSON.stringify({
        verified_fields: verifiedFields,
        reviewer_notes: reviewerNotes,
      }),
    });
  },
};
