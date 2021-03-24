import React, { useState, useEffect } from "react";

import Timeline from "./components/Timeline";
import Editor from "./components/Editor";

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
  const userId = 1;
  const [entries, setEntries] = useState([""]);

  useEffect(() => {
    setEntries(fetchEntries(1));
  }, []);

  const handleNewEntry = (newEntry) => {
    setEntries([newEntry, ...entries]);
  };
  return (
    <div className="App">
      <header className="App-header">
        <div>
          <span className="title">My Journal</span>
          <span className="login">Login</span>
        </div>
      </header>
      <Editor onNewEntrySubmit={handleNewEntry} userId={userId} />
      <Timeline entries={entries} />
    </div>
  );
};
export default App;
