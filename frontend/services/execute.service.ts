import endpoint from "../endpoints.config";
import { ApiResponse } from "./api_response";

const ExecuteService = {
      runCode: async ({ code }: { code: string }): Promise<ApiResponse | null> => {
        try {
          const response = await fetch(`${endpoint.isolateURL}/execute/python`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                code,
            }),
          });
          
          if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(
              errorData.detail || `Request failed with status ${response.status}`
            );
          }
          const data = await response.json();
          console.log(data)
          if (data.status === "error") {
            throw new Error(data.detail || "Code execution failed");
          }
    
          return data;
          
        } catch (error) {
          console.error("Failed to execute code:", error);
          return {
            status: "error",
            detail: error instanceof Error ? error.message : "Unknown error occurred",
          };
        }
      }
    };

    

export default ExecuteService;