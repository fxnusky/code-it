'use client';
import { useState, useEffect } from 'react';
import styles from '../page.module.css';
import PlayerService from '../../../services/player.service';
import { useWSConnection } from '../../../contexts/ws_connection_context';
import { useCallback } from 'react';
import { useRouter } from 'next/navigation';

interface Player {
  id: string;
  nickname: string;
}

export default function Manager() {
  const [players, setPlayers] = useState<Player[]>([]);
  const [roomCode, setRoomCode] = useState('123456');
  const [state, setState] = useState('');
  const [questionIds, setQuestionIds] = useState<number[]>([]);
  const [questionIndex, setQuestionIndex] = useState(0);
  const connectionService = useWSConnection();
  const router = useRouter();

  
  const handleMessage = (message: string) => {
    console.log('Received game message:', message);
    const message_json = JSON.parse(message);
    if (message_json.action === "room_opened"){
      setState(message_json.action);
      setQuestionIds([1, 2, 3, 4]);
      // set room_code and question ids in order
    }else if (message_json.action === "player_joined"){
      fetchPlayers();
    }else if (message_json.action === "question"){
      setState(message_json.action);
      // recieve question and set it
    }else if (message_json.action === "player_submitted"){
      // set the amount of submissions
    }else if (message_json.action === "question_results"){
      setState(message_json.action);
      // recieve question results and set it
    }else if (message_json.action === "ranking"){
      setState(message_json.action);
      // recieve ranking and set it
    }else{
      console.error("Unknown message from server ", message)
    }
    
  };

  const handleStartGame = () =>{
    // Send question id
    connectionService.sendMessage({"action": "start_game"})
  }
  const handleEndQuestion = () =>{
    // Send question id
    connectionService.sendMessage({"action": "end_question"})
  }
  const handleNextQuestion = () =>{
    if (questionIndex +1 < questionIds.length){
      setQuestionIndex(questionIndex + 1)
      // Send question id
      connectionService.sendMessage({"action": "next_question"})
    }else{
      connectionService.sendMessage({"action": "end_game"})
    }
  }
  const handleShowRanking = () =>{
    connectionService.sendMessage({"action": "show_ranking"})
  }

  useEffect(() => {
    connectionService.addMessageHandler(handleMessage);
    setRoomCode("123456");
  }, [connectionService]);

  const fetchPlayers = useCallback(async () => {
    const response = await PlayerService.getPlayers({ room_code: roomCode });
    if (response && response.data) {
      setPlayers(response.data);
    }
  }, [roomCode]);

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
          <button className={styles.button} onClick={handleStartGame}>Start Game</button>
        </div>
      )}
      {state == "question" &&  (
        <button className={styles.button} onClick={handleEndQuestion}>End questions and show results</button>
      )}
      {state == "question_results" &&  (
        <button className={styles.button} onClick={handleShowRanking}>Show ranking</button>
      )}
      {state == "ranking" &&  (
        <button className={styles.button} onClick={handleNextQuestion}>Next question</button>
      )}
      {state == "game_ended" &&  (
        <button className={styles.button} onClick={() => {router.push("/join-game")}}>Close</button>
      )}
    </div>
  );
}