import { useEffect, useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import CommitForm from "./components/CommitForm";
import CommitLog from "./components/CommitLog";
import StatusBlock from "./components/StatusBlock";
import BranchControls from "./components/BranchControls";
import StashControls from "./components/StashControls";
import MergeRevertControls from "./components/MergeRevertControls";
import FileActions from "./components/FileActions";
import TagControls from "./components/TagControls";
import RemoteControls from "./components/RemoteControls";
import "./App.css";

function App() {
  const [log, setLog] = useState([]);
  const [status, setStatus] = useState({});
  const [branch, setBranch] = useState("");

  const refresh = () => {
    axios.get("/log").then(res => setLog(res.data));
    axios.get("/status").then(res => setStatus(res.data));
    axios.get("/current-branch").then(res => setBranch(res.data.branch));
  };

  useEffect(() => {
    refresh();
  }, []);

  return (
    <motion.div
      className="container"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h1>VCS</h1>
      <p>📍 Current branch: <strong>{branch}</strong></p>

      <CommitForm onCommit={refresh} />
      <BranchControls onChange={refresh} />
      <StashControls onChange={refresh} />
      <MergeRevertControls onChange={refresh} />
      <FileActions onChange={refresh} />
      <TagControls onChange={refresh} />
      <RemoteControls onChange={refresh} />
      <StatusBlock status={status} />
      <CommitLog log={log} />
    </motion.div>
  );
}

export default App;
