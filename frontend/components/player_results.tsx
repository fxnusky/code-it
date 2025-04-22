'use client';
import styles from './results.module.css';
import { PlayerResult } from '../services/ws_connection.service';

type PlayerResultsProps = {
  nickname: string,
  results: PlayerResult;
};

export const PlayerResults = ({
nickname,
  results
}: PlayerResultsProps) => {
  return (
    <div className={styles.container}>
      <div className={styles.header}> 
        <p className={styles.headerText}>{nickname}</p>
        <p className={styles.headerText}>Total points: {results.total_points}</p>
      </div>
      <div className={`${styles.earnedPoints}`} >
              <div className={styles.resultLabel}>
                +{results.question_points} points
              </div>
            </div>
      <div className={styles.playersWall}>
        {results.test_case_executions.map((result, index) => (
          <div key={index} className={styles.resultContainer}>
            <div className={`${styles.resultBarBackground} ${
                  result.correct? styles.green : styles.red
                  }`} >
              <div className={styles.resultLabel}>
                TEST {index + 1}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};