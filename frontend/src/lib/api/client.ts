// frontend/src/lib/api/client.ts

import { authStore } from '$lib/stores/auth';
import { get } from 'svelte/store';
import type {
  Issue,
  IssueCreate,
  IssueUpdate,
  User,
  UserCreate,
  LoginCredentials,
} from '$lib/types';
import type { DashboardData } from '$lib/types/dashboard';

const API_BASE_URL = 'http://localhost:8000';

interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
    console.log('🔗 API Client initialized with base URL:', this.baseURL);
  }

  private getAuthHeaders(): Record<string, string> {
    const auth = get(authStore);
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (auth.token) {
      headers['Authorization'] = `Bearer ${auth.token}`;
      console.log('🔑 Auth header added:', auth.token.slice(0, 20) + '...');
    }

    return headers;
  }

  private async handleResponse<T>(response: Response): Promise<ApiResponse<T>> {
    try {
      if (response.status === 401) {
        authStore.logout();
        throw new Error('Authentication required');
      }

      const data = await response.json();

      if (response.ok) {
        return { data, status: response.status };
      } else {
        return {
          error: data.detail || data.message || 'An error occurred',
          status: response.status,
        };
      }
    } catch (error) {
      if (error instanceof Error) {
        return { error: error.message, status: response.status };
      }
      return { error: 'Network error', status: response.status };
    }
  }

  async testConnection(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseURL}/health`);
      return response.ok;
    } catch {
      return false;
    }
  }

  // Auth
  async register(userData: UserCreate): Promise<ApiResponse<{ access_token: string; token_type: string }>> {
    const url = `${this.baseURL}/api/auth/register`;

    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    });

    return this.handleResponse(response);
  }

  async login(credentials: LoginCredentials): Promise<ApiResponse<{ access_token: string; token_type: string }>> {
    const formData = new FormData();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);

    const url = `${this.baseURL}/api/auth/login`;

    const response = await fetch(url, {
      method: 'POST',
      body: formData,
    });

    return this.handleResponse(response);
  }

  async getCurrentUser(): Promise<ApiResponse<User>> {
    const url = `${this.baseURL}/api/auth/me`;
    const headers = this.getAuthHeaders();

    const response = await fetch(url, {
      headers,
    });

    return this.handleResponse(response);
  }

  // Issues
  async getIssues(): Promise<ApiResponse<Issue[]>> {
    const url = `${this.baseURL}/api/issues/`;
    const response = await fetch(url, {
      headers: this.getAuthHeaders(),
    });

    return this.handleResponse(response);
  }

  async createIssue(formData: FormData): Promise<ApiResponse<Issue>> {
    const title = formData.get('title') as string;
    const description = formData.get('description') as string;
    const severity = formData.get('severity') as string;

    const issueData: IssueCreate = {
      title,
      description: description || undefined,
      severity: severity as any,
    };

    const url = `${this.baseURL}/api/issues/`;
    const response = await fetch(url, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(issueData),
    });

    return this.handleResponse(response);
  }

  // ✅ Dashboard stats - Returns structure that matches DashboardData type
  async getDashboardStats(): Promise<ApiResponse<DashboardData>> {
    const issuesResponse = await this.getIssues();

    if (!issuesResponse.data) {
      return {
        error: issuesResponse.error || 'Failed to load dashboard data',
        status: issuesResponse.status,
      };
    }

    const issues = issuesResponse.data;

    const severities = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'];
    const statuses = ['OPEN', 'TRIAGED', 'IN_PROGRESS', 'DONE'];

    const severity_breakdown = severities.map(sev => ({
      severity: sev,
      count: issues.filter(i => i.severity === sev).length,
    }));

    const status_breakdown = statuses.map(stat => ({
      status: stat,
      count: issues.filter(i => i.status === stat).length,
    }));

    const total_open = issues.filter(i => i.status === 'OPEN').length;

    const dashboardData: DashboardData = {
      severity_breakdown,
      status_breakdown,
      total_open,
    };

    return { data: dashboardData, status: 200 };
  }

  async healthCheck(): Promise<ApiResponse<{ message: string }>> {
    const response = await fetch(`${this.baseURL}/health`);
    return this.handleResponse(response);
  }
}

export const apiClient = new ApiClient();
apiClient.testConnection();
