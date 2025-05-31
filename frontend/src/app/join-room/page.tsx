'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';
import styles from '../page.module.css';
import PlayerService from '../../../services/player.service';
import { Button } from "@/components/ui/button"
import { LoadingState } from '../../../components/loading_state';

export default function JoinGame() {
  const router = useRouter();
  const [roomCode, setRoomCode] = useState('');
  const [nickname, setNickname] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState({
    roomCode: '',
    nickname: ''
  });

  function handleJoinRoom() {
    let isValid = true;
    const newErrors = {
      roomCode: '',
      nickname: ''
    };

    if (!roomCode.trim()) {
      newErrors.roomCode = 'Room code is required';
      isValid = false;
    }else if (!/^\d{6}$/.test(roomCode)) {
      newErrors.roomCode = 'Room code must have 6 digits';
      isValid = false;
    }

    if (!nickname.trim()) {
      newErrors.nickname = 'Nickname is required';
      isValid = false;
    } else if (nickname.length > 20) {
      newErrors.nickname = 'Nickname must be less than 20 characters';
      isValid = false;
    }

    setErrors(newErrors);

    if (isValid) {
      setIsLoading(true);
      const connect = async () => {
        try {
          const response = await PlayerService.createPlayer({nickname, roomCode})
          if (response?.status == "success"){
            router.push(`/player/${response.data["token"]}`);
          }else {
            const apiErrors = {
              roomCode: '',
              nickname: ''
            };
            if (response?.status_code === 405 || response?.status_code === 403) {
              apiErrors.roomCode = response?.detail || 'does not exist';
            }
            
            if (response?.status_code === 409) {
              apiErrors.nickname = "This nickname is already taken in this room";
            }
            setErrors(apiErrors);
          }
        } catch (error) {
            console.error('Connection failed:', error);
        } finally{
            setIsLoading(true);
        }
      }
      connect();
    }
  }

  return (
    <div className={styles.container}>
      {isLoading? (
        <LoadingState></LoadingState>
      ):(
        <div className={styles.container}>
          <div className={styles.card}>
            <div className={styles.cardContent}>
              <h1 className={styles.title}>Join a game</h1>
              
              <div className={styles.inputContainer}>
                <input
                  type="text"
                  placeholder="Room code"
                  className={`${styles.inputField} ${errors.roomCode ? styles.errorInput : ''}`}
                  value={roomCode}
                  onChange={(e) => {
                    setRoomCode(e.target.value);
                    setErrors({...errors, roomCode: ''});
                  }}
                  required
                />
                {errors.roomCode && (
                  <p className={styles.errorText}>{errors.roomCode}</p>
                )}
              </div>

              <div className={styles.inputContainer}>
                <input
                  type="text"
                  placeholder="Your nickname"
                  className={`${styles.inputField} ${errors.nickname ? styles.errorInput : ''}`}
                  value={nickname}
                  onChange={(e) => {
                    setNickname(e.target.value);
                    setErrors({...errors, nickname: ''});
                  }}
                  required
                  maxLength={20}
                />
                {errors.nickname && (
                  <p className={styles.errorText}>{errors.nickname}</p>
                )}
              </div>

              <Button 
                onClick={handleJoinRoom}
                style={{ width: '100%' }}
              >
                Join Room
              </Button>
            </div>
          </div>   
          <div className={styles.card}>
            <div className={styles.cardContent}>
              <p className={styles.createGameText}>Want to host your own game?</p>
              <Button 
                onClick={() => router.push("/profile")}
                variant="secondary"
              >
                Enter the application
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}