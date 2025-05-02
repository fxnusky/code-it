'use client';
import { RequireAuth } from "../../../components/require_auth";
import styles from '../page.module.css';
import { useRouter } from 'next/navigation';
import { useAuth } from "../../../contexts/auth_context";
import RoomService from "../../../services/room.service";
import { ApiResponse } from "../../../services/api_response";
import { Button } from "@/components/ui/button"
import { useState } from "react";
import { LoadingState } from "../../../components/loading_state";

export default function Profile() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const {token} = useAuth();

  async function handleStartGame(){
    try{
      setIsLoading(true);
      const template_id = 1;
      const response: ApiResponse | null = await RoomService.createRoom({template_id, token});
      
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
      {isLoading? (
        <LoadingState text=""></LoadingState>
      ):(
        <div className={styles.container}>
          <Button onClick={handleStartGame}>
              Start a Game
          </Button>
        </div>
      )}
    </RequireAuth>
  );
}