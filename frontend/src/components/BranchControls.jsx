import { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";

function BranchControls({ onChange }) {
  const [newBranch, setNewBranch] = useState("");
  const [switchBranch, setSwitchBranch] = useState("");

  const createBranch = async () => {
    if (!newBranch.trim()) return;
    await axios.post("/branch", { name: newBranch });
    setNewBranch("");
    onChange();
  };

  const checkoutBranch = async () => {
    if (!switchBranch.trim()) return;
    await axios.post("/checkout-branch", { name: switchBranch });
    setSwitchBranch("");
    onChange();
  };

  return (
    <motion.div
      className="controls"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <h3>Branch Controls</h3>
      <input
        type="text"
        placeholder="New branch name"
        value={newBranch}
        onChange={e => setNewBranch(e.target.value)}
      />
      <button onClick={createBranch}>Create Branch</button>

      <input
        type="text"
        placeholder="Switch to branch"
        value={switchBranch}
        onChange={e => setSwitchBranch(e.target.value)}
        style={{ marginLeft: "10px" }}
      />
      <button onClick={checkoutBranch}>Checkout</button>
    </motion.div>
  );
}

export default BranchControls;
