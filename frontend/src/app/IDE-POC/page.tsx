'use client'
import React, { useState } from 'react';
import Editor from '@monaco-editor/react';

export default function IDE() {
  const [code, setCode] = useState('');

  return (
    <div>
      <Editor 
      height="90vh" 
      defaultLanguage="javascript" 
      defaultValue="// some comment" 
      onChange={(value) => setCode(value || '')}
      />
    </div>
  );
}
