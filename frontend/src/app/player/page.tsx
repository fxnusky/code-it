'use client';
import styles from '../page.module.css'
import { useState, useEffect } from 'react';
import { useWSConnection } from '../../../contexts/ws_connection_context';
import { useRouter } from 'next/navigation';
import { GameMessage } from '../../../services/ws_connection.service';
import { PlayerRoom } from '../../../components/player_room';

export default function Profile() {
    //TODO: improve
    const [roomCode] = useState("123456");
    const [nickname] = useState("John Doe");
    const [state, setState] = useState('')
    const connectionService = useWSConnection();
    const router = useRouter();

    useEffect(() => {
        connectionService.addMessageHandler(handleMessage);
        const messages = connectionService.popMessages();
            messages.forEach(message => {
                handleMessage(message);
            });
    }, [connectionService]);

    const handleMessage = (message: GameMessage) => {
        console.log('Received game message:', message);
        if (message.action === "joined"){
            setState("room");
        }else if (message.action === "question"){
            setState(message.action);
    
        }else if (message.action === "question_submitted"){
            setState(message.action);
      
        }else if (message.action === "question_results"){
            setState(message.action);
    
        }else if (message.action === "ranking"){
            setState(message.action);
    
        }else if (message.action === "game_ended"){
            setState(message.action);
    
        }else{
            console.error("Unknown message from server ", message)
        }
        
      };
    
    const handleSubmitQuestion = () => {
        connectionService.sendMessage({"action": "submit_question"})
    }

    return (
        <div className={styles.container}>
            {state == "room" &&  (
                <PlayerRoom room_code={roomCode} nickname={nickname}></PlayerRoom>
            )}
            {state == "question" &&  (
                <button className={styles.button} onClick={handleSubmitQuestion}>Send question</button>
            )}
            {state == "question_submitted" &&  (
                <p>Question submitted!</p>
            )}
            {state == "question_results" &&  (
                <p>Question results</p>
            )}
            {state == "ranking" &&  (
                <p>Ranking</p>
            )}
            {state == "game_ended" &&  (
                <button className={styles.button} onClick={() => {router.push("/join-room")}}>Close</button>
            )}
        </div>
    );
}