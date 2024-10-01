import React, { useState } from "react";
import axios from "axios";
import { SERVER_URL } from "./constant";

function FileUpload({ onSuccess }) {
  const [secFile, setSecFile] = useState(null);
  const [portfolioFile, setPortfolioFile] = useState(null);

  const handleFileChange = (e, setFile) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = () => {
    const formData = new FormData();
    formData.append("secFile", secFile);
    formData.append("portfolioFile", portfolioFile);

    axios
      .post(`${SERVER_URL}/api/upload`, formData)
      .then((response) => {
        onSuccess(response.data.downloadPath);
      })
      .catch((error) => {
        console.error("Error uploading files:", error);
      });
  };

  return (
    <div>
      <input type="file" onChange={(e) => handleFileChange(e, setSecFile)} />
      <input
        type="file"
        onChange={(e) => handleFileChange(e, setPortfolioFile)}
      />
      <button onClick={handleUpload}>Upload and Process</button>
    </div>
  );
}

export default FileUpload;
