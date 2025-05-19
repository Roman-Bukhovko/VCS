import sys
from vcs import vcs

def main():
    args = sys.argv
    if len(args) < 2:
        print("Usage: python main.py <command> [args]")
        return

    cmd = args[1]

    if cmd == "init":
        vcs.init_repo()

    elif cmd == "add" and len(args) == 3:
        vcs.add_file(args[2])

    elif cmd == "commit":
        if len(args) >= 4 and args[2] == "-a":
            vcs.commit_all(args[3])
        elif len(args) >= 3:
            vcs.commit(args[2])
        else:
            print("Usage: python main.py commit [-a] <message>")

    elif cmd == "log":
        if len(args) == 4 and args[2] == "--branch":
            vcs.log_branch(args[3])
        else:
            vcs.log_commits()

    elif cmd == "status":
        vcs.status()

    elif cmd == "diff":
        if len(args) == 3:
            vcs.diff(args[2])
        elif len(args) == 4:
            vcs.diff_commits(args[2], args[3])
        else:
            print("Usage: python main.py diff <file> OR <commit1> <commit2>")

    elif cmd == "checkout" and len(args) == 3:
        vcs.checkout(args[2])

    elif cmd == "restore":
        if len(args) == 3:
            vcs.restore(args[2])
        elif len(args) == 4:
            vcs.restore(args[2], args[3])
        else:
            print("Usage: python main.py restore <filename> OR <commit> <filename>")

    elif cmd == "history" and len(args) == 3:
        vcs.history(args[2])

    elif cmd == "branch" and len(args) == 3:
        vcs.branch(args[2])

    elif cmd == "checkout-branch" and len(args) == 3:
        vcs.checkout_branch(args[2])

    elif cmd == "current-branch":
        vcs.current_branch()

    elif cmd == "rm" and len(args) == 3:
        vcs.rm(args[2])

    elif cmd == "reset":
        vcs.reset()

    elif cmd == "help":
        vcs.help()

    elif cmd == "tag":
        if len(args) == 4:
            print(vcs.tag(args[2], args[3]))
        elif len(args) == 3 and args[2] == "--list":
            print(vcs.list_tags())
        else:
            print("Usage: python main.py tag <name> <commit_id> OR tag --list")

    elif cmd == "stash":
        if len(args) == 2:
            print(vcs.stash())
        elif len(args) == 3 and args[2] == "pop":
            print(vcs.stash_pop())
        else:
            print("Usage: python main.py stash OR stash pop")

    elif cmd == "revert" and len(args) == 3:
        print(vcs.revert(args[2]))

    elif cmd == "merge" and len(args) == 3:
        print(vcs.merge(args[2]))

    elif cmd == "push" and len(args) == 3:
        print(vcs.push(args[2]))

    elif cmd == "pull" and len(args) == 3:
        print(vcs.pull(args[2]))

    else:
        print("Unknown command. Run `python main.py help` for list of commands.")

if __name__ == "__main__":
    main()
