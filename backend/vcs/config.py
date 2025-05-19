import os

# Base directory for the VCS metadata
VCS_DIR = ".myvcs"

# Subdirectories within .myvcs
COMMITS_DIR = os.path.join(VCS_DIR, "commits")
INDEX_DIR = os.path.join(VCS_DIR, "index")
BRANCHES_DIR = os.path.join(VCS_DIR, "branches")
STASH_DIR = os.path.join(VCS_DIR, "stash")

# Metadata files
LOG_FILE = os.path.join(VCS_DIR, "log.json")
TAGS_FILE = os.path.join(VCS_DIR, "tags.json")
HEAD_FILE = os.path.join(VCS_DIR, "HEAD")

# The working directory where user files are
WORKSPACE_DIR = "workspace"