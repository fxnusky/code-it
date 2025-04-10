'use client';
import { RequireAuth } from "../../../components/require_auth";
import styles from '../page.module.css';
import { useRouter } from 'next/navigation';
import { useAuth } from "../../../contexts/auth_context";
import RoomService from "../../../services/room.service";
import { ApiResponse } from "../../../services/api_response";

export default function Profile() {
  const router = useRouter();

  const {token} = useAuth();

  async function handleStartGame(){
    try{
      let template_id = 1;
      let response: ApiResponse<any> | null = await RoomService.createRoom({template_id, token});
      
      if (response && response.status == "success") {
          router.push(`/game-manager/${response.data["room_code"]}`);
      }else{
        console.error('Connection failed:', response?.detail);
      }
    }
    catch (error) {
      console.error('Connection failed:', error);
    }
  }

  return (
    <RequireAuth>
      <div className={styles.container}>
          <button className={styles.primaryButton} onClick={handleStartGame}>
              Start a Game
          </button>
      </div>
    </RequireAuth>
  );
}