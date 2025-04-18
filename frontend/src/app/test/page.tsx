'use client';
import styles from '../page.module.css'
import { LoadingState } from '../../../components/loading_state';

export default function Test() {
    return(
        <div className={styles.container}>
           <LoadingState text="Loading..."></LoadingState>
        </div>
    )
}
