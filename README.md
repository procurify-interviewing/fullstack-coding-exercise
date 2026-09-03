# Interview Exercise - Purchase Requests

A small Django + React project. It runs, but the API endpoint is a stub and the React app is a
shell. The brief is in `EXERCISE.md`.

## Goal
Implement the API on the `backend/` project according to the problem statements and build a React component 
in the `frontend/` project to consume the API locally. 

## Prerequisites

- Python 3.10 or newer (`python3 --version`). SQLite ships with Python.
- Node 20 or newer (`node --version`).
- No Docker, no database server.

## Setup after a fresh clone

macOS / Linux:

```bash
./setup.sh
```

Windows (PowerShell):

```powershell
.\setup.ps1
```

The automated scripts creates `backend/.venv`, installs the Python dependencies, runs migrations, seeds
sample data, and runs the tests, and installs the frontend's npm dependencies. It takes a couple of
minutes on a normal connection.

Manual setup:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate          # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd src
python manage.py migrate
python manage.py seed_data
python manage.py test
cd ../../frontend
npm install
```

## Run

```bash
make run
```

Starts both frontend and backend servers

| | |
| --- | --- |
| Frontend | <http://localhost:5173> |
| API | <http://localhost:8000/api/purchase-requests/> |

Open the frontend and you should see a `501 Not Implemented` response rendered on the page.
That is the Django stub, reached through the dev server. The React app calls relative
`/api/...` paths and Vite proxies them to Django, so there is no CORS to configure and no API
base URL to set.

To run one half on its own: `make run-backend` or `make run-frontend`.


## Troubleshooting

- `python: command not found` - use `python3`, or run `./setup.sh` which finds the right interpreter.
- `No module named django` - the virtualenv is not active. Run the activate line above, or use the `make` targets, which do not need it.
- `npm: command not found` - install Node 20 or newer from <https://nodejs.org/>.
- `Port 8000 is already in use` - `python manage.py runserver 8001`, and point `vite.config.ts`'s proxy target at the same port.
- `Port 5173 is already in use` - `npm run dev --prefix frontend -- --port 5174`.
- PowerShell refuses to run `setup.ps1` - run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first, then retry.
- For a clean slate, delete `backend/db.sqlite3` and re-run `./setup.sh`.
