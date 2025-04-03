'use client';
import { useState, useEffect } from 'react';
import styles from '../page.module.css';
import PlayerService from '../../../services/player.service';
import { useWSConnection } from '../../../contexts/ws_connection_context';
import { useCallback } from 'react';

interface Player {
  id: string;
  nickname: string;
}

export default function Manager() {
  const [players, setPlayers] = useState<Player[]>([]);
  const [roomCode, setRoomCode] = useState('123456');
  const [state, setState] = useState('')
  const connectionService = useWSConnection();
  useEffect(() => {
    connectionService.sendMessage({"action": "confirm_manager"})
    setRoomCode("123456");
  }, [connectionService]);

  const fetchPlayers = useCallback(async () => {
    const response = await PlayerService.getPlayers({ room_code: roomCode });
    if (response && response.data) {
      setPlayers(response.data);
    }
  }, [roomCode]);

  useEffect(() => {
    if (roomCode) {
      fetchPlayers();
    }
  }, [roomCode, fetchPlayers]);


  return (
    <div className={styles.container}>
      {state == "room_opened" &&  (
        <div>
          <h2>Players: ({players.length})</h2>
          <ul>
            {players.map(player => (
                <li key={player.id}>{player.nickname}</li>
            ))}
          </ul>
        </div>
      )}
      {state == "question" &&  (
        <button className={styles.button}>End questions and show results</button>
      )}
      {state == "question_results" &&  (
        <button className={styles.button}>Show ranking</button>
      )}
      {state == "ranking" &&  (
        <button className={styles.button}>Show ranking</button>
      )}
      {state == "game_ended" &&  (
        <button className={styles.button}>Close</button>
      )}
    </div>
  );
}