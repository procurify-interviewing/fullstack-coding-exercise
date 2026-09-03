# Backend Exercise

## Part 1: Build an Approve-aware Purchase Requests API
Build an approver-aware Purchase Requests API. Your API lets clients retrieve purchase requests over HTTP.

The endpoint returns the purchase requests the current user is allowed to see:
- requests they created, or
- requests where they are an approver.		

Models are predefined and there are some data already seeded in the SQLite database.

Make decisions on missing requirements - talk through and explain decisions made. Aim for implementation as if this is used in production.


# Project Setup

A Django application backed by SQLite. It serves the JSON API that the frontend consumes.

Django REST Framework is installed and configured, using it is optional.

## Running the project

Application code lives under `src/`. Run `manage.py` from there:

```bash
source .venv/bin/activate          # Windows: .\.venv\Scripts\Activate.ps1
cd src
python manage.py runserver 8000
```

The `make` targets in the repo root (`make run-backend`, `make test-backend`) do this for you
and do not need the virtualenv activated.

## Database

SQLite, in a single file at `backend/db.sqlite3`. Nothing to install or run - SQLite ships with
Python. The file is created by `python manage.py migrate`.

```bash
rm db.sqlite3
cd src && python manage.py migrate && python manage.py seed_data
```

`BASE_DIR` in `settings.py` resolves to this directory.

## Tests

Everything lives in `src/tests/` and runs under pytest:

- `factories.py`: helpers for building test data
- `conftest.py`: test fixtures

Run them from this directory, or with `make test-backend` from the repo root:

```bash
pytest src/tests/
```

## The exercise

You may add files and packages. If you want to change the models, say so first.
