import endpoint from "../endpoints.config";
import { ApiResponse } from "./api_response";

const RoomService = {
    createRoom: async ({ template_id, token }: { template_id: number, token: string }): Promise<ApiResponse | null> => {
        const response = await fetch(endpoint.dbURL +'/rooms', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ "token": token, "template_id": template_id }),
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
              detail: data.detail
            };
          }
        }
    };

export default RoomService;