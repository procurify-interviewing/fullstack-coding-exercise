.PHONY: setup run run-backend run-frontend test-backend test-frontend

# Entry-point scripts in .venv/bin bake in an absolute shebang when the venv is
# created, so commands are invoked as modules through the interpreter instead.
PYTHON := .venv/bin/python

# manage.py runs with src/ as the working directory so that test discovery and
# app imports resolve; settings put db.sqlite3 in backend/ regardless.
MANAGE := cd backend/src && ../$(PYTHON) manage.py

# pytest.ini lives in backend/ and puts src/ on the path.
PYTEST := cd backend && $(PYTHON) -m pytest

# Installs both halves, migrates and seeds the database.
setup:
	./setup.sh

# Runs the API and the dev server together.
run:
	$(MAKE) -j2 run-backend run-frontend

run-backend:
	$(MANAGE) runserver 8000

run-frontend:
	npm run dev --prefix frontend

test-backend:
	$(PYTEST)

# The frontend has no test runner yet; type checking is the available check.
test-frontend:
	npm run typecheck --prefix frontend
