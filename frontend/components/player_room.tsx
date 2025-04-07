'use client';
import styles from './room.module.css'; 

type PlayerRoomProps = {
  room_code: string;
  nickname: string;
};

export const PlayerRoom = ({
    room_code,
    nickname
}: PlayerRoomProps) => {
  
  return (
    <div className={styles.player_content}>
        <div className={styles.card}>
            {nickname}
        </div>
        <p className={styles.text}>You joined the room {room_code}.</p>
        <p className={styles.text}>Wait for the manager to start the game.</p>
    </div>
  );
};