'use client';
import styles from '../../page.module.css'
import { useState, useEffect } from 'react';
import { useWSConnection } from '../../../../contexts/ws_connection_context';
import { useRouter } from 'next/navigation';
import { GameMessage } from '../../../../services/ws_connection.service';
import { PlayerRoom } from '../../../../components/player_room';
import { useParams } from 'next/navigation';
import PlayerService from '../../../../services/player.service';
import { ApiResponse } from '../../../../services/api_response';
import { Question } from '../../../../services/ws_connection.service';
import { Button } from "@/components/ui/button"
import { PlayerQuestion } from '../../../../components/player_question';

export default function Profile() {
    const [roomCode, setRoomCode] = useState("");
    const [nickname, setNickname] = useState("");
    const [state, setState] = useState('')
    const [isManagerConnected, setIsManagerConnected] = useState(true);
    const [question, setQuestion] = useState<Question>();
    const connectionService = useWSConnection();
    const router = useRouter();
    const { token }: {token: string} = useParams(); 

    useEffect(() => {
        const getPlayerAndConnect = async () => {
            if (!token) return;
            
            try {
                const response: ApiResponse | null = await PlayerService.getPlayer({token});
                if (!response?.data) return;
                const { room_code, nickname } = response.data;
                setRoomCode(room_code);
                setNickname(nickname);
                
                connectionService.addMessageHandler(handleMessage);
                await connectionService.player_connect(room_code, nickname, token);
            } catch (error) {
                console.error('Error:', error);
                setState("error");
            }
        };
    
        getPlayerAndConnect();
    }, [token, connectionService]); 

    const handleMessage = (message: GameMessage) => {
        console.log('Received game message:', message);
        if (message.action === "status"){
            if (message.state){
                setState(message.state);
            }
            if (message.nickname){
                setNickname(message.nickname);
            }
            if (message.room_code){
                setRoomCode(message.room_code);
            }
            if (message.manager_connected){
                setIsManagerConnected(message.manager_connected);
            }
        }else if (message.action === "question"){
            if (message.question){
                setQuestion(message.question);
            }
            setState(message.action);
        }else if (message.action === "question_submitted"){
            setState(message.action);
      
        }else if (message.action === "question_results"){
            setState(message.action);
    
        }else if (message.action === "ranking"){
            setState(message.action);
    
        }else if (message.action === "game_ended"){
            setState(message.action);
        }else if (message.action === "manager_disconnected"){
            setIsManagerConnected(false);
        }else if (message.action === "manager_connected"){
            setIsManagerConnected(true);
        }else{
            console.error("Unknown message from server ", message)
        }
      };
    
    const handleSubmitQuestion = () => {
        connectionService.sendMessage({"action": "submit_question"})
    }

    return (
        <div className={styles.container}>
            {!isManagerConnected &&(
                <p className={styles.errorText}>The room manager has disconnected.</p>
            )}
            {state == "joined" &&  (
                <PlayerRoom room_code={roomCode} nickname={nickname}></PlayerRoom>
            )}
            {state == "question" && question !== undefined &&  (
                <PlayerQuestion question={question} handleSubmitQuestion={handleSubmitQuestion}></PlayerQuestion>
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
                <Button onClick={() => {router.push("/join-room")}}>Close</Button>
            )}
            {state == "error" &&  (
                <div className={styles.container}>
                    <p>You cannot access this room</p>
                    <Button onClick={() => {router.push("/join-room")}}>Go back</Button>
                </div>
            )}
        </div>
    );
}