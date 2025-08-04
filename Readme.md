# 🧵 Mini Social Media API

A scalable, containerized REST API built with **FastAPI**, powered by **PostgreSQL**, and orchestrated with **Docker**. It features secure user authentication, post creation with voting mechanics, and robust testing/migration pipelines via **Alembic** and **Pytest**.

---

## 🧠 Features

- 👤 **User Registration & Login**  
  Secure signup/login with password hashing and JWT-based authentication.

- 📝 **Create & Manage Posts**  
  Authenticated users can create, retrieve, update, and delete posts.

- 📊 **Voting System**  
  Vote for posts with automatic vote count aggregation and conflict checks.

- 🔒 **Token-Based Auth**  
  OAuth2 scheme with JWT tokens tied to access expiration logic.

- ⚙️ **Database Migrations**  
  Alembic tracks schema changes in `/versions` for reproducible upgrades.

- 🧪 **Test Coverage**  
  Pytest verifies critical workflows using isolated testing database.

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone git@github.com:kevin-ndolo/mini-socialmedia-app.git
cd mini-socialmedia-app
```

### 2. Create `.env` file and configure environment
```env
DATABASE_HOSTNAME=
DATABASE_PORT=
DATABASE_USERNAME=
DATABASE_PASSWORD=
DATABASE_NAME=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
```

### 3. Run with Docker Compose
```bash
docker-compose -f docker-compose-prod.yml up --build
```

Visit [http://localhost](http://localhost) to test endpoints.

---

## 🧱 Tech Stack

| Layer            | Technology           |
|------------------|----------------------|
| API Framework    | FastAPI              |
| ORM              | SQLAlchemy           |
| Auth             | OAuth2 + JWT         |
| Database         | PostgreSQL           |
| Migrations       | Alembic              |
| Containerization | Docker + Compose     |
| Testing          | Pytest               |

---

## 🧪 Running Tests
Tests are written with Pytest and use a dedicated test database for isolation:

```bash
pytest --disable-warnings -vsx ./tests/test_users.py
```

Fixtures handle DB setup/teardown and TestClient overrides.

---

## 📂 Project Structure Highlights
```bash
.
├── app              # Core API logic and routing
├── alembic          # Database migration history
├── tests            # Pytest test cases & setup
├── Dockerfile       # API container setup
├── docker-compose-prod.yml
└── requirements.txt
```

---

## 🗒️ Notes

- Token verification, user identity extraction, and database sessions are cleanly modularized.
- Alembic migrations are auto-generated and applied through `env.py` wiring to models.
- Test suite uses dependency overrides to isolate production code from test logic.

---

## 📄 License
MIT — use, remix, and deploy freely.