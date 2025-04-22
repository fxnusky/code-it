'use client';
import styles from './results.module.css';
import { Button } from "@/components/ui/button"
import { ManagerResult } from '../services/ws_connection.service';

type ManagerResultsProps = {
  results: ManagerResult[];
  handleShowRanking: () => void;
};

export const ManagerResults = ({
  results,
  handleShowRanking
}: ManagerResultsProps) => {
  return (
    <div className={styles.container}>
      <div className={styles.playersWall}>
        {results.map((result, index) => (
          <div key={index} className={styles.resultContainer}>
            <div className={styles.resultBarBackground}>
              <div className={styles.resultLabel}>
                TEST {index + 1}
                <div className={styles.percentageText}>
                  {Math.round(result.percentage_correct || 0)}%
                </div>
              </div>
              <div 
                  className={`${styles.resultBarFill} ${
                  result.percentage_correct || 0 >= 50 ? styles.green : styles.red
                  }`}
                  style={{ width: `${result.percentage_correct || 0}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      <div className={styles.footer}>
        <Button onClick={handleShowRanking}>
          NEXT
        </Button>
      </div>
    </div>
  );
};