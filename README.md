# Job Application Tracker (WIP)

FastAPI REST API to track job applications (company, role, status, dates, notes).

## Status

Work in progress — MVP under development.

## Planned Features

- CRUD for applications
- Filtering + pagination
- Stats endpoint
- Tests + GitHub Actions CI
- Docker (optional)

## Tech (planned)

FastAPI · Pydantic · SQLAlchemy · SQLite · Pytest

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
