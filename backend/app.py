from flask import Flask, request, jsonify
from flask_cors import CORS
from vcs.vcs  import (
    init_repo, add_file, commit, commit_all, log_commits, log_branch, 
    status, diff, diff_commits, restore, history, branch, checkout_branch, 
    current_branch, rm, reset, tag, list_tags, stash, stash_pop, revert, 
    merge, push, pull
)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests (React uses port 3000)

# === Basic Operations ===

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Welcome to the MyVCS API!",
        "endpoints": [
            "/init (POST)",
            "/status (GET)",
            "/log (GET)",
            "/commit (POST)",
            "/add (POST)",
            "/current-branch (GET)",
            "/branch (POST)",
            "/stash (POST)",
            "/stash/pop (POST)",
            "/restore (POST)",
            "/merge (POST)",
            "/revert (POST)",
            "/push (POST)",
            "/pull (POST)"
        ]
    })

@app.route("/init", methods=["GET", "POST"])
def init():
    if request.method == "POST":
        init_repo()
        return jsonify({"success": True})
    return jsonify({"message": "Use POST to initialize the repository."})


@app.route("/add", methods=["POST"])
def add():
    data = request.json
    filename = data.get("filename")
    add_file(filename)
    return jsonify({"success": True, "file": filename})

@app.route("/commit", methods=["POST"])
def commit_route():
    data = request.json
    message = data.get("message")
    if data.get("all", False):
        result = commit_all(message)
    else:
        result = commit(message)
    return jsonify(result), 400 if not result["success"] else 200

@app.route("/status", methods=["GET"])
def status_route():
    return jsonify(status())

@app.route("/log", methods=["GET"])
def log_route():
    return jsonify(log_commits())

@app.route("/log/<branch_name>", methods=["GET"])
def log_branch_route(branch_name):
    return jsonify(log_branch(branch_name))

@app.route("/diff", methods=["POST"])
def diff_route():
    data = request.json
    file = data.get("file")
    return jsonify({"diff": diff(file)})

@app.route("/diff/<commit1>/<commit2>", methods=["GET"])
def diff_commits_route(commit1, commit2):
    return jsonify({"diff": diff_commits(commit1, commit2)})

@app.route("/restore", methods=["POST"])
def restore_route():
    data = request.json
    commit_id = data.get("commit_id")
    filename = data.get("filename")
    result = restore(commit_id, filename)
    return jsonify(result), 400 if not result["success"] else 200

@app.route("/history/<filename>", methods=["GET"])
def history_route(filename):
    return jsonify(history(filename))

# === Branching ===

@app.route("/branch", methods=["POST"])
def branch_route():
    data = request.json
    name = data.get("name")
    branch(name)
    return jsonify({"success": True, "branch": name})

@app.route("/checkout-branch", methods=["POST"])
def checkout_branch_route():
    data = request.json
    name = data.get("name")
    checkout_branch(name)
    return jsonify({"success": True, "branch": name})

@app.route("/current-branch", methods=["GET"])
def current_branch_route():
    return jsonify({"branch": current_branch()})

# === File/Staging ===

@app.route("/rm", methods=["POST"])
def rm_route():
    data = request.json
    rm(data.get("filename"))
    return jsonify({"success": True})

@app.route("/reset", methods=["POST"])
def reset_route():
    reset()
    return jsonify({"success": True})

# === Tagging ===

@app.route("/tag", methods=["POST"])
def tag_route():
    data = request.json
    return jsonify(tag(data["name"], data["commit_id"]))

@app.route("/tags", methods=["GET"])
def list_tags_route():
    return jsonify(list_tags())

# === Stashing ===

@app.route("/stash", methods=["POST"])
def stash_route():
    return jsonify(stash())

@app.route("/stash/pop", methods=["POST"])
def stash_pop_route():
    return jsonify(stash_pop())

# === Reverting & Merging ===

@app.route("/revert", methods=["POST"])
def revert_route():
    data = request.json
    return jsonify(revert(data["commit_id"]))

@app.route("/merge", methods=["POST"])
def merge_route():
    data = request.json
    return jsonify(merge(data["branch"]))

# === Remotes ===

@app.route("/push", methods=["POST"])
def push_route():
    data = request.json
    return jsonify(push(data["remote_path"]))

@app.route("/pull", methods=["POST"])
def pull_route():
    data = request.json
    return jsonify(pull(data["remote_path"]))

# === Run ===

if __name__ == "__main__":
    app.run(debug=True)
