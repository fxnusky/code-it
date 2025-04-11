'use client';
import styles from '../page.module.css'
import { ManagerQuestion } from '../../../components/manager_question';

export default function Test() {
    let question = {
        id: 1,
        description: "Lorem ipsum dolor sit amet, ",
        time_limit: 3610
    }
    const handleEndQuestion = () => {

    }
    return(
        <div className={styles.container}>
            <ManagerQuestion question={question} num_players={5} num_questions={5} question_index={3} submissions={3} handleEndQuestion={handleEndQuestion}></ManagerQuestion>
        </div>
    )
}
