'use client';
import styles from '../page.module.css'
import { PlayerQuestion } from '../../../components/player_question';

export default function Test() {
    let question = {
        id: 1,
        description: "Lorem ipsum dolor sit amet, ",
        time_limit: 3610,
        code_starter: "# your code here"
    }
    const handleEndQuestion = () => {

    }
    return(
        <div className={styles.container}>
            <PlayerQuestion question={question} handleSubmitQuestion={handleEndQuestion}></PlayerQuestion>
        </div>
    )
}
