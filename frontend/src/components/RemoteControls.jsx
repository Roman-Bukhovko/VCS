import { useState } from "react";
import axios from "axios";

function RemoteControls({ onChange }) {
  const [remotePath, setRemotePath] = useState("");

  const push = async () => {
    if (!remotePath.trim()) return;
    await axios.post("/push", { remote_path: remotePath });
  };

  const pull = async () => {
    if (!remotePath.trim()) return;
    await axios.post("/pull", { remote_path: remotePath });
    onChange();
  };

  return (
    <div style={{ marginBottom: "1rem" }}>
      <h3>Remote Sync</h3>
      <input
        type="text"
        placeholder="Remote folder path"
        value={remotePath}
        onChange={(e) => setRemotePath(e.target.value)}
      />
      <button onClick={push}>Push</button>
      <button onClick={pull} style={{ marginLeft: "10px" }}>Pull</button>
    </div>
  );
}

export default RemoteControls;
