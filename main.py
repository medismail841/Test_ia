import hashlib
import hmac
import os
import secrets
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from functools import wraps
from pathlib import Path

import jwt
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
DB_PATH = BASE_DIR / "users.db"

# JWT signing key. Generate a random one per process unless one is supplied
# through the environment so that no secret is committed to the repository.
SECRET_KEY = os.environ.get("JWT_SECRET") or secrets.token_hex(32)
JWT_ALGORITHM = "HS256"
TOKEN_TTL_HOURS = 12
TOKEN_COOKIE_NAME = "access_token"

_PBKDF2_ITERATIONS = 100_000


def _get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                hashed_password TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, _PBKDF2_ITERATIONS
    )
    return "pbkdf2_sha256${}${}${}".format(
        _PBKDF2_ITERATIONS, salt.hex(), digest.hex()
    )


def verify_password(password: str, stored: str) -> bool:
    try:
        _, iterations, salt_hex, digest_hex = stored.split("$")
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations),
        )
        return hmac.compare_digest(digest.hex(), digest_hex)
    except ValueError:
        return False


def create_token(username: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "iat": now,
        "exp": now + timedelta(hours=TOKEN_TTL_HOURS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload.get("sub")
    except jwt.PyJWTError:
        return None


def get_authenticated_user(request: Request) -> str | None:
    token = request.cookies.get(TOKEN_COOKIE_NAME)
    if not token:
        return None
    return decode_token(token)


def require_login(redirect_url: str = "/"):
    def decorator(func):
        @wraps(func)
        def wrapper(request: Request, *args, **kwargs):
            username = get_authenticated_user(request)
            if username is None:
                return RedirectResponse(url=redirect_url, status_code=302)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


app = FastAPI(title="Calculator App")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

init_db()


class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=6, max_length=128)


def _set_auth_cookie(response: Response, username: str) -> None:
    response.set_cookie(
        key=TOKEN_COOKIE_NAME,
        value=create_token(username),
        httponly=True,
        secure=False,  # use True when served over HTTPS in production
        samesite="lax",
        max_age=TOKEN_TTL_HOURS * 3600,
        path="/",
    )


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/register", status_code=201)
def register(body: Credentials, response: Response):
    username = body.username.strip()
    password = body.password
    if not username:
        raise HTTPException(status_code=400, detail="Username cannot be empty.")

    with _get_db() as conn:
        existing = conn.execute(
            "SELECT 1 FROM users WHERE username = ?", (username,)
        ).fetchone()
        if existing:
            raise HTTPException(status_code=409, detail="Username already exists.")

        conn.execute(
            "INSERT INTO users (username, hashed_password, created_at) VALUES (?, ?, ?)",
            (
                username,
                hash_password(password),
                datetime.now(timezone.utc).isoformat(),
            ),
        )

    _set_auth_cookie(response, username)
    return {"message": "Registration successful.", "username": username}


@app.post("/login")
def login(body: Credentials, response: Response):
    username = body.username.strip()
    with _get_db() as conn:
        row = conn.execute(
            "SELECT hashed_password FROM users WHERE username = ?", (username,)
        ).fetchone()

    valid = row is not None and verify_password(body.password, row["hashed_password"])
    if not valid:
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    _set_auth_cookie(response, username)
    return {"message": "Login successful.", "username": username}


@app.post("/auth")
def auth(body: Credentials, response: Response):
    username = body.username.strip()
    with _get_db() as conn:
        row = conn.execute(
            "SELECT hashed_password FROM users WHERE username = ?", (username,)
        ).fetchone()

    valid = row is not None and verify_password(body.password, row["hashed_password"])
    if not valid:
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    _set_auth_cookie(response, username)
    return {"message": "Authentication successful.", "username": username}


@app.post("/logout")
def logout(response: Response):
    response.delete_cookie(key=TOKEN_COOKIE_NAME, path="/")
    return {"message": "Logged out."}


@app.get("/auth/check")
def auth_check(request: Request):
    username = get_authenticated_user(request)
    if username is None:
        return JSONResponse({"authenticated": False}, status_code=200)
    return {"authenticated": True, "username": username}


@app.get("/calculator")
@require_login()
def calculator(request: Request):
    return FileResponse(STATIC_DIR / "index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)