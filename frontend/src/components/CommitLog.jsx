// src/components/CommitLog.jsx
import { motion } from "framer-motion";

function CommitLog({ log }) {
  return (
    <div className="commit-log">
      <h2>Commit Log</h2>
      <ul>
        {log.map((entry, index) => (
          <motion.li
            key={entry.id}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.05 }}
          >
            <strong>{entry.id}</strong>: {entry.message} ({entry.timestamp})
          </motion.li>
        ))}
      </ul>
    </div>
  );
}

export default CommitLog;
