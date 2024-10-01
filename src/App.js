import React, { useState } from "react";
import FileUpload from "./FileUpload";
import Result from "./Result";

function App() {
  const [downloadPath, setDownloadPath] = useState(null);

  const handleUploadSuccess = (path) => {
    setDownloadPath(path);
  };

  return (
    <div className="App">
      <h1>Excel Joiner</h1>
      <FileUpload onSuccess={handleUploadSuccess} />
      {downloadPath && <Result downloadPath={downloadPath} />}
    </div>
  );
}

export default App;
