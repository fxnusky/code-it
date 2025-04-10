'use client';
import styles from './question.module.css'; 
import { Question } from '../services/ws_connection.service';
type PlayerQuestionProps = {
  question: Question;
  num_players: number;
  num_questions: number;
  question_index: number;
  handleEndQuestion: () => void;
};

export const PlayerQuestion = ({
    question,
    num_questions,
    question_index,
}: PlayerQuestionProps) => {
  return (
    <div className={styles.question_container}>
      <div className={styles.main_section}>
        <h1 className={styles.question_title}>QUESTION {question_index + 1}/{num_questions}</h1>
        <p className={styles.question_description}>{question.description}</p>
      </div>
      <div className={styles.side_section}>
        
      </div>
    </div>
  );
};