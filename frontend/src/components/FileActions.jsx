import { useState } from "react";
import axios from "axios";

function FileActions({ onChange }) {
  const [filename, setFilename] = useState("");
  const [commitId, setCommitId] = useState("");
  const [diffOutput, setDiffOutput] = useState("");

  const addFile = async () => {
    if (!filename.trim()) return;
    await axios.post("/add", { filename });
    onChange();
  };

  const diffFile = async () => {
    if (!filename.trim()) return;
    const res = await axios.post("/diff", { file: filename });
    setDiffOutput(res.data.diff || "No differences.");
  };

  const restoreFile = async () => {
    if (!filename.trim() || !commitId.trim()) return;
    await axios.post("/restore", { filename, commit_id: commitId });
    onChange();
  };

  return (
    <div style={{ marginBottom: "1rem" }}>
      <h3>File Actions</h3>
      <input
        type="text"
        placeholder="Filename"
        value={filename}
        onChange={(e) => setFilename(e.target.value)}
      />
      <button onClick={addFile}>Add</button>
      <button onClick={diffFile}>Diff</button>

      <input
        type="text"
        placeholder="Commit ID (for restore)"
        value={commitId}
        onChange={(e) => setCommitId(e.target.value)}
        style={{ marginLeft: "10px" }}
      />
      <button onClick={restoreFile}>Restore</button>

      {diffOutput && (
        <pre style={{ marginTop: "10px", background: "#f0f0f0", padding: "10px" }}>
          {diffOutput}
        </pre>
      )}
    </div>
  );
}

export default FileActions;
