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
import ExecuteService from '../services/execute.service';


type PlayerQuestionProps = {
  token: string;
  question: Question;
  handleSubmitQuestion: (code: string) => void;
};

export const PlayerQuestion = ({
    token,
    question,
    handleSubmitQuestion
}: PlayerQuestionProps) => {
  const [code, setCode] = useState('');
  const [terminalText, setTerminalText] = useState('');


  useEffect(() => {
    if (question?.code_starter) {
        const formattedCode = question.code_starter.replace(/\\n/g, '\n');
        setCode(formattedCode);
    }
  }, [question]);

  useEffect(() => {
    const roomData = JSON.parse(localStorage.getItem(`room-${token}`) || '{}');
    
    if (roomData[`code-${question.id}`]) {
      setCode(roomData[`code-${question.id}`]);
    }
  }, [question.id, token]);

  const handleEditorChange = (value: string | undefined) => {
      if (value) {
          setCode(value);
          const roomData = JSON.parse(localStorage.getItem(`room-${token}`) || '{}');
          roomData[`code-${question.id}`] = value;
          localStorage.setItem(`room-${token}`, JSON.stringify(roomData));
      }
  };

  const handleSubmit = () => {
      const roomData = JSON.parse(localStorage.getItem(`room-${token}`) || '{}');
      delete roomData[`code-${question.id}`];
      localStorage.setItem(`room-${token}`, JSON.stringify(roomData));
      
      handleSubmitQuestion(code);
  };

  async function runCode() {
    let result = await ExecuteService.runCode({code});
    if (result && result.data.return_code === 0){
      const formattedOutput = result.data.output.replace(/\\n/g, '\n');
      setTerminalText(formattedOutput)
    }
    else if (result){
      const formattedError = result.data.error.replace(/\\n/g, '\n');
      setTerminalText(formattedError)
    }
    else{
      setTerminalText("Error")
    }
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
              <Button variant="secondary" className={styles.margin_inline} onClick={runCode}>Run</Button>
              <Button onClick={handleSubmit}>Submit</Button>
            </div>
            
            <div className={styles.terminal}>
              {terminalText}
            </div>
            </ResizablePanel>
          </ResizablePanelGroup>
        </ResizablePanel>
      </ResizablePanelGroup> 
    </div>
  );
};