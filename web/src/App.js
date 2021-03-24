import React, { useState,  useEffect   } from 'react';
import { EditorState, convertToRaw } from 'draft-js';
import { Editor } from 'react-draft-wysiwyg';
import { convertToHTML } from 'draft-convert';
import axios from 'axios';
import 'react-draft-wysiwyg/dist/react-draft-wysiwyg.css';
import './App.css';

const App = () => {
  const [editorState, setEditorState] = useState(
    () => EditorState.createEmpty(),
  );

  const [convertedContent, setConvertedContent] = useState("");

  const [entriesList, setEntriesList] = useState([]);

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
      "user_id": 2,
    }
    try {
      const res = await axios.post('http://127.0.0.1:5000/v1/posts', data)
      setEntriesList([res.data, ...entriesList]);
    } catch  (e){
      console.log('posting failed', e);
    }    
    event.preventDefault();
  }

  // useEffect(() =>{
  //   const entiresMarkup = entries.map()
  // }, [entries])
  const entries = entriesList.map((item, index) =>
    <li key={item['last_modified']}>
      <h3>{item['last_modified']}</h3>
      <p>{item['post']}</p>
    </li>
  );
  console.log(entriesList);
  return (
    <div className="App">
    <header className="App-header">
      <div>
        <span className="title">My Journal</span>
        <span className="login">Login</span>
      </div>
    </header>
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
    <div>
      { entriesList !== [] ?
      <>
        <h1>Submitted Entries</h1>
        <ul>{entries}</ul>
      </>: null
      }
    </div>
  </div>
  
  )
}
export default App;