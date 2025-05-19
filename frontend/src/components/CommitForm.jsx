// src/components/CommitForm.jsx
import { useState } from "react";
import axios from "axios";

function CommitForm({ onCommit }) {
  const [message, setMessage] = useState("");

  const handleSubmit = async () => {
    if (!message.trim()) return alert("Enter a commit message.");
    await axios.post("/commit", { message });
    setMessage("");
    onCommit(); // refresh status + log
  };

  return (
    <div style={{ marginBottom: "1rem" }}>
      <input
        type="text"
        placeholder="Commit message"
        value={message}
        onChange={e => setMessage(e.target.value)}
      />
      <button onClick={handleSubmit}>Commit</button>
    </div>
  );
}

export default CommitForm;
