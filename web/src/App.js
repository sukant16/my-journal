import React, { useState, useEffect } from "react";

import Timeline from "./components/Timeline";
import JournalEditor from "./components/Editor";
import Login from './components/Login';
import Logout from './components/Logout';
import API from "./utils/API"

import "./App.css";

const fetchEntries = async (userId) => {
  const res = await API.get("/posts", {
    params: {
      user_id: userId,
    },
  });
  return res.data;
};

const App = () => {
  // const userId = "1";
  // const [entries, setEntries] = useState([]);

  // useEffect(() => {
  //   let mounted = true;
  //   const fetchData = async () => {
  //     const data = await fetchEntries(userId);
  //     if (mounted){
  //       setEntries(data);
  //     }
  //   }
  //   fetchData();
  //   return () => mounted = false;
  // }, []);

  // const handleNewEntry = (newEntry) => {
  //   setEntries([newEntry, ...entries]);
  // };
  return (
    <div className="App">
      <header className="App-header">
        <div>
          <span className="title">My Journal</span>
        </div>
      </header>
      <Login />
      <Logout />
      {/* <JournalEditor onNewEntrySubmit={handleNewEntry} userId={userId} /> */}
      {/* <Timeline entries={entries} /> */}
    </div>
  );
};

export default App;
