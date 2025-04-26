'use client';
import styles from './ranking.module.css';
import { Button } from "@/components/ui/button"

type ManagerRankingProps = {
  ranking: [string, number][];
  handleNextQuestion: () => void;
};

export const ManagerRanking = ({
  ranking,
  handleNextQuestion
}: ManagerRankingProps) => {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Leaderboard</h1>
      
      <div className={styles.playersWall}>
        <div className={styles.rankingHeader}>
          <span>Rank</span>
          <span>Player</span>
          <span>Points</span>
        </div>
        
        {ranking.map(([nickname, points], index) => (
          <div key={index} className={styles.playerRow}>
            <span className={styles.rank}>#{index + 1}</span>
            <span className={styles.nickname}>{nickname}</span>
            <span className={styles.points}>{points} pts</span>
          </div>
        ))}
      </div>

      <div className={styles.footer}>
        <Button onClick={handleNextQuestion}>
          NEXT
        </Button>
      </div>
    </div>
  );
};