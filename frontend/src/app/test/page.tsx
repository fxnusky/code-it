'use client';
import styles from '../page.module.css'
import { PlayerResults } from '../../../components/player_results';

export default function Test() {
    let func = () => {

    }
    let results = {total_points: 0, question_points: 0, test_case_executions: [{case_id: 1, correct: false}, {case_id: 2, correct: false}, {case_id: 3, correct: false}]}
    
    return(
        <PlayerResults nickname='fanny' results={results}></PlayerResults>
    )
}
