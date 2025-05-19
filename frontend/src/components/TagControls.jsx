import { useState } from "react";
import axios from "axios";

function TagControls({ onChange }) {
  const [tagName, setTagName] = useState("");
  const [commitId, setCommitId] = useState("");
  const [tags, setTags] = useState({});

  const createTag = async () => {
    if (!tagName || !commitId) return;
    await axios.post("/tag", { name: tagName, commit_id: commitId });
    setTagName("");
    setCommitId("");
    onChange();
  };

  const loadTags = async () => {
    const res = await axios.get("/tags");
    setTags(res.data);
  };

  return (
    <div style={{ marginBottom: "1rem" }}>
      <h3>Tags</h3>
      <input
        type="text"
        placeholder="Tag name"
        value={tagName}
        onChange={(e) => setTagName(e.target.value)}
      />
      <input
        type="text"
        placeholder="Commit ID"
        value={commitId}
        onChange={(e) => setCommitId(e.target.value)}
        style={{ marginLeft: "10px" }}
      />
      <button onClick={createTag}>Create Tag</button>
      <button onClick={loadTags} style={{ marginLeft: "10px" }}>List Tags</button>

      {Object.keys(tags).length > 0 && (
        <ul>
          {Object.entries(tags).map(([tag, id]) => (
            <li key={tag}><strong>{tag}</strong>: {id}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default TagControls;
