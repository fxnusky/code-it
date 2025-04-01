'use client';
import { RequireAuth } from "../../../components/require_auth";
import styles from '../page.module.css';
import { useRouter } from 'next/navigation';

export default function Profile() {
  const router = useRouter();

  return (
    <RequireAuth>
      <div className={styles.container}>
          <button className={styles.primaryButton} onClick={() => router.push("/game-manager")}>
              Start a Game
          </button>
      </div>
    </RequireAuth>
  );
}