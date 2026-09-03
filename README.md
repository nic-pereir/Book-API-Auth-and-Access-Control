# Authentication and Authorization

Evolution of the week 6 Book API (FastAPI + SQLAlchemy + Pydantic), adding
user registration/login, JWT, and role-based access control (`user` / `admin`).

## What was added

| File | What it does |
|---|---|
| `security.py` | Password hashing with `bcrypt` and JWT creation/validation |
| `dependencies.py` | `get_current_user` (requires a valid token) and `require_admin` (requires admin role) |
| `models.py` | New `User` model (name, unique email, hashed_password, role) |
| `schemas.py` | `UserCreate`, `UserLogin`, `UserOut` (no password!), `Token` |
| `crud.py` | Data access functions for `User` |
| `main.py` | Routes `/auth/register`, `/auth/login`, `/users/me`, `/users`, `/users/{id}` + protection added to `books`/`authors` routes |

`database.py` did not change.

## How to run

```
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs`. In Swagger, use the "Authorize" button
with the token returned by `/auth/login` (format `Bearer <token>`) to test
the protected routes.

## Who can do what

| Route | No token | USER | ADMIN |
|---|---|---|---|
| `GET /books`, `/authors` | ✅ | ✅ | ✅ |
| `POST`/`PUT` books, authors | 401 | ✅ | ✅ |
| `DELETE` books, authors | 401 | 403 | ✅ |
| `GET /users/me` | 401 | ✅ | ✅ |
| `GET /users` | 401 | ✅ | ✅ |
| `DELETE /users/{id}` | 401 | 403 | ✅ |

