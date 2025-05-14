export interface ApiResponse {
    status: "success" | "error";
    status_code?: number;
    detail: string;
    data?: any;   
  }