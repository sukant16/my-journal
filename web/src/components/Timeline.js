import React, { useEffect, useState } from "react";
import API from "../utils/API";


const Timeline = (props) => {
  
  const [entriesMarkup, setEntriesMarkup] = useState([""]);

  useEffect(() => {
    setEntriesMarkup(entries.map((item) => (
      <li key={item.last_modified}>
        <h4>Entry @{item.creation_date}</h4>
        <p>{item.post}</p>
        <hr />
      </li>
    )));
  }, [props.entries]);
  
  return (
  <>
  {entriesMarkup !== [] ?
    <div>
      <h2>My Timeline</h2>
      {entriesMarkup}
    </div>
    : <h3>We are waiting for your first Journal Entry!</h3>
  }
  </>
  );
};

export default Timeline;
