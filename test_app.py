import tempfile
from pathlib import Path

import main
from fastapi.testclient import TestClient

main.DB_PATH = Path(tempfile.gettempdir()) / "test_users.db"
if main.DB_PATH.exists():
    main.DB_PATH.unlink()
main.init_db()

client = TestClient(main.app)

WAIT = main.TOKEN_COOKIE_NAME


def _register(username="alice", password="secret123"):
    return client.post("/register", json={"username": username, "password": password})


def _login(username="alice", password="secret123"):
    return client.post("/login", json={"username": username, "password": password})


def test_register_returns_token_cookie():
    res = _register()
    assert res.status_code == 201
    assert WAIT in res.cookies
    assert res.cookies[WAIT] != ""


def test_register_stores_hashed_password():
    _register("bob", "hunter22")
    import sqlite3

    conn = sqlite3.connect(main.DB_PATH)
    row = conn.execute(
        "SELECT hashed_password FROM users WHERE username = 'bob'"
    ).fetchone()
    conn.close()
    assert row is not None
    stored = row[0]
    assert stored != "hunter22"
    assert stored.startswith("pbkdf2_sha256$")
    assert "hunter22" not in stored


def test_duplicate_username_rejected():
    _register("carol", "secret123")
    res = _register("carol", "otherpass123")
    assert res.status_code == 409


def test_login_with_valid_credentials():
    _register("dave", "secret123")
    res = _login("dave", "secret123")
    assert res.status_code == 200
    assert res.json()["username"] == "dave"
    assert res.cookies[WAIT] != ""


def test_login_with_invalid_credentials_denied():
    _register("erin", "secret123")
    res = _login("erin", "wrongpass")
    assert res.status_code == 401
    assert WAIT not in res.cookies


def test_calculator_redirects_when_not_authenticated():
    anonymous = TestClient(main.app)
    res = anonymous.get("/calculator", follow_redirects=False)
    assert res.status_code in (301, 302, 307, 308)
    assert res.headers["location"] == "/"


def test_calculator_accessible_when_authenticated():
    _register("frank", "secret123")
    res = _login("frank", "secret123")
    assert res.status_code == 200

    client2 = TestClient(main.app)
    client2.cookies.set(WAIT, res.cookies[WAIT])
    page = client2.get("/calculator")
    assert page.status_code == 200
    assert "Calculator" in page.text


def test_auth_check_endpoint():
    anonymous = TestClient(main.app)
    anon = anonymous.get("/auth/check")
    assert anon.status_code == 200
    assert anon.json() == {"authenticated": False}

    res = _register("grace", "secret123")
    logged = client.get("/auth/check")
    assert logged.status_code == 200
    assert logged.json()["authenticated"] is True
    assert logged.json()["username"] == "grace"


def test_logout_clears_session():
    _register("heidi", "secret123")
    res = client.post("/logout")
    assert res.status_code == 200
    assert client.get("/auth/check").json()["authenticated"] is False


def test_root_serves_frontend():
    res = client.get("/")
    assert res.status_code == 200
    assert "calculator" in res.text.lower()