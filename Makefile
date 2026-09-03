.PHONY: setup migrate seed backend run frontend dev test

# manage.py runs with src/ as the working directory so that test discovery and
# app imports resolve; settings put db.sqlite3 in backend/ regardless.
MANAGE := cd backend/src && ../.venv/bin/python manage.py

setup:
	./setup.sh

migrate:
	$(MANAGE) migrate

seed:
	$(MANAGE) seed_data

backend:
	$(MANAGE) runserver 8000

run: backend

frontend:
	npm run dev --prefix frontend

dev:
	$(MAKE) -j2 backend frontend

test:
	cd backend && .venv/bin/pytest
