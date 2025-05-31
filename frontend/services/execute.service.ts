import endpoint from "../endpoints.config";
import { ApiResponse } from "./api_response";

const ExecuteService = {
      runCode: async ({ code, language }: { code: string, language: string }): Promise<ApiResponse | null> => {
        try {
          const response = await fetch(`${endpoint.isolateURL}/execute`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                code,
                language
            }),
          });
          
          if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(
              errorData.detail || `Request failed with status ${response.status}`
            );
          }
          const data = await response.json();
          return data;
          
        } catch (error) {
          console.error("Failed to execute code:", error);
          return {
            status: "error",
            data: error instanceof Error ? error : "Unknown error occurred",
          };
        }
      },

      submitCode: async ({code, token, question_id, main_function, language} : {code: string, token: string, question_id: number, main_function: string, language: string}): Promise<ApiResponse | null> => {
        try {
          const response = await fetch(`${endpoint.dbURL}/submit`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                code,
                token,
                question_id,
                main_function,
                language
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
            throw new Error(data.detail || "Code submission failed");
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