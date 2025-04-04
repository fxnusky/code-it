import endpoint from "../endpoints.config";
import { ApiResponse } from "./api_response";

const AuthService = {
  authenticateUser: async ({ credentialResponse }: { credentialResponse: any }): Promise<ApiResponse | null> => {    
    const response = await fetch(endpoint.dbURL +'/validate-token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token: credentialResponse.credential }),
    });
    const data = await response.json();
    if (data.status === "success") {
      return {
        status: "success",
        detail: data.detail,
        data: data.data
      };
    } else {
      console.error('Token validation failed:', data.detail);
      return {
        status: "error",
        detail: data.detail
      };
    }
  }
}

export default AuthService;