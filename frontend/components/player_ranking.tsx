'use client';
import styles from './ranking.module.css';

type PlayerRankingProps = {
  position: number;
  nickname: string;
  points: number;
};

export const PlayerRanking = ({
    position,
    nickname,
    points,
}: PlayerRankingProps) => {
  return (
    <div className={styles.playerContainer}>
        <div className={styles.playerRanking}>
            <span className={styles.nickname}>{position}</span>
            <span className={styles.nickname}>{nickname}</span>
            <span className={styles.points}>{points} pts</span>
        </div>
    </div>
  );
};