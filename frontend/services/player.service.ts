import endpoint from "../endpoints.config";
import { ApiResponse } from "./api_response";

const PlayerService = {
    getPlayers: async ({ room_code }: { room_code: string }): Promise<ApiResponse | null> => {
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
    getPlayer: async ({ token }: { token: string }): Promise<ApiResponse | null> => {
        try {
          if (!token || typeof token !== "string") {
            throw new Error("Invalid token");
          }
    
          const url = new URL(endpoint.dbURL + "/player/" + token);
    
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
          console.error("Failed to fetch player:", error);
          
          return {
            status: "error",
            detail: error instanceof Error ? error.message : "Unknown error occurred",
          };
        }
      },
      createPlayer: async ({ nickname, roomCode }: { nickname: string, roomCode: string }): Promise<ApiResponse | null> => {
        try {
          const response = await fetch(`${endpoint.dbURL}/players`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              nickname,
              room_code: roomCode
            }),
          });
          console.log(response)
          
          if (!response.ok) {
            if (response.status === 409 || response.status === 403 || response.status === 405){
              const data = await response.json();
              return {
                "status": "error",
                "status_code": response.status,
                "detail": data.detail
              }
            }
            const errorData = await response.json().catch(() => ({}));
            throw new Error(
              errorData.detail || `Request failed with status ${response.status}`
            );
          }
          const data = await response.json();
          if (data.status !== "success") {
            throw new Error(data.detail || "Player creation failed");
          }
    
          return data;
          
        } catch (error) {
          console.error("Failed to create player:", error);
          return {
            status: "error",
            detail: error instanceof Error ? error.message : "Unknown error occurred",
          };
        }
      }
    };

    

export default PlayerService;