import axios from "axios";
import { motion } from "framer-motion";

function StashControls({ onChange }) {
  const stash = async () => {
    await axios.post("/stash");
    onChange();
  };

  const pop = async () => {
    await axios.post("/stash/pop");
    onChange();
  };

  return (
    <motion.div
      className="controls"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.1, duration: 0.4 }}
    >
      <h3>Stash</h3>
      <button onClick={stash}>Stash Changes</button>
      <button onClick={pop} style={{ marginLeft: "10px" }}>Pop Stash</button>
    </motion.div>
  );
}

export default StashControls;
