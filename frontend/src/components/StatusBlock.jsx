// src/components/StatusBlock.jsx
function StatusBlock({ status }) {
  return (
    <div className="status-section">
      <h2>Status</h2>
      <ul>
        <li><strong>Staged:</strong> {status.staged?.join(', ') || "None"}</li>
        <li><strong>Modified:</strong> {status.modified?.join(', ') || "None"}</li>
        <li><strong>Untracked:</strong> {status.untracked?.join(', ') || "None"}</li>
      </ul>
    </div>
  );
}

export default StatusBlock;
