import os

VCS_DIR = ".vcs"
COMMITS_DIR = os.path.join(VCS_DIR, "commits")
INDEX_DIR = os.path.join(VCS_DIR, "index")
LOG_FILE = os.path.join(VCS_DIR, "log.json")
BRANCHES_DIR = os.path.join(VCS_DIR, "branches")
HEAD_FILE = os.path.join(VCS_DIR, "HEAD")