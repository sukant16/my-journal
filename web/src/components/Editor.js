import React, { useState } from 'react';
import { EditorState } from 'draft-js';
import { Editor } from 'react-draft-wysiwyg';
import { convertToHTML } from 'draft-convert';
import PropTypes from "prop-types";

import API from "../utils/API"

import 'react-draft-wysiwyg/dist/react-draft-wysiwyg.css';

const JournalEditor = (props) => {
  const [editorState, setEditorState] = useState(
    () => EditorState.createEmpty(),
  );
  console.log(editorState);
  const [convertedContent, setConvertedContent] = useState("");

  const handleEditorChange = (state) => {
    setEditorState(state);
    // console.log(convertToRaw(editorState.getCurrentContent()));
    convertContentToHTML();
  }
  
  const convertContentToHTML = () => {
    let currentContentAsHTML = convertToHTML(editorState.getCurrentContent());  
    setConvertedContent(currentContentAsHTML);
  }
  
  const handleSubmit = async (event) => {
    const data = {
      "post" : JSON.stringify(convertedContent),
      "user_id": props.userId,
    }
    try {
      const res = await API.post('posts', data)
      props.onNewEntrySubmit(res.data);
      // setEditorState({});
    } catch  (e){
      console.log('creating new post failed:', e);
    }    
    event.preventDefault();
  }

  return (
    <div className="editor">
    <Editor
      editorState={editorState}
      onEditorStateChange={handleEditorChange}
      wrapperClassName="wrapper-class"
      editorClassName="editor-class"
      toolbarClassName="toolbar-class"
    />
    <div>
      <button onClick={handleSubmit}>Submit</button>
    </div>
  </div>
  
  )
}


JournalEditor.propTypes = {
  userId: PropTypes.string,
  onNewEntrySubmit: PropTypes.func,
}

export default JournalEditor;