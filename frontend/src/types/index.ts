export type UserRole =
  | 'SYSTEM_ADMIN'
  | 'FIELD_RESEARCHER'
  | 'BENEFICIARY_OFFICER'
  | 'PROGRAMS_OFFICER'
  | 'DATA_ANALYST'
  | 'AUDITOR'
  | 'MANAGER';

export type IdType = 'NATIONAL_ID' | 'FAMILY_CARD' | 'TEMPORARY_ID' | 'OTHER';

export type IdVerificationStatus =
  | 'VERIFIED_OFFICIAL'
  | 'LOCAL_ATTESTATION'
  | 'PENDING_REVIEW';

export type HousingType =
  | 'OWNED'
  | 'RENTED'
  | 'DISPLACED_CAMP'
  | 'SHARED'
  | 'MAKSHA';

export type HouseholdStatus = 'ACTIVE' | 'ARCHIVED' | 'MERGED_DUPLICATE';

export interface User {
  id: string;
  username: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  scopes: Array<{ district_id: string; can_write: boolean }>;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  role: UserRole;
  username: string;
  full_name: string;
  scopes: string[];
}

export interface HouseholdListItem {
  id: string;
  file_number: string;
  pseudo_id: string;
  head_full_name: string;
  id_type: IdType;
  id_number: string;
  id_verification_status: IdVerificationStatus;
  phone_number?: string | null;
  housing_type: HousingType;
  monthly_income: number;
  status: HouseholdStatus;
  members_count: number;
  created_at: string;
}

export interface HouseholdMember {
  id: string;
  full_name: string;
  relationship: string;
  gender: string;
  approximate_age?: number;
  health_status: string;
  disability_type?: string;
  education_level?: string;
  employment_status: string;
}

export interface HouseholdDetails extends HouseholdListItem {
  attestation_source?: string | null;
  address_details?: string | null;
  village_id: string;
  members: HouseholdMember[];
}

export interface FactorBreakdownItem {
  name_ar: string;
  weight_max: number;
  awarded_points: number;
  reason_ar: string;
  [key: string]: any;
}

export interface MLClusterInfo {
  id: number;
  title_ar: string;
  title_en: string;
  description: string;
  recommended_intervention: string;
}

export interface MLDemandForecast {
  estimated_aid_amount_yer: number;
  currency: string;
}

export interface MLContributingFactor {
  feature: string;
  label_ar: string;
  value: number;
  importance_pct: number;
}

export interface MLInsights {
  status: 'AVAILABLE' | 'UNAVAILABLE';
  model_version?: string;
  predicted_tier?: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  confidence_pct?: number;
  tier_probabilities?: Record<string, number>;
  cluster?: MLClusterInfo;
  demand_forecast?: MLDemandForecast;
  top_contributing_factors?: MLContributingFactor[];
  extracted_features?: Record<string, number>;
  disclaimer_ar?: string;
}

export interface NeedsAssessmentData {
  id?: string;
  household_id: string;
  calculated_score: number;
  priority_tier: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  tier_label_ar: string;
  model_version: string;
  factors_breakdown: Record<string, FactorBreakdownItem>;
  disclaimer_text_ar: string;
  disclaimer_acknowledged: boolean;
  evaluator_override_tier?: string | null;
  evaluator_notes?: string | null;
  ml_insights?: MLInsights;
}

export interface DuplicateSuspicion {
  id: string;
  source_household_id: string;
  matched_household_id: string;
  match_type: 'EXACT_NATIONAL_ID' | 'EXACT_PHONE' | 'FUZZY_NAME_GEO';
  similarity_score: number;
  match_details: {
    matched_field?: string;
    matched_value?: string;
    source_name?: string;
    candidate_name?: string;
    reason_ar?: string;
    source?: string;
    candidate?: string;
    name_sim?: number;
    [key: string]: any;
  };
  resolution_status: 'PENDING' | 'CONFIRMED_MERGED' | 'FALSE_POSITIVE';
  resolution_reason?: string | null;
  created_at: string;
}

export interface OCRField {
  value: string | null;
  confidence: number;
  label_ar: string;
  requires_review: boolean;
  human_corrected?: boolean;
}

export interface OCRExtractionData {
  id: string;
  document_id: string;
  extracted_data: Record<string, OCRField>;
  raw_text?: string | null;
  overall_confidence: number;
  human_verified: boolean;
  verified_at?: string | null;
}

export interface DocumentData {
  id: string;
  household_id: string;
  doc_type: string;
  storage_path: string;
  mime_type: string;
  file_size_bytes: number;
  ocr_status: string;
  created_at: string;
  ocr_extraction?: OCRExtractionData | null;
}
