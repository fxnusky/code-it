export interface ApiResponse<T = any> {
    status: "success" | "error";
    status_code?: number;
    detail: string;
    data?: T;   
  }