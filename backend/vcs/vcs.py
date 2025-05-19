import os
import shutil
import hashlib
import json
from datetime import datetime
from .config import *
import difflib

def init_repo():
    """Initialize a new repository."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    os.makedirs(VCS_DIR, exist_ok=True)
    os.makedirs(COMMITS_DIR, exist_ok=True)
    os.makedirs(INDEX_DIR, exist_ok=True)
    os.makedirs(BRANCHES_DIR, exist_ok=True)
    os.makedirs(STASH_DIR, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)
    if not os.path.exists(TAGS_FILE):
        with open(TAGS_FILE, "w") as f:
            json.dump({}, f)
    if not os.path.exists(HEAD_FILE):
        with open(HEAD_FILE, "w") as f:
            f.write("main")
    main_branch = os.path.join(BRANCHES_DIR, "main.json")
    if not os.path.exists(main_branch):
        with open(main_branch, "w") as f:
            json.dump([], f)

def add_file(filename):
    """Add a file to the staging area."""
    src = os.path.join(WORKSPACE_DIR, filename)
    dst = os.path.join(INDEX_DIR, filename)
    if os.path.exists(src):
        shutil.copy2(src, dst)

def commit(message):
    """Commit staged files with a message."""
    if not os.listdir(INDEX_DIR):
        return {"success": False, "error": "Nothing to commit."}

    timestamp = datetime.utcnow().isoformat()
    commit_id = hashlib.sha1(f"{timestamp}{message}".encode()).hexdigest()[:6]
    commit_path = os.path.join(COMMITS_DIR, commit_id)
    os.makedirs(commit_path)

    for fname in os.listdir(INDEX_DIR):
        shutil.copy2(os.path.join(INDEX_DIR, fname), os.path.join(commit_path, fname))

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            log = json.load(f)
    else:
        log = []

    log.append({"id": commit_id, "timestamp": timestamp, "message": message})
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

    branch = get_current_branch()
    branch_file = os.path.join(BRANCHES_DIR, f"{branch}.json")
    if os.path.exists(branch_file):
        with open(branch_file, "r") as f:
            branch_log = json.load(f)
    else:
        branch_log = []
    branch_log.append(commit_id)
    with open(branch_file, "w") as f:
        json.dump(branch_log, f, indent=2)

    shutil.rmtree(INDEX_DIR)
    os.makedirs(INDEX_DIR)

    return {
        "success": True,
        "commit_id": commit_id,
        "timestamp": timestamp,
        "message": message
    }

def log_commits():
    """Return the commit log."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []

