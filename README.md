# VCS - Custom Version Control System

VCS is a lightweight, Git-inspired version control system built from scratch in Python. It supports file tracking, commits, branches, tags, merges, stashing, and more. VCS comes with:

- ✅ A command-line interface (CLI)
- ✅ A Flask REST API backend
- ✅ A modern React frontend GUI

---

## 🚀 Features

- `init`, `add`, `commit`, `log`, `status`, `diff`, `restore`, `checkout`
- Branching: `branch`, `checkout-branch`, `current-branch`
- History: `history`, `tag`, `stash`, `revert`, `merge`
- Remote support: `push`, `pull`
- GUI with commit viewer, status display, and file restore actions

---

## 📦 Project Structure

```
vcs_project/
├── backend/               # Flask API
│   ├── app.py             # RESTful API for frontend
│   ├── requirements.txt   # Flask and CORS
│   └── vcs/               # Core version control logic
│       ├── config.py
│       └── vcs.py
├── frontend/              # React UI
│   ├── src/               # React components and logic
│   ├── public/
│   └── package.json
├── workspace/             # Simulated working directory
├── .vcs/                  # Internal VCS metadata (auto-created)
├── main.py                # CLI entry point
└── README.md
```

---

## 🖥️ Setup Instructions

### 1. Backend (Flask API)

```bash
cd backend
python -m venv venv
source venv\Scripts\activate 
pip install -r requirements.txt
flask run
```

### 2. Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`, Flask runs on `http://localhost:5000`.

---

## 🧪 CLI Usage

```bash
python main.py init
python main.py add file.txt
python main.py commit "Initial commit"
python main.py log
python main.py branch feature
python main.py checkout-branch feature
```

Run `python main.py help` for a full list of commands.

---

## 🌐 API Endpoints (Flask)

| Method | Route                 | Description                     |
|--------|-----------------------|---------------------------------|
| POST   | `/init`               | Initialize repository           |
| POST   | `/commit`             | Commit staged files             |
| GET    | `/log`                | View commit history             |
| GET    | `/status`             | Get file status                 |
| POST   | `/add`                | Stage a file                    |
| POST   | `/restore`            | Restore a file from a commit    |
| POST   | `/stash`              | Save stash                      |
| POST   | `/stash/pop`          | Pop stash                       |
| ...    | *many more*           | See `app.py`                    |

---

## 📚 Technologies Used

- **Python 3.10+**
- **Flask** – REST API backend
- **React + Vite** – frontend UI
- **Axios** – frontend HTTP client
- **JSON + filesystem** – metadata storage

---

## 📝 License

MIT License – free to use, modify, and build upon.

---

## 🙋‍♂️ Author

**Roman Bukhovko**
