'use client';
import { useState, useEffect, useCallback } from 'react';
import styles from '../../page.module.css';
import { useWSConnection } from '../../../../contexts/ws_connection_context';
import { useRouter } from 'next/navigation';
import { GameMessage } from '../../../../services/ws_connection.service';
import { ManagerRoom } from '../../../../components/manager_room';
import PlayerService from '../../../../services/player.service';
import { useParams } from 'next/navigation';
import { useAuth } from '../../../../contexts/auth_context';
import { Question } from '../../../../services/ws_connection.service';
import { ManagerQuestion } from '../../../../components/manager_question';
import { Button } from "@/components/ui/button"

export interface Player {
  id: string;
  nickname: string;
}

export default function Manager() {
  const [players, setPlayers] = useState<Player[]>([]);
  const [state, setState] = useState('');
  const [questionIds, setQuestionIds] = useState<number[]>([]);
  const [question, setQuestion] = useState<Question | null>(null);
  const [questionIndex, setQuestionIndex] = useState(0);
  const [submissions, setSubmissions] = useState(0);
  const connectionService = useWSConnection();
  const router = useRouter();
  const { room_code }: {room_code: string} = useParams(); 
  const { token } = useAuth();

  const fetchPlayers = useCallback(async () => {
    const response = await PlayerService.getPlayers({ room_code: room_code });
    if (response && response.data) {
      setPlayers(response.data);
    }
  }, []); 

  
  const handleMessage = (message: GameMessage) => {
    console.log('Received game message:', message);
    if (message.action === "player_joined" || message.action === "player_disconnected"){
      fetchPlayers();
    }else if (message.action === "question"){
      if (message.question){
        setQuestion(message.question);
      }
      setState(message.action);
    }else if (message.action === "player_submitted"){
      setSubmissions(prevSubmissions => prevSubmissions + 1);
    }else if (message.action === "question_results"){
      setState(message.action);
      // recieve question results and set it
    }else if (message.action === "ranking"){
      setState(lastState => lastState !== "game_ended"? message.action: "game_ended");
      // recieve ranking and set it
    }else if (message.action === "status"){
      if(message.state){
        setState(message.state)
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
      if (message.question){
        setQuestion(message.question);
      }
    }else{
      console.error("Unknown message from server ", message)
    }
    
  };

  const handleEndQuestion = () =>{
    // Send question id
    localStorage.removeItem(`time_start`);
    connectionService.sendMessage({"action": "end_question"})
  }
  const handleNextQuestion = () =>{
    setSubmissions(0);
    let nextIndex = questionIndex +1;
    if (nextIndex < questionIds.length){
      setQuestionIndex(nextIndex)
      // Send question id
      connectionService.sendMessage({"action": "next_question", "question_id": questionIds[nextIndex]})
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
        setState("error");
      }
    };

    if (token && room_code) {
      connectToRoom();
    }
  }, [connectionService, token, room_code]);

  const handleStartGame = () =>{
    connectionService.sendMessage({"action": "start_game", "question_id": questionIds[questionIndex]})
  }
  return (
    <div className={styles.container}>
      {state == "room_opened" &&  (
        <ManagerRoom room_code={room_code} players={players} handleStartGame={handleStartGame}></ManagerRoom>
      )}
      {state == "question" && question && (
        <ManagerQuestion question={question} submissions={submissions} num_players={players.length} num_questions={questionIds.length} question_index={questionIndex} handleEndQuestion={handleEndQuestion}></ManagerQuestion>
      )}
      {state == "question_results" &&  (
        <Button onClick={handleShowRanking}>Show ranking</Button>
      )}
      {state == "ranking" &&  (
        <Button onClick={handleNextQuestion}>Next question</Button>
      )}
      {state == "game_ended" &&  (
        <Button onClick={() => {router.push("/profile")}}>Close</Button>
      )}
      {state == "error" &&  (
        <div className={styles.container}>
          <p>You cannot access this room</p>
          <Button onClick={() => {router.push("/profile")}}>Back to profile</Button>
        </div>
      )}
    </div>
  );
}