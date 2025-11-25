# Project Setup Prompt for AI

Use this prompt to set up a FastAPI project with similar structure:

---

**Create the folder structure for a FastAPI project:**

```
project_name/
├── alembic/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
├── alembic.ini
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── clients/
│   │   └── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── logging.py
│   │   ├── response.py
│   │   ├── security.py
│   │   └── utils.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── session.py
│   ├── entities/
│   │   ├── __init__.py
│   │   └── [entity_name]/
│   │       ├── model.py
│   │       ├── schema.py
│   │       └── service.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── [entity_name].py
│   ├── seeds/
│   │   ├── __init__.py
│   │   └── colors.py
│   └── utils/
│       └── constant.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_*.py
├── scripts/
│   └── script.sh
├── pyproject.toml
└── README.md
```

**Initialize Poetry with:**
- Python ^3.12
- FastAPI, SQLAlchemy, Alembic, psycopg2-binary
- pytest for dev dependencies

**Initialize Alembic** with basic configuration.

**Create empty Python files** with just `__init__.py` or basic file structure. Do NOT implement any code logic - just create the folder structure and empty files.

