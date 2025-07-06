// src/lib/types/index.ts 

// User types
export interface User {
    id: string;
    email: string;
    role: 'ADMIN' | 'MAINTAINER' | 'REPORTER';
    is_active: boolean;
    created_at: string;
  }
  
  export interface UserCreate {
    email: string;
    password: string;
    role?: 'ADMIN' | 'MAINTAINER' | 'REPORTER';
  }
  
  export interface LoginCredentials {
    email: string;
    password: string;
  }
  
  // Issue types - Added missing properties
  export interface Issue {
    id: string;
    title: string;
    description?: string;
    status: 'OPEN' | 'IN_PROGRESS' | 'RESOLVED' | 'CLOSED';
    severity?: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    created_by: string;
    created_at: string;
    updated_at: string;
    creator?: User;
  }
  
  export interface IssueCreate {
    title: string;
    description?: string;
    severity?: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  }
  
  export interface IssueUpdate {
    title?: string;
    description?: string;
    status?: 'OPEN' | 'IN_PROGRESS' | 'RESOLVED' | 'CLOSED';
    severity?: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  }
  
  // Auth store types
  export interface AuthState {
    isAuthenticated: boolean;
    user: User | null;
    token: string | null;
    loading: boolean;
  }
  
  // Toast types - Exported properly
  export interface Toast {
    id: string;
    type: 'success' | 'error' | 'warning' | 'info';
    message: string;
    duration?: number;
  }
  
  // Dashboard stats type
  export interface DashboardStats {
    totalIssues: number;
    openIssues: number;
    inProgressIssues: number;
    resolvedIssues: number;
    closedIssues: number;
    recentIssues: Issue[];
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
    severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    tags: string;
    file?: File | null;
  }