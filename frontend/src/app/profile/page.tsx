'use client';
import { RequireAuth } from "../../../components/require_auth";
import styles from '../page.module.css';
import { useRouter } from 'next/navigation';
import { connectionService } from '../../../services/ws_connection.service';
import { useState } from 'react';
import { useWSConnection } from "../../../contexts/ws_connection_context";

export default function Profile() {
  const router = useRouter();
  const connectionService = useWSConnection();

  
      const handleMessage = (message: string) => {
        console.log('Received game message:', message);
      };
      const connect = async () => {
        try {
            await connectionService.manager_connect();
            
            connectionService.addMessageHandler(handleMessage);
            
        } catch (error) {
            console.error('Connection failed:', error);
        }
      };
      function handleStartGame(){
          connect();
          router.push("/game-manager")
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