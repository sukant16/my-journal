import React, { useEffect, useState } from "react";
import API from "../utils/API";

const fetchEntries = async (userId) => {
  const res = await API.get("/posts", {
    params: {
      user_id: userId,
    }
  });
  return res.data;
};

const Timeline = (props) => {
  const [entries, setEntries] = useState([""]);
  const [entriesMarkup, setEntriesMarkup] = useState([""]);

  useEffect(() => {
    setEntries(fetchEntries(props.userId));
  }, [props.userId]);

  useEffect(() => {
    setEntries([props.latestEntry, ...entries]);
  }, [props.latestEntry]);

  useEffect(() => {
    setEntriesMarkup(entries.map((item) => (
      <li key={item.last_modified}>
        <h4>Entry @{item.creation_date}</h4>
        <p>{item.post}</p>
        <hr />
      </li>
    )));
  }, [entries]);
  

  
  return (
    <div>
      <h2>My Timeline</h2>
      {entriesMarkup}
    </div>
  );
};

export default Timeline;
