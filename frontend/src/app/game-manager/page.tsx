'use client';
import { useState, useEffect } from 'react';
import styles from '../page.module.css';
import PlayerService from '../../../sevices/player.service';

interface Player {
  id: string;
  nickname: string;
}

export default function Manager() {
  const [players, setPlayers] = useState<Player[]>([]);
  const [roomCode, setRoomCode] = useState('123456');

  const fetchPlayers = async () => {

    const response = await PlayerService.getPlayers({ room_code: roomCode });
    if (response && response.data) {
        setPlayers(response.data);
    }
  };

  useEffect(() => {
    if (roomCode) {
      fetchPlayers();
    }
  }, [roomCode]);

  return (
    <div className={styles.container}>
        <h1>Player Manager</h1>
        <div className={styles.playerList}>
            <h2>Players: ({players.length})</h2>
            <ul>
            {players.map(player => (
                <li key={player.id}>{player.nickname}</li>
            ))}
            </ul>
        </div>
    </div>
  );
}