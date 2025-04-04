'use client';
import styles from '../page.module.css'
import { useState, useEffect } from 'react';
import { useWSConnection } from '../../../contexts/ws_connection_context';
import { useRouter } from 'next/navigation';

export default function Profile() {
    //TODO: improve
    const [roomCode] = useState("123456");
    const [nickname] = useState("John Doe");
    const [state, setState] = useState('')
    const connectionService = useWSConnection();
    const router = useRouter();

    useEffect(() => {
        connectionService.addMessageHandler(handleMessage);
        connectionService.sendMessage({"action": "confirm_player"})
    }, [connectionService]);

    const handleMessage = (message: string) => {
        console.log('Received game message:', message);
        const message_json = JSON.parse(message);
        if (message_json.action === "joined"){
            setState("room");
        }else if (message_json.action === "question"){
            setState(message_json.action);
    
        }else if (message_json.action === "question_submitted"){
            setState(message_json.action);
      
        }else if (message_json.action === "question_results"){
            setState(message_json.action);
    
        }else if (message_json.action === "ranking"){
            setState(message_json.action);
    
        }else if (message_json.action === "game_ended"){
            setState(message_json.action);
    
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
                <div>
                    <div className={styles.card}>
                        <p className={styles.title}>{nickname}</p>
                    </div>
                    <p className={styles.createGameText}>You joined the room {roomCode}.</p>
                </div>
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
                <button className={styles.button} onClick={() => {router.push("/profile")}}>Close</button>
            )}
        </div>
    );
}