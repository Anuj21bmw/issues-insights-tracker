// src/lib/types/index.ts 

// User types
export interface User {
  id: string;
  name: string;
  email: string;
  role: 'ADMIN' | 'MAINTAINER' | 'REPORTER';
  is_active: boolean;
  created_at: string;
}

export interface UserCreate {
  name: string;
  email: string;
  password: string;
  role?: 'ADMIN' | 'MAINTAINER' | 'REPORTER';
}

export interface LoginCredentials {
  email: string;
  password: string;
}

// Issue types - Fixed and consistent
export type IssueStatus = 'OPEN' | 'TRIAGED' | 'IN_PROGRESS' | 'DONE';
export type IssueSeverity = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface Issue {
  id: string;
  title: string;
  description?: string;
  status: IssueStatus;
  severity: IssueSeverity;
  file_path?: string;
  tags?: string;
  created_by: string;
  assigned_to?: string;
  created_at: string;
  updated_at: string;
  creator?: User;
}

export interface IssueCreate {
  title: string;
  description?: string;
  severity?: IssueSeverity;
  tags?: string;
}

export interface IssueUpdate {
  title?: string;
  description?: string;
  status?: IssueStatus;
  severity?: IssueSeverity;
  tags?: string;
  assigned_to?: string;
}

// Auth store types
export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  loading: boolean;
}

// Toast types - Fixed with title property
export interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  duration?: number;
}

// Dashboard stats type
export interface DashboardStats {
  total_issues: number;
  open_issues: number;
  in_progress_issues: number;
  resolved_issues: number;
  closed_issues: number;
  recent_issues: Issue[];
  issuesByStatus: { [key: string]: number };
  issuesBySeverity: { [key: string]: number };
}

// API Response types
export interface ApiError {
  detail: string;
  status_code?: number;
}

// Form types
export interface CreateIssueForm {
  title: string;
  description: string;
  severity: IssueSeverity;
  tags: string;
  file?: File | null;
}