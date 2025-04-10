'use client';
import styles from './question.module.css'; 
import { Question } from '../services/ws_connection.service';
import Editor from '@monaco-editor/react';
import { Button } from "@/components/ui/button"
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable"


type PlayerQuestionProps = {
  question: Question;
  num_questions: number;
  question_index: number;
};

export const PlayerQuestion = ({
    question,
    num_questions,
    question_index,
}: PlayerQuestionProps) => {

  function handleEditorChange(value: string | undefined) {
    console.log('here is the current model value:', value);
  }
  return (
    <div className={styles.question_container}>
      <ResizablePanelGroup direction="horizontal">
        <ResizablePanel defaultSize={30}>
        <div className={styles.question_section}>
          <h1 className={styles.question_title}>QUESTION {question_index + 1}/{num_questions}</h1>
          <p className={styles.question_description}>{question.description}</p>
        </div>
        </ResizablePanel>
        <ResizableHandle />
        <ResizablePanel defaultSize={70}>
          <ResizablePanelGroup direction="vertical">
            <ResizablePanel defaultSize={60}>
            <div className={styles.editor_container}>
              <Editor
                height="100vh"
                defaultLanguage="javascript"
                defaultValue="// some comment"
                onChange={handleEditorChange}
              />
            </div>
            </ResizablePanel>
            <ResizableHandle />
            <ResizablePanel defaultSize={40}>
            <div className={styles.button_bar}>
              <Button variant="secondary" className={styles.margin_inline}>Run</Button>
              <Button>Submit</Button>
            </div>
            
            <div className={styles.terminal}>
              {/* Terminal output will go here */}
            </div>
            </ResizablePanel>
          </ResizablePanelGroup>
        </ResizablePanel>
      </ResizablePanelGroup> 
    </div>
  );
};