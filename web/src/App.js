import React, { useState } from 'react';
import { EditorState, convertToRaw } from 'draft-js';
import { Editor } from 'react-draft-wysiwyg';
import { convertToHTML } from 'draft-convert';
import 'react-draft-wysiwyg/dist/react-draft-wysiwyg.css';
import './App.css';

const App = () => {
  const [editorState, setEditorState] = useState(
    () => EditorState.createEmpty(),
  );

  const [convertedContent, setConvertedContent] = useState("");

  const handleEditorChange = (state) => {
    setEditorState(state);
    console.log(convertToRaw(editorState.getCurrentContent()));
    convertContentToHTML();
  }
  
  const convertContentToHTML = () => {
    let currentContentAsHTML = convertToHTML(editorState.getCurrentContent());
    console.log(currentContentAsHTML);
    setConvertedContent(currentContentAsHTML);
  }

  return (
    <div className="App">
    <header className="App-header">
      Rich Text Editor Example
    </header>
    <Editor
      editorState={editorState}
      onEditorStateChange={handleEditorChange}
      wrapperClassName="wrapper-class"
      editorClassName="editor-class"
      toolbarClassName="toolbar-class"
    />
  </div>
  )
}
export default App;