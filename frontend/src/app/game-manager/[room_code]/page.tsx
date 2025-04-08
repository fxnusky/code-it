'use client';
import { useState, useEffect, useCallback, useRef } from 'react';
import styles from '../../page.module.css';
import { useWSConnection } from '../../../../contexts/ws_connection_context';
import { useRouter } from 'next/navigation';
import { GameMessage } from '../../../../services/ws_connection.service';
import { ManagerRoom } from '../../../../components/manager_room';
import PlayerService from '../../../../services/player.service';
import { useParams } from 'next/navigation';
import { useAuth } from '../../../../contexts/auth_context';

export interface Player {
  id: string;
  nickname: string;
}

export default function Manager() {
  const [players, setPlayers] = useState<Player[]>([]);
  const [roomCode, setRoomCode] = useState('');
  const [state, setState] = useState('');
  const [questionIds, setQuestionIds] = useState<number[]>([]);
  const [questionIndex, setQuestionIndex] = useState(0);
  const connectionService = useWSConnection();
  const router = useRouter();
  const roomCodeRef = useRef(roomCode);
  const { room_code }: {room_code: string} = useParams(); 
  const { token } = useAuth();

  useEffect(() => {
    roomCodeRef.current = roomCode;
  }, [roomCode]);

  const fetchPlayers = useCallback(async () => {
    const currentRoomCode = roomCodeRef.current;
    if (!currentRoomCode) {
      console.error("No room code available");
      return;
    }
    const response = await PlayerService.getPlayers({ room_code: currentRoomCode });
    if (response && response.data) {
      setPlayers(response.data);
    }
  }, []); 

  
  const handleMessage = (message: GameMessage) => {
    console.log('Received game message:', message);
    if (message.action === "player_joined"){
      fetchPlayers();
    }else if (message.action === "question"){
      setState(message.action);
      // recieve question and set it
    }else if (message.action === "player_submitted"){
      // set the amount of submissions
    }else if (message.action === "question_results"){
      setState(message.action);
      // recieve question results and set it
    }else if (message.action === "ranking"){
      console.log("state handleRankingMessage", state);
      setState(lastState => lastState !== "game_ended"? message.action: "game_ended");
      // recieve ranking and set it
    }else if (message.action === "status"){
      if(message.status){
        setState(message.status)
      }
      if(message.question_ids){
        setQuestionIds(message.question_ids)
      }
      if(message.players){
        setPlayers(message.players)
      }
      if(message.current_question_id && message.question_ids){
        setQuestionIndex(message.question_ids.indexOf(message.current_question_id))
      }
    }else{
      console.error("Unknown message from server ", message)
    }
    
  };

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
      setState("game_ended");
      connectionService.sendMessage({"action": "end_game"})
    }
  }
  const handleShowRanking = () =>{
    connectionService.sendMessage({"action": "show_ranking"})
  }

  useEffect(() => {
    const connectToRoom = async () => {
      try {
        connectionService.addMessageHandler(handleMessage);
        await connectionService.manager_connect(token, room_code); 

      } catch (error) {
        console.error('Connection error:', error);
      }
    };

    if (token && room_code) {
      connectToRoom();
    }
  }, [connectionService, token, room_code]);

  return (
    <div className={styles.container}>
      {state == "room_opened" &&  (
        <ManagerRoom room_code={roomCode} players={players}></ManagerRoom>
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
        <button className={styles.button} onClick={() => {router.push("/profile")}}>Close</button>
      )}
    </div>
  );
}