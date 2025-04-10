'use client';
import { useWSConnection } from '../contexts/ws_connection_context';
import styles from './room.module.css'; 
import { Player } from '../src/app/game-manager/[room_code]/page';

type ManagerRoomProps = {
  room_code: string;
  players: Player[];
};

export const ManagerRoom = ({
    room_code,
    players
}: ManagerRoomProps) => {
  const connectionService = useWSConnection();

  const handleStartGame = () =>{
    // Send question id
    connectionService.sendMessage({"action": "start_game"})
  }
  
  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.roomCodeContainer}>
          <span className={styles.roomCodeLabel}>Room Code:</span>
          <div className={styles.roomCode}>{room_code}</div>
        </div>
        <div className={styles.playerCount}>
          <span className={styles.playerCountNumber}>{players.length}</span>
          <span className={styles.playerCountLabel}>players</span>
        </div>
      </div>

      <div className={styles.playersWall}>
        {players.map(player =>(
          <div key={player.id} className={styles.card}>{player.nickname}</div>
        ))
        }
      </div>

      <div className={styles.footer}>
        <button 
          className={styles.startButton} 
          onClick={handleStartGame}
          disabled={players.length === 0}
        >
          START
        </button>
      </div>
    </div>
  );
};