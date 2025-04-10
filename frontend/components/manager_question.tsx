'use client';
import styles from './question.module.css'; 
import { Question } from '../services/ws_connection.service';
import { useState, useEffect } from 'react';
type ManagerQuestionProps = {
  question: Question;
  num_players: number;
  num_questions: number;
  question_index: number;
  handleEndQuestion: () => void;
};

export const ManagerQuestion = ({
    question,
    num_players,
    num_questions,
    question_index,
    handleEndQuestion,
}: ManagerQuestionProps) => {
  const [timeLeft, setTimeLeft] = useState(question.time_limit); 
  const [submissions, setSubmissions] = useState(0); 


  useEffect(() => {
    if (timeLeft <= 0) {
        handleEndQuestion(); 
      return;
    }

    const timer = setInterval(() => {
      setTimeLeft(prevTime => prevTime - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft, handleEndQuestion]);


  
  return (
    <div className={styles.question_container}>
      <div className={styles.main_section}>
        <h1 className={styles.question_title}>QUESTION {question_index + 1}/{num_questions}</h1>
        <p className={styles.question_description}>{question.description}</p>
      </div>
      <div className={styles.side_section}>
        <div className={styles.controls_container}>
          <div className={styles.numbers}>{submissions}/{num_players}</div>
          <div className={styles.text}>
            SUBMISSIONS
          </div>
        </div>
        <div className={styles.controls_container}>
          <div className={styles.text}>Time</div>
          <div className={styles.numbers}>{timeLeft}s</div>
        </div>
        <button className={styles.next_button} onClick={handleEndQuestion}>NEXT</button>
      </div>
    </div>
  );
};