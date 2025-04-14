'use client';
import styles from './question.module.css'; 
import { Question } from '../services/ws_connection.service';
import { useState, useEffect } from 'react';
import { Button } from "@/components/ui/button"

type ManagerQuestionProps = {
  question: Question;
  num_players: number;
  num_questions: number;
  question_index: number;
  submissions: number;
  handleEndQuestion: () => void;
};

export const ManagerQuestion = ({
    question,
    num_players,
    num_questions,
    question_index,
    submissions,
    handleEndQuestion,
}: ManagerQuestionProps) => {
  const [timeLeft, setTimeLeft] = useState(() => {
    const startTime = localStorage.getItem(`time_start`);
    if (!startTime) return question.time_limit; 
    
    const elapsedSeconds = Math.floor((Date.now() - parseInt(startTime)) / 1000);
    const remainingTime = Math.max(0, question.time_limit - elapsedSeconds);
    return remainingTime;
  });

  useEffect(() => {
    if (!localStorage.getItem(`time_start`)) {
      localStorage.setItem(`time_start`, Date.now().toString());
    }
  }, [question.id]);

  const formatTime = (seconds: number): string => {
    if (seconds >= 3600) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
        const secs = (seconds % 60).toString().padStart(2, '0');
        return `${hours}:${minutes}:${secs}`;
    } else if (seconds >= 60) {
        const minutes = Math.floor(seconds / 60).toString().padStart(2, '0');
        const secs = (seconds % 60).toString().padStart(2, '0');
        return `${minutes}:${secs}`;
    } else {
        return `${seconds.toString().padStart(2, '0')}`;
    }
  };

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
          <div className={styles.numbers}>{formatTime(timeLeft)}</div>
        </div>
        <Button onClick={handleEndQuestion}>NEXT</Button>
      </div>
    </div>
  );
};