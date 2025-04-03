'use client';
import styles from '../page.module.css'
import { useState, useEffect } from 'react';
import { useWSConnection } from '../../../contexts/ws_connection_context';

export default function Profile() {
    //TODO: improve
    const [roomCode] = useState("123456");
    const [nickname] = useState("John Doe");
    const connectionService = useWSConnection();
    useEffect(() => {
        connectionService.sendMessage({"action": "confirm_player"})
    }, [connectionService]);
    
    

    return (
        <div className={styles.container}>
            <div className={styles.card}>
                <p className={styles.title}>{nickname}</p>
            </div>
            <p className={styles.createGameText}>You joined the room {roomCode}.</p>
        </div>
    );
}