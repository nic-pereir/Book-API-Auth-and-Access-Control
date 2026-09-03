# Week 7 — Authentication and Authorization

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

I went a bit beyond what the exercises asked by also protecting
`books`/`authors` with both access levels (not just `/users`), so that
`role` actually means something across more than one route — if you'd
rather present only the exact scope that was asked (users), just remove the
`get_current_user`/`require_admin` `Depends` from the books/authors routes.

## Extra challenge — 3 security issues found

1. **Weak/default JWT secret in production**
   `SECRET_KEY` has a hardcoded default value (`dev-only-secret-change-me`),
   and the token expires after 30 minutes — but if someone ran this in
   production without setting the `SECRET_KEY` environment variable, anyone
   could forge valid tokens. Fix: require `SECRET_KEY` via environment
   variable (fail to start the app if it's missing) and never commit
   secrets to the repository.

2. **No password confirmation / weak password policy at registration**
   `POST /auth/register` accepts any string as a password (even `"1"`),
   with no minimum length requirement. Fix: enforce a minimum length (e.g.
   8 characters) in `UserCreate` with a Pydantic `field_validator`, and
   ideally check against known leaked-password lists.

3. **No rate limiting on `/auth/login`**
   As it stands, nothing prevents a brute-force attack against the login
   endpoint (trying thousands of passwords per second). Fix: add rate
   limiting per IP/email (e.g. `slowapi`) and/or temporary lockout after N
   failed attempts.

Questions from the assignment, answered briefly:

- **What if the JWT never expired?** a stolen/leaked token would stay valid
  forever — there would be no way to "log out" a user without rotating the
  `SECRET_KEY` (which would invalidate everyone's tokens at once).
- **What if `/users/me` returned the password?** even hashed, it would
  expose the hash to any authenticated user trying to crack it offline —
  that's why `UserOut` doesn't have that field.
- **What if a USER could call `DELETE /users/:id`?** any regular user could
  delete anyone else's account, including admins — that's why this route
  depends on `require_admin`.