def hash_file(path):
    with open(path, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()

def status():
    """Return the status of files."""
    workspace_files = set(os.listdir(WORKSPACE_DIR)) if os.path.exists(WORKSPACE_DIR) else set()
    index_files = set(os.listdir(INDEX_DIR)) if os.path.exists(INDEX_DIR) else set()

    return {
        "staged": list(index_files),
        "untracked": list(workspace_files - index_files),
        "modified": list(workspace_files & index_files)
    }

def checkout(commit_id):
    """Replace workspace files with files from a specified commit."""
    commit_path = os.path.join(COMMITS_DIR, commit_id)
    if not os.path.exists(commit_path):
        return {"success": False, "error": "Commit not found"}

    if workspace_has_changes():
        return {"success": False, "error": "Uncommitted changes exist"}

    for f in os.listdir(WORKSPACE_DIR):
        os.remove(os.path.join(WORKSPACE_DIR, f))

    for f in os.listdir(commit_path):
        shutil.copy2(os.path.join(commit_path, f), os.path.join(WORKSPACE_DIR, f))

    return {"success": True, "commit_id": commit_id}

def diff(file):
    """Return the diff of a file between workspace and staging area."""
    workspace_file = os.path.join(WORKSPACE_DIR, file)
    index_file = os.path.join(INDEX_DIR, file)
    if not os.path.exists(workspace_file) or not os.path.exists(index_file):
        return ""
    with open(workspace_file, "r") as f1, open(index_file, "r") as f2:
        workspace_lines = f1.readlines()
        index_lines = f2.readlines()
    diff_lines = []
    for line in workspace_lines:
        if line not in index_lines:
            diff_lines.append(f"+ {line}")
    for line in index_lines:
        if line not in workspace_lines:
            diff_lines.append(f"- {line}")
    return "".join(diff_lines)

def restore(commit_id, filename):
    """Restore a file from a specific commit."""
    commit_path = os.path.join(COMMITS_DIR, commit_id)
    file_path = os.path.join(commit_path, filename)
    if not os.path.exists(file_path):
        return {"success": False, "error": "File not found in commit."}
    shutil.copy2(file_path, os.path.join(WORKSPACE_DIR, filename))
    return {"success": True, "file": filename}

def history(filename):
    """Return the history of a file."""
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        log = json.load(f)
    history_list = []
    for entry in log:
        commit_id = entry["id"]
        commit_path = os.path.join(COMMITS_DIR, commit_id)
        if filename in os.listdir(commit_path):
            history_list.append(entry)
    return history_list

def get_current_branch():
    """Get the name of the current branch."""
    if os.path.exists(HEAD_FILE):
        with open(HEAD_FILE, "r") as f:
            return f.read().strip()
    return "main"

def branch(name):
    """Create a new branch."""
    branch_file = os.path.join(BRANCHES_DIR, f"{name}.json")
    if os.path.exists(branch_file):
        return {"success": False, "error": "Branch already exists."}
    current_branch = get_current_branch()
    current_branch_file = os.path.join(BRANCHES_DIR, f"{current_branch}.json")
    if os.path.exists(current_branch_file):
        with open(current_branch_file, "r") as f:
            commits = json.load(f)
    else:
        commits = []
    with open(branch_file, "w") as f:
        json.dump(commits, f, indent=2)
    return {"success": True, "branch": name}

def checkout_branch(name):
    """Switch to a different branch."""
    branch_file = os.path.join(BRANCHES_DIR, f"{name}.json")
    if not os.path.exists(branch_file):
        return {"success": False, "error": "Branch does not exist."}
    with open(HEAD_FILE, "w") as f:
        f.write(name)
    return {"success": True, "branch": name}

def current_branch():
    """Return the current branch name."""
    return get_current_branch()

def rm(filename):
    """Remove a file from the workspace."""
    file_path = os.path.join(WORKSPACE_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return {"success": True, "file": filename}

def reset():
    """Reset the staging area."""
    shutil.rmtree(INDEX_DIR)
    os.makedirs(INDEX_DIR)
    return {"success": True}

def commit_all(message):
    """Stage all files and commit."""
    for fname in os.listdir(WORKSPACE_DIR):
        add_file(fname)
    return commit(message)

def workspace_has_changes():
    """Check if the current workspace has uncommitted changes."""
    if not os.path.exists(LOG_FILE):
        return False

    with open(LOG_FILE) as f:
        log = json.load(f)
    if not log:
        return False

    last_commit_id = log[-1]["id"]
    last_commit_path = os.path.join(COMMITS_DIR, last_commit_id)

    workspace_files = set(os.listdir(WORKSPACE_DIR))
    committed_files = set(os.listdir(last_commit_path))

    for f in workspace_files:
        workspace_file = os.path.join(WORKSPACE_DIR, f)
        committed_file = os.path.join(last_commit_path, f)
        if f not in committed_files or not os.path.exists(committed_file):
            return True
        if hash_file(workspace_file) != hash_file(committed_file):
            return True
    return False

def diff_commits(commit1, commit2):
    """Return the diff between two commits."""
    commit1_path = os.path.join(COMMITS_DIR, commit1)
    commit2_path = os.path.join(COMMITS_DIR, commit2)
    files1 = set(os.listdir(commit1_path))
    files2 = set(os.listdir(commit2_path))
    all_files = files1.union(files2)
    diffs = {}
    for file in all_files:
        file1 = os.path.join(commit1_path, file)
        file2 = os.path.join(commit2_path, file)
        lines1 = open(file1, "r").readlines() if os.path.exists(file1) else []
        lines2 = open(file2, "r").readlines() if os.path.exists(file2) else []
        diff_lines = []
        for line in lines1:
            if line not in lines2:
                diff_lines.append(f"- {line}")
        for line in lines2:
            if line not in lines1:
                diff_lines.append(f"+ {line}")
        diffs[file] = "".join(diff_lines)
    return diffs

def log_branch(branch_name):
    """Return the commit log for a specific branch."""
    branch_file = os.path.join(BRANCHES_DIR, f"{branch_name}.json")
    if os.path.exists(branch_file):
        with open(branch_file, "r") as f:
            commit_ids = json.load(f)
        with open(LOG_FILE, "r") as f:
            all_logs = json.load(f)
        return [entry for entry in all_logs if entry["id"] in commit_ids]
    return []

def push(remote_path):
    """Push the local .myvcs metadata to a remote repository location."""
    try:
        remote_vcs = os.path.join(remote_path, VCS_DIR)
        shutil.copytree(VCS_DIR, remote_vcs, dirs_exist_ok=True)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

def pull(remote_path):
    """Pull .vcs metadata from a remote directory into the current repository."""
    try:
        remote_vcs = os.path.join(remote_path, VCS_DIR)
        shutil.copytree(remote_vcs, VCS_DIR, dirs_exist_ok=True)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

def merge(branch_name):
    """Merge the latest commit from the specified branch into the current index."""
    target_file = os.path.join(BRANCHES_DIR, f"{branch_name}.json")
    if not os.path.exists(target_file):
        return {"success": False, "error": "Branch not found"}

    with open(target_file) as f:
        commits = json.load(f)
    if not commits:
        return {"success": False, "error": "Branch has no commits"}

    latest_commit = commits[-1]
    commit_path = os.path.join(COMMITS_DIR, latest_commit)

    for fname in os.listdir(commit_path):
        shutil.copy2(os.path.join(commit_path, fname), os.path.join(INDEX_DIR, fname))

    return {"success": True, "merged_from": branch_name}

def revert(commit_id):
    """Revert the changes introduced by a specific commit."""
    commit_path = os.path.join(COMMITS_DIR, commit_id)
    if not os.path.exists(commit_path):
        return {"success": False, "error": "Commit not found"}

    for fname in os.listdir(commit_path):
        committed_file = os.path.join(commit_path, fname)
        workspace_file = os.path.join(WORKSPACE_DIR, fname)
        if os.path.exists(workspace_file):
            os.remove(workspace_file)
        shutil.copy2(committed_file, workspace_file)

    return commit(f"Revert commit {commit_id}")

def stash():
    """Save the current workspace as a stash and clear the workspace."""
    os.makedirs(STASH_DIR, exist_ok=True)
    i = 0
    while os.path.exists(os.path.join(STASH_DIR, f"stash{i}")):
        i += 1
    stash_path = os.path.join(STASH_DIR, f"stash{i}")
    os.makedirs(stash_path)

    for f in os.listdir(WORKSPACE_DIR):
        shutil.copy2(os.path.join(WORKSPACE_DIR, f), os.path.join(stash_path, f))
        os.remove(os.path.join(WORKSPACE_DIR, f))

    return {"success": True, "stash": f"stash{i}"}

def stash_pop():
    """Restore the most recent stashed changes into the workspace."""
    stashes = sorted(os.listdir(STASH_DIR))
    if not stashes:
        return {"success": False, "error": "No stash to pop"}

    latest = os.path.join(STASH_DIR, stashes[-1])

    for f in os.listdir(latest):
        shutil.copy2(os.path.join(latest, f), os.path.join(WORKSPACE_DIR, f))

    shutil.rmtree(latest)
    return {"success": True, "restored": stashes[-1]}

def tag(name, commit_id):
    """Create a tag for a specific commit."""
    if not os.path.exists(os.path.join(COMMITS_DIR, commit_id)):
        return {"success": False, "error": "Commit does not exist."}
    if os.path.exists(TAGS_FILE):
        with open(TAGS_FILE, "r") as f:
            tags = json.load(f)
    else:
        tags = {}
    tags[name] = commit_id
    with open(TAGS_FILE, "w") as f:
        json.dump(tags, f, indent=2)
    return {"success": True, "tag": name, "commit": commit_id}

def list_tags():
    """List all tags."""
    if os.path.exists(TAGS_FILE):
        with open(TAGS_FILE, "r") as f:
            return json.load(f)
    return {}

def help():
    """Print a list of all supported commands with descriptions."""
    print("""
    VCS - Custom Version Control System

    Available Commands:
    init                      Initialize a new repository
    add <file>                Stage a file
    commit "<msg>"            Commit staged files
    commit -a "<msg>"         Auto-stage all and commit
    log                       Show commit history
    log --branch <name>       Show branch commit history
    status                    Show file status
    diff <file>               Diff file vs index
    diff <commit1> <commit2>  Diff between two commits
    restore <file> OR <commit> <file>   Restore file
    history <file>            Show file commit history
    branch <name>             Create a branch
    checkout-branch <name>    Switch branch
    current-branch            Show current branch
    checkout <commit_id>      Load commit into workspace
    rm <file>                 Remove from workspace
    reset                     Clear staging area
    tag <name> <commit>       Tag a commit
    tags                      List tags
    stash                     Save workspace changes
    stash pop                 Restore last stash
    revert <commit>           Undo commit
    merge <branch>            Merge branch
    push <remote_path>        Sync to remote
    pull <remote_path>        Sync from remote
    """)