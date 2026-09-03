# Backend

A Django application backed by SQLite. It serves the JSON API that the frontend consumes.

Django REST Framework is installed and configured, using it is optional.

Application code lives under `src/`. Run `manage.py` from there:

```bash
source .venv/bin/activate          # Windows: .\.venv\Scripts\Activate.ps1
cd src
python manage.py runserver 8000
```

The `make` targets in the repo root (`make backend`, `make test`, `make seed`) do this for you
and do not need the virtualenv activated.

## Database

SQLite, in a single file at `backend/db.sqlite3`. Nothing to install or run - SQLite ships with
Python. The file is created by `python manage.py migrate` and is gitignored, so it is safe to
delete and rebuild:

```bash
rm db.sqlite3
cd src && python manage.py migrate && python manage.py seed_data
```

`BASE_DIR` in `settings.py` resolves to this directory, so the database file stays out of `src/`
no matter which directory you run `manage.py` from.

User models come from `django.contrib.auth`.

## Tests

Everything lives in `src/tests/` and runs under pytest:

- `test_project.py` - `ProjectTests`, two sanity checks that the endpoint is routed and the
  factories work. These pass as handed over.
- `test_purchase_request_api.py` - the API tests. The request is wired up and the fixtures are
  ready, but it calls `pytest.fail(...)` instead of asserting anything. **It fails until you
  write it.** That is deliberate, and it is yours to fill in.
- `factories.py` - helpers for building test data, no external factory library.
- `conftest.py` - fixtures: `alice` (a requester), `bob` (an approver), and `pending_request`
  (alice's request awaiting bob's decision).

Run them from this directory, or with `make test` from the repo root:

```bash
pytest
```

`python manage.py test` collects nothing - these are pytest test cases, not
`django.test.TestCase` subclasses. Use pytest.

## The exercise

The brief is in `../EXERCISE.md`. You may add files and packages. If you want to change the models, say so first.
