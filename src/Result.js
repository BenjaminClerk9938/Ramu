import React from "react";

function Result({ downloadPath }) {
  return (
    <div>
      <h2>Processing Complete</h2>
      <a href={downloadPath} download>
        Download Combined Excel File
      </a>
    </div>
  );
}

export default Result;
