'use client';
import styles from '../src/app/page.module.css'; 
import PacmanLoader from 'react-spinners/PacmanLoader'

type LoadingStateProps = {
  text: string;
};

export const LoadingState = ({
    text
}: LoadingStateProps) => {
  
  return (
    <div className={styles.container}>
         <PacmanLoader color="#7aacd5" size={25} margin="1rem"/>
         <p className={styles.description}>{text}</p>
    </div>
  );
};