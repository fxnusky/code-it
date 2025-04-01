'use client';
import styles from '../page.module.css'
import { useState } from 'react';

export default function Profile() {
    //TODO: improve
    const [roomCode, setRoomCode] = useState("123456");
    const [nickname, setNickname] = useState("John Doe");

    return (
        <div className={styles.container}>
            <div className={styles.card}>
                <p className={styles.title}>{nickname}</p>
            </div>
            <p className={styles.createGameText}>You joined the room {roomCode}.</p>
        </div>
    );
}