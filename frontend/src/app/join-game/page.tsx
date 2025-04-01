'use client';

import { useRouter } from 'next/navigation';
import styles from '../page.module.css'

export default function JoinGame() {
  const router = useRouter();

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <div className={styles.cardContent}>
          <h1 className={styles.title}>Join a game</h1>
          <input
            type="text"
            placeholder="Room code"
            className={styles.inputField}
            required
          />
          <input
            type="text"
            placeholder="Your nickname"
            className={styles.inputField}
            required
          />
          <button 
            onClick={() => router.push("/profile")}
            className={styles.primaryButton}
            style={{ width: '100%' }}
          >
            Join Room
          </button>
        </div>
      </div>   
      <div className={styles.card}>
        <div className={styles.cardContent}>
          
          <p className={styles.createGameText}>Want to create your own game?</p>
          
          <button 
            onClick={() => router.push("/profile")}
            className={styles.secondaryButton}
          >
            Enter the application
          </button>
        </div>
      </div>
    </div>
  );
}