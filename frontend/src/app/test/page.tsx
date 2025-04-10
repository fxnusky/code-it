'use client';
import styles from '../page.module.css'
import { PlayerQuestion } from '../../../components/player_question';

export default function Test() {
    let question = {
        id: 1,
        description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac metus elit. Donec est neque, tristique sit amet hendrerit vel, fringilla in turpis. Suspendisse venenatis ullamcorper vehicula. Sed vitae aliquet elit, eu finibus quam. Donec venenatis, enim quis consectetur gravida, metus lacus lacinia mi, placerat gravida nibh ipsum et urna. Nam sed tincidunt ligula. Etiam aliquam volutpat velit, non aliquet felis tristique consectetur. Nulla varius vitae dolor ut volutpat. Integer ornare risus ut neque rhoncus, sed venenatis enim consequat./nFusce a dolor vel velit dapibus porttitor vitae sed tellus. Aliquam aliquam, lectus et finibus tempus, velit ipsum pulvinar dolor, ut mattis ligula nisi id nulla. Etiam rhoncus risus et ex consectetur tempus. In hac habitasse platea dictumst. Etiam non ipsum dui. Integer sit amet libero enim. Etiam in posuere mi, id dictum dolor. Proin posuere ipsum a viverra elementum. Nam laoreet augue auctor, hendrerit nisl non, lobortis libero. Integer ultricies velit quis nisl accumsan, id eleifend massa ullamcorper.",
        time_limit: 15
    }
    const handleEndQuestion = () => {

    }
    return(
        <div className={styles.container}>
            <PlayerQuestion question={question}num_questions={2} question_index={1}></PlayerQuestion>
        </div>
    )
}
