# Students Service v2.0 (Lab 4 - Re-engineering & Migration)

Re-engineered from the v1.1 console app into a layered service.

```
app/
  models.py       # Pydantic models (StudentIn, Student)
  utils.py        # statistics + table formatting (pure functions)
  database.py     # SQLite connection + schema
  controllers.py  # use cases
  main.py         # FastAPI REST API
  cli.py          # console report
migrate.py        # JSON -> SQLite migration
data/students.json
tests/            # pytest (API + migration)
Dockerfile, docker-compose.yml
docs/             # reverse-engineering notes and dependency diagrams
```

## Run locally
```
pip install -r requirements.txt
python migrate.py            # creates data/students.db from data/students.json
python -m app.cli            # console report
uvicorn app.main:app --reload   # http://127.0.0.1:8000/docs
pytest
```

## Run with Docker Compose
```
docker compose up --build
# API:    http://localhost:8000/docs
# Report: docker compose logs report
```

## API
| Method | Path | Description |
|---|---|---|
| GET | /health | liveness |
| GET | /students | list |
| POST | /students | create `{name, score}` |
| GET | /students/{id} | read |
| DELETE | /students/{id} | delete |
| GET | /stats | count, average, median, highest, lowest |
