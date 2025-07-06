export interface SeverityData {
    severity: string;
    count: number;
  }
  
  export interface StatusData {
    status: string;
    count: number;
  }
  
  export interface DashboardData {
    severity_breakdown: SeverityData[];
    status_breakdown: StatusData[];
    total_open: number;
  }
  