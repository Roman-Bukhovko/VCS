import os
import shutil
import hashlib
import json
from datetime import datetime
from vcs.org_config import *
import difflib

def init_repo():
    if os.path.exists(VCS_DIR):
        print(".vcs already exists")
        return
    
    os.makedirs(INDEX_DIR)
    os.makedirs(COMMITS_DIR)
    with open(LOG_FILE, "w") as f:
        f.write("[]")
    print("INITIALIZED: empty repo in .vcs")

def add_file(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return
    
    os.makedirs(INDEX_DIR, exist_ok=True)
    shutil.copy2(filename, os.path.join(INDEX_DIR, os.path.basename(filename)))
    print(f"STAGED: {filename}")

def commit(message):
    if not os.path.exists(INDEX_DIR) or not os.listdir(INDEX_DIR):
        print("Nothing to commit.")
        return

    with open(LOG_FILE, "r") as f:
        log = json.load(f)

    timestamp = datetime.utcnow().isoformat()
    commit_id = hashlib.sha1(f"{timestamp}{message}".encode()).hexdigest()[:6]
    commit_path = os.path.join(COMMITS_DIR, commit_id)
    os.makedirs(commit_path)

    for filename in os.listdir(INDEX_DIR):
        shutil.copy2(os.path.join(INDEX_DIR, filename), os.path.join(commit_path, filename))

    log.append({"id": commit_id, "message": message, "timestamp": timestamp})
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

    branch = get_current_branch()
    branch_path = os.path.join(BRANCHES_DIR, f"{branch}.json")

    if os.path.exists(branch_path):
        with open(branch_path, "r") as f:
            branch_log = json.load(f)
    else:
        branch_log = []

    branch_log.append(commit_id)

    with open(branch_path, "w") as f:
        json.dump(branch_log, f, indent=2)

    shutil.rmtree(INDEX_DIR)
    os.makedirs(INDEX_DIR)

    print(f"COMMITTED: {commit_id}: {message}")

def log_commits():
    if not os.path.exists(LOG_FILE):
        print("No commits found.")
        return

    with open(LOG_FILE, "r") as f:
        log = json.load(f)

    if not log:
        print("No commits yet.")
        return

    for entry in reversed(log):  # most recent first
        print(f"Commit: {entry['id']}")
        print(f"Date: {entry['timestamp']}")
        print(f"Message: {entry['message']}\n")

def hash_file(path):
    with open(path, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()

def status():
    workspace_files = set(os.listdir("workspace")) if os.path.exists("workspace") else set()
    index_files = set(os.listdir(INDEX_DIR)) if os.path.exists(INDEX_DIR) else set()

    # Get last commit ID
    if os.path.exists(LOG_FILE):
        import json
        with open(LOG_FILE) as f:
            log = json.load(f)
            last_commit_id = log[-1]['id'] if log else None
    else:
        last_commit_id = None

    committed_files = set()
    committed_hashes = {}

    if last_commit_id:
        commit_path = os.path.join(COMMITS_DIR, last_commit_id)
        if os.path.exists(commit_path):
            committed_files = set(os.listdir(commit_path))
            for fname in committed_files:
                committed_hashes[fname] = hash_file(os.path.join(commit_path, fname))

    print("=== Workspace Status ===")
    for fname in sorted(workspace_files):
        in_index = fname in index_files
        in_commit = fname in committed_files
        file_path = os.path.join("workspace", fname)

        if not in_index and not in_commit:
            print(f"{fname}: Untracked")
        elif in_index and not in_commit:
            print(f"{fname}: Staged for commit")
        elif in_commit:
            current_hash = hash_file(file_path)
            committed_hash = committed_hashes.get(fname)
            if in_index:
                index_hash = hash_file(os.path.join(INDEX_DIR, fname))
                if index_hash == current_hash:
                    print(f"{fname}: Staged (Unmodified)")
                else:
                    print(f"{fname}: Staged but modified")
            elif current_hash != committed_hash:
                print(f"{fname}: Modified but not staged")
            else:
                print(f"{fname}: Unmodified")

    # Files staged but deleted from workspace
    for fname in sorted(index_files - workspace_files):
        print(f"{fname}: Staged but missing in workspace")

def checkout(commit_id):
    commit_path = os.path.join(COMMITS_DIR, commit_id)
    workspace_path = "workspace"

    if not os.path.exists(commit_path):
        print(f"Commit {commit_id} does not exist.")
        return

    if not os.path.exists(workspace_path):
        os.makedirs(workspace_path)

    # Clear workspace
    for fname in os.listdir(workspace_path):
        fpath = os.path.join(workspace_path, fname)
        if os.path.isfile(fpath):
            os.remove(fpath)

    # Copy files from commit into workspace
    for fname in os.listdir(commit_path):
        shutil.copy2(os.path.join(commit_path, fname), os.path.join(workspace_path, fname))

    print(f"Checked out commit {commit_id} to workspace.")

def diff(filepath):
    filename = os.path.basename(filepath)

    if not os.path.exists(filepath):
        print(f"{filename} does not exist in workspace.")
        return

    # Find last commit ID
    if not os.path.exists(LOG_FILE):
        print("No commits found.")
        return

    with open(LOG_FILE) as f:
        log = json.load(f)

    if not log:
        print("No commits found.")
        return

    last_commit_id = log[-1]["id"]
    committed_path = os.path.join(COMMITS_DIR, last_commit_id, filename)

    if not os.path.exists(committed_path):
        print(f"{filename} was not in the last commit.")
        return

    with open(committed_path, "r") as f1:
        committed_lines = f1.readlines()

    with open(filepath, "r") as f2:
        workspace_lines = f2.readlines()

    diff = difflib.unified_diff(
        committed_lines,
        workspace_lines,
        fromfile=f"committed/{filename}",
        tofile=f"workspace/{filename}",
        lineterm=""
    )

    diff_output = list(diff)
    if diff_output:
        print("\n".join(diff_output))
    else:
        print(f"No changes in {filename}.")

def restore(commit_id, filename=None):
    if filename is None:
        filename = commit_id
        if not os.path.exists(LOG_FILE):
            print("No commits found.")
            return
        with open(LOG_FILE) as f:
            log = json.load(f)
            if not log:
                print("No commits found.")
                return
        commit_id = log[-1]["id"]

    commit_path = os.path.join(COMMITS_DIR, commit_id)
    source_file = os.path.join(commit_path, filename)
    destination = os.path.join("workspace", filename)

    if not os.path.exists(commit_path):
        print(f"Commit {commit_id} does not exist.")
        return

    if not os.path.exists(source_file):
        print(f"{filename} not found in commit {commit_id}.")
        return

    os.makedirs("workspace", exist_ok=True)
    shutil.copy2(source_file, destination)
    print(f"Restored {filename} from commit {commit_id} to workspace.")

def history(filename):
    if not os.path.exists(LOG_FILE):
        print("No commits found.")
        return

    with open(LOG_FILE, "r") as f:
        log = json.load(f)

    if not log:
        print("No commits found.")
        return

    found_any = False

    for entry in reversed(log):  # Newest first
        commit_id = entry["id"]
        commit_path = os.path.join(COMMITS_DIR, commit_id)
        committed_file = os.path.join(commit_path, filename)

        if os.path.exists(committed_file):
            print(f"Commit: {commit_id}")
            print(f"Date: {entry['timestamp']}")
            print(f"Message: {entry['message']}\n")
            found_any = True

    if not found_any:
        print(f"No history found for {filename}.")

def get_current_branch():
    if os.path.exists(HEAD_FILE):
        with open(HEAD_FILE, "r") as f:
            return f.read().strip()
    return "main" 

def branch(name):
    os.makedirs(BRANCHES_DIR, exist_ok=True)
    current = get_current_branch()
    current_path = os.path.join(BRANCHES_DIR, f"{current}.json")
    new_path = os.path.join(BRANCHES_DIR, f"{name}.json")

    if os.path.exists(new_path):
        print(f"Branch {name} already exists.")
        return

    if not os.path.exists(current_path):
        print(f"Current branch {current} has no history.")
        return

    shutil.copy2(current_path, new_path)
    print(f"Created branch {name} from {current}")

def checkout_branch(name):
    branch_path = os.path.join(BRANCHES_DIR, f"{name}.json")
    if not os.path.exists(branch_path):
        print(f"Branch {name} does not exist.")
        return

    with open(HEAD_FILE, "w") as f:
        f.write(name)

    with open(branch_path, "r") as f:
        commits = json.load(f)

    if not commits:
        print(f"Switched to branch {name} (no commits yet)")
        return

    latest_commit = commits[-1]
    checkout(latest_commit)
    print(f"Switched to branch {name}")

def current_branch():
    if not os.path.exists(HEAD_FILE):
        print("No branch found.")
        return
    with open(HEAD_FILE) as f:
        print(f"Current branch: {f.read().strip()}")

def rm(filename):
    path = os.path.join(INDEX_DIR, os.path.basename(filename))
    if os.path.exists(path):
        os.remove(path)
        print(f"Removed {filename} from staging area.")
    else:
        print(f"{filename} is not staged.")

def reset():
    if os.path.exists(INDEX_DIR):
        shutil.rmtree(INDEX_DIR)
        os.makedirs(INDEX_DIR)
        print("Staging area reset.")
    else:
        print("Nothing to reset.")

def commit_all(message):
    workspace_files = os.listdir("workspace") if os.path.exists("workspace") else []
    for fname in workspace_files:
        add_file(os.path.join("workspace", fname))  # reuse add logic

    commit(message)

def help():
    print("""
    Available commands:
    init                      Initialize a new repository
    add <file>                Stage a file
    commit "<msg>"            Commit staged files
    commit -a "<msg>"         Auto-stage all workspace files and commit
    log                       Show commit history
    status                    Show file states (modified, staged, etc.)
    diff <file>               Compare file to last commit
    restore <commit> <file>   Restore a file from a commit
    history <file>            Show commit history for a file
    branch <name>             Create a new branch
    checkout-branch <name>    Switch to a branch and load its latest commit
    current-branch            Show active branch
    checkout <commit>         Restore workspace to a previous commit
    rm <file>                 Remove a file from the staging area
    reset                     Clear the staging area
    help                      Show this help message
    """)

def workspace_has_changes():
    workspace_files = set(os.listdir("workspace")) if os.path.exists("workspace") else set()
    index_files = set(os.listdir(INDEX_DIR)) if os.path.exists(INDEX_DIR) else set()

    if not os.path.exists(LOG_FILE):
        return bool(workspace_files)

    with open(LOG_FILE, "r") as f:
        log = json.load(f)
        if not log:
            return bool(workspace_files)

    last_commit_id = log[-1]["id"]
    commit_path = os.path.join(COMMITS_DIR, last_commit_id)
    committed_files = set(os.listdir(commit_path)) if os.path.exists(commit_path) else set()

    # check untracked or modified files
    for fname in workspace_files:
        if fname not in committed_files:
            return True
        with open(os.path.join("workspace", fname), "rb") as f1:
            with open(os.path.join(commit_path, fname), "rb") as f2:
                if f1.read() != f2.read():
                    return True
    return False

def diff_commits(commit1, commit2):
    path1 = os.path.join(COMMITS_DIR, commit1)
    path2 = os.path.join(COMMITS_DIR, commit2)

    if not os.path.exists(path1) or not os.path.exists(path2):
        print("One or both commits not found.")
        return

    files1 = set(os.listdir(path1))
    files2 = set(os.listdir(path2))
    common_files = files1 & files2

    if not common_files:
        print("No common files to compare.")
        return

    for fname in sorted(common_files):
        with open(os.path.join(path1, fname), "r") as f1, open(os.path.join(path2, fname), "r") as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
            diff = list(difflib.unified_diff(lines1, lines2, fromfile=f"{commit1}/{fname}", tofile=f"{commit2}/{fname}", lineterm=""))
            if diff:
                print("\n".join(diff))

def log_branch(branch_name):
    branch_file = os.path.join(BRANCHES_DIR, f"{branch_name}.json")
    if not os.path.exists(branch_file):
        print(f"Branch {branch_name} does not exist.")
        return

    with open(branch_file) as f:
        commits = json.load(f)

    with open(LOG_FILE) as f:
        log = json.load(f)

    for cid in reversed(commits):
        for entry in log:
            if entry["id"] == cid:
                print(f"Commit: {entry['id']}")
                print(f"Date: {entry['timestamp']}")
                print(f"Message: {entry['message']}\n")

def push(remote_path: str) -> dict:
    try:
        shutil.copytree(VCS_DIR, os.path.join(remote_path, ".myvcs"), dirs_exist_ok=True)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

def pull(remote_path: str) -> dict:
    try:
        shutil.copytree(os.path.join(remote_path, ".myvcs"), VCS_DIR, dirs_exist_ok=True)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

def merge(branch_name: str) -> dict:
    target_file = os.path.join(BRANCHES_DIR, f"{branch_name}.json")
    if not os.path.exists(target_file):
        return {"success": False, "error": "Branch not found"}

    with open(target_file) as f:
        target_commits = json.load(f)
    if not target_commits:
        return {"success": False, "error": "Target branch is empty"}

    target_commit = target_commits[-1]
    target_path = os.path.join(COMMITS_DIR, target_commit)

    for fname in os.listdir(target_path):
        shutil.copy2(os.path.join(target_path, fname), os.path.join(INDEX_DIR, fname))

    return {"success": True, "merged_from": branch_name}

def revert(commit_id: str) -> dict:
    commit_path = os.path.join(COMMITS_DIR, commit_id)
    if not os.path.exists(commit_path):
        return {"success": False, "error": "Commit not found"}

    latest_commit = None
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            log = json.load(f)
            if log and log[-1]["id"] == commit_id:
                return {"success": False, "error": "Can't revert HEAD directly"}
            for i in range(len(log)-1):
                if log[i]["id"] == commit_id:
                    latest_commit = log[i+1]["id"]
                    break

    if latest_commit is None:
        return {"success": False, "error": "No child commit to revert against"}

    # Reverse diff: just replace files from parent (crude revert)
    child_path = os.path.join(COMMITS_DIR, latest_commit)
    for fname in os.listdir(commit_path):
        old_file = os.path.join(child_path, fname)
        if os.path.exists(old_file):
            shutil.copy2(old_file, os.path.join(INDEX_DIR, fname))

    return commit(f"Revert commit {commit_id}")

STASH_DIR = os.path.join(VCS_DIR, "stash")

def stash() -> dict:
    if not os.path.exists("workspace"):
        return {"success": False, "error": "No workspace"}

    os.makedirs(STASH_DIR, exist_ok=True)
    i = 0
    while os.path.exists(os.path.join(STASH_DIR, f"stash{i}")):
        i += 1
    stash_path = os.path.join(STASH_DIR, f"stash{i}")
    os.makedirs(stash_path)

    for fname in os.listdir("workspace"):
        shutil.copy2(os.path.join("workspace", fname), os.path.join(stash_path, fname))
        os.remove(os.path.join("workspace", fname))

    return {"success": True, "stash": f"stash{i}"}

def stash_pop() -> dict:
    if not os.path.exists(STASH_DIR):
        return {"success": False, "error": "No stash exists"}

    stashes = sorted(os.listdir(STASH_DIR))
    if not stashes:
        return {"success": False, "error": "Stash is empty"}

    latest = stashes[-1]
    stash_path = os.path.join(STASH_DIR, latest)

    for fname in os.listdir(stash_path):
        shutil.copy2(os.path.join(stash_path, fname), os.path.join("workspace", fname))

    shutil.rmtree(stash_path)
    return {"success": True, "restored": latest}





TAGS_FILE = os.path.join(VCS_DIR, "tags.json")

def tag(name: str, commit_id: str) -> dict:
    if not os.path.exists(os.path.join(COMMITS_DIR, commit_id)):
        return {"success": False, "error": "Commit does not exist"}

    tags = {}
    if os.path.exists(TAGS_FILE):
        with open(TAGS_FILE) as f:
            tags = json.load(f)

    tags[name] = commit_id
    with open(TAGS_FILE, "w") as f:
        json.dump(tags, f, indent=2)

    return {"success": True, "tag": name, "commit": commit_id}

def list_tags() -> list:
    if not os.path.exists(TAGS_FILE):
        return []
    with open(TAGS_FILE) as f:
        return json.load(f)
