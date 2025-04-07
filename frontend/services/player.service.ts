import endpoint from "../endpoints.config";
import { ApiResponse } from "./api_response";

const PlayerService = {
    getPlayers: async ({ room_code }: { room_code: string }): Promise<ApiResponse | null> => {
      console.log("room_Code", room_code);
        try {
          if (!room_code || typeof room_code !== "string") {
            throw new Error("Invalid room code");
          }
    
          const url = new URL(endpoint.dbURL + "/players");
          url.searchParams.append("room_code", room_code);
    
          const response = await fetch(url.toString());
    
          if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(
              errorData.error || `Request failed with status ${response.status}`
            );
          }
    
          const data: ApiResponse = await response.json();
          if (!data || data.status !== "success") {
            throw new Error(data.detail || "Invalid response from server");
          }
    
          return data;
        } catch (error) {
          console.error("Failed to fetch players:", error);
          
          return {
            status: "error",
            detail: error instanceof Error ? error.message : "Unknown error occurred",
          };
        }
      },
    };

export default PlayerService;