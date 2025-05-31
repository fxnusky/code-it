import endpoint from "../endpoints.config";
import { ApiResponse } from "./api_response";

const RoomService = {
    createRoom: async ({ template_id, token, override }: { template_id: number, token: string, override: boolean }): Promise<ApiResponse | null> => {
        const response = await fetch(endpoint.dbURL +'/rooms', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ "token": token, "template_id": template_id, "override": override }),
          });
          const data = await response.json();
          if (data.status === "success") {
            return {
              status: "success",
              detail: data.detail,
              data: data.data
            };
          } else {
            console.error('Room creation failed:', data.detail);
            return {
                status: "error",
                status_code: response.status,
                detail: data.detail?.message || data.detail || "Unknown error",
                data: data.detail?.data || null
            };
          }
        }
    };

export default RoomService;