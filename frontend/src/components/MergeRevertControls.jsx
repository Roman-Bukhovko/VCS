import { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";

function MergeRevertControls({ onChange }) {
  const [mergeBranch, setMergeBranch] = useState("");
  const [revertId, setRevertId] = useState("");

  const merge = async () => {
    if (!mergeBranch.trim()) return;
    await axios.post("/merge", { branch: mergeBranch });
    setMergeBranch("");
    onChange();
  };

  const revert = async () => {
    if (!revertId.trim()) return;
    await axios.post("/revert", { commit_id: revertId });
    setRevertId("");
    onChange();
  };

  return (
    <motion.div
      className="controls"
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.4 }}
    >
      <h3>Merge & Revert</h3>
      <input
        type="text"
        placeholder="Merge branch"
        value={mergeBranch}
        onChange={e => setMergeBranch(e.target.value)}
      />
      <button onClick={merge}>Merge</button>

      <input
        type="text"
        placeholder="Revert commit ID"
        value={revertId}
        onChange={e => setRevertId(e.target.value)}
        style={{ marginLeft: "10px" }}
      />
      <button onClick={revert}>Revert</button>
    </motion.div>
  );
}

export default MergeRevertControls;
