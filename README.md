# Book API — Auth & Access Control (FastAPI + JWT + SQLAlchemy)

A REST API built with **FastAPI**, **SQLAlchemy** and **Pydantic**, extending
a library CRUD (books and authors) with a full authentication and
authorization layer: password hashing, JWT-based login, protected endpoints,
and role-based access control (`user` / `admin`).

This project favors clarity over completeness — each file has a single,
well-defined responsibility.

## Features

- Password hashing with `bcrypt` (automatic salting)
- User registration and login (`/auth/register`, `/auth/login`)
- JWT access tokens (`python-jwt`, HS256, expiring)
- Protected endpoints via FastAPI dependencies (`get_current_user`)
- Role-based access control (`require_admin`) — `user` vs `admin` permissions
- Proper HTTP status codes (`401 Unauthorized`, `403 Forbidden`, `404 Not Found`)
- Full CRUD for `Book` and `Author`, with a one-to-many relationship
- Passwords are never included in API responses
- Interactive API docs via Swagger UI, with built-in "Authorize" support

## Tech stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/) (ORM)
- [Pydantic](https://docs.pydantic.dev/)
- [bcrypt](https://pypi.org/project/bcrypt/) for password hashing
- [PyJWT](https://pyjwt.readthedocs.io/) for token creation/validation
- SQLite by default (zero setup), swappable for PostgreSQL/MySQL via `DATABASE_URL`

## Project structure

```
.
├── main.py          # FastAPI app and HTTP routes
├── database.py      # Engine, session, and DB connection setup
├── models.py        # SQLAlchemy ORM models (tables)
├── schemas.py        # Pydantic schemas (request/response validation)
├── crud.py          # Database access functions
├── security.py       # Password hashing and JWT helpers
└── dependencies.py   # Auth dependencies (get_current_user, require_admin)
```

## Getting started

```
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000/docs` for the interactive Swagger UI. Log
in via `/auth/login`, copy the returned token, and use the **Authorize**
button (`Bearer <token>`) to call protected routes from the docs.

By default the API uses SQLite (a `livraria.db` file created automatically
on first run). To use PostgreSQL or MySQL instead, set the `DATABASE_URL`
environment variable:

```
export DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
```

In production, also set a strong `SECRET_KEY` environment variable (used to
sign JWTs) instead of relying on the development default.

## Endpoints

| Method | Endpoint              | Auth required | Description                      |
| ------ | ---------------------- | -------------- | --------------------------------- |
| POST   | `/auth/register`       | —              | Register a new user               |
| POST   | `/auth/login`          | —              | Log in, returns a JWT             |
| GET    | `/users/me`            | any user       | Get the logged-in user's profile  |
| GET    | `/users`               | any user       | List all users                    |
| DELETE | `/users/{id}`          | admin only     | Delete a user                     |
| GET    | `/books`               | —              | List all books                    |
| GET    | `/books/{id}`          | —              | Get a single book                 |
| POST   | `/books`               | any user       | Create a new book                 |
| PUT    | `/books/{id}`          | any user       | Update a book                     |
| DELETE | `/books/{id}`          | admin only     | Delete a book                     |
| GET    | `/authors`             | —              | List all authors                  |
| GET    | `/authors/{id}`        | —              | Get a single author               |
| POST   | `/authors`             | any user       | Create a new author               |
| PUT    | `/authors/{id}`        | any user       | Update an author                  |
| DELETE | `/authors/{id}`        | admin only     | Delete an author                  |
| GET    | `/authors/{id}/books`  | —              | List all books by a given author  |

---

Developed by Nicolly Pereira