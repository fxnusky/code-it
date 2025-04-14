'use client';
import styles from './question.module.css'; 
import { Question } from '../services/ws_connection.service';
import Editor from '@monaco-editor/react';
import { Button } from "@/components/ui/button";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";
import { useState, useEffect } from 'react';


type PlayerQuestionProps = {
  question: Question;
  handleSubmitQuestion: () => void;
};

export const PlayerQuestion = ({
    question,
    handleSubmitQuestion
}: PlayerQuestionProps) => {
  const [code, setCode] = useState('');

  useEffect(() => {
    if (question?.code_starter) {
        const formattedCode = question.code_starter.replace(/\\n/g, '\n');
        setCode(formattedCode);
    }
  }, [question]);

  useEffect(() => {
    const savedCode = localStorage.getItem(`code-${question.id}`);
    if (savedCode) {
      setCode(savedCode)
    };
  }, [question.id]);
  
  const handleEditorChange = (value: string | undefined) => {
    if (value) {
      setCode(value);
      localStorage.setItem(`code-${question.id}`, value); 
    }
  };
  
  const handleSubmit = () => {
    localStorage.removeItem(`code-${question.id}`); 
    handleSubmitQuestion();
  };

  return (
    <div className={styles.question_container}>
      <ResizablePanelGroup direction="horizontal">
        <ResizablePanel defaultSize={30}>
        <div className={styles.question_section}>
          <h1 className={styles.question_title}>Description:</h1>
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
                defaultLanguage="python"
                onChange={handleEditorChange}
                value={code}
                options={{
                    minimap: { enabled: false },
                    fontSize: 14,
                    wordWrap: 'on',
                }}
              />
            </div>
            </ResizablePanel>
            <ResizableHandle />
            <ResizablePanel defaultSize={40}>
            <div className={styles.button_bar}>
              <Button variant="secondary" className={styles.margin_inline}>Run</Button>
              <Button onClick={handleSubmit}>Submit</Button>
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