import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";

const Timeline = (props) => {
  
  const [entriesMarkup, setEntriesMarkup] = useState([""]);

  useEffect(() => {
    console.log(props.entries);
    const entriesLi = props.entries.map((item) => (
      <li key={item.last_modified}>
        <h4>Entry @{item.creation_date}</h4>
        <p>{item.post}</p>
        <hr />
      </li>
    ));
    setEntriesMarkup(entriesLi);
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


  Timeline.propTypes = {
    entries: PropTypes.array,
  }

export default Timeline;
