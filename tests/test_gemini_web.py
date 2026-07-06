"""Tests for the Gemini web client's session-rotation handling.

Google rotates the ``__Secure-1PSIDTS`` cookie frequently; the stored
snapshot goes stale and StreamGenerate starts returning 401. The client must
retry once (the token-scrape GET refreshes the cookie jar), surface a
friendly error instead of the raw response blob when auth truly fails, and
expose the rotated cookie so the app can persist it.

All HTTP is faked with httpx.MockTransport — no real Gemini traffic.
"""

import json

import httpx
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.services.gemini_web import GeminiAuthError, GeminiWebClient

TOKENS_HTML = '"SNlM0e":"AT_TOKEN","cfb2h":"BL_TOKEN","FdrFJe":"SID_TOKEN"'
RAW_401_BLOB = ")]}'\n105\n[[\"er\",null,null,null,null,401,null,null,null,16]]"


def _stream_body(reply="Hello!", conv="c_1", msg="r_1"):
    inner = [None, [conv, msg], None, None, [[None, [reply]]]]
    return json.dumps([["wrb.fr", None, json.dumps(inner)]])


class FakeGemini:
    """MockTransport handler standing in for gemini.google.com."""

    def __init__(self, post_statuses=(200,), rotate_to="ROTATED_TS"):
        self.post_statuses = post_statuses
        self.rotate_to = rotate_to
        self.post_calls = 0

    @property
    def transport(self):
        return httpx.MockTransport(self.handler)

    def handler(self, request):
        if request.method == "GET":
            headers = {}
            if self.rotate_to:
                headers["set-cookie"] = (
                    f"__Secure-1PSIDTS={self.rotate_to}; "
                    "Domain=.google.com; Path=/; Secure"
                )
            return httpx.Response(200, text=TOKENS_HTML, headers=headers)
        self.post_calls += 1
        status = self.post_statuses[
            min(self.post_calls - 1, len(self.post_statuses) - 1)
        ]
        if status != 200:
            return httpx.Response(status, text=RAW_401_BLOB)
        return httpx.Response(200, text=_stream_body())


def _client(fake: FakeGemini) -> GeminiWebClient:
    return GeminiWebClient("PSID_VALUE", "OLD_TS", transport=fake.transport)


def test_retries_once_after_401_and_succeeds():
    fake = FakeGemini(post_statuses=(401, 200))
    reply, conv_id, msg_id = _client(fake).send_message("hi")
    assert reply == "Hello!"
    assert conv_id == "c_1"
    assert msg_id == "r_1"
    assert fake.post_calls == 2


def test_raises_friendly_auth_error_when_401_persists():
    fake = FakeGemini(post_statuses=(401, 401))
    with pytest.raises(GeminiAuthError) as excinfo:
        _client(fake).send_message("hi")
    assert fake.post_calls == 2  # retried exactly once
    message = str(excinfo.value)
    assert "session" in message.lower()
    assert "[[" not in message  # no raw protobuf blob leaking to the UI


def test_current_psidts_picks_up_rotated_cookie():
    fake = FakeGemini()
    client = _client(fake)
    client.send_message("hi")
    assert client.current_psidts == "ROTATED_TS"


def test_current_psidts_without_rotation_returns_original():
    fake = FakeGemini(rotate_to=None)
    client = _client(fake)
    client.send_message("hi")
    assert client.current_psidts == "OLD_TS"


# --- Router integration: persistence + friendly HTTP error ------------------


@pytest.fixture()
def api(monkeypatch):
    """TestClient with an in-memory DB seeded with stale Gemini cookies.

    Yields (test_client, session_factory, fake) — the fake is swappable per
    test via fake.post_statuses. Lifespan is deliberately not run, so the
    real app.db is never touched.
    """
    from app.database import Base, get_db
    from app.main import app
    from app.models import Settings
    from app.routers import chatbot

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine, expire_on_commit=False)
    with TestingSession() as db:
        db.add(Settings(gemini_session_cookie="PSID_VALUE", gemini_cookie_ts="OLD_TS"))
        db.commit()

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    fake = FakeGemini()
    monkeypatch.setattr(
        chatbot,
        "GeminiWebClient",
        lambda **kwargs: GeminiWebClient(transport=fake.transport, **kwargs),
    )
    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app), TestingSession, fake
    finally:
        app.dependency_overrides.pop(get_db, None)


def test_message_endpoint_persists_rotated_cookie(api):
    from app.models import Settings

    client, TestingSession, fake = api
    resp = client.post("/api/chatbot/message", json={"message": "hi"})
    assert resp.status_code == 200
    assert resp.json()["reply"] == "Hello!"
    with TestingSession() as db:
        settings = db.execute(select(Settings)).scalar_one()
        assert settings.gemini_cookie_ts == "ROTATED_TS"


def test_message_endpoint_returns_friendly_401(api):
    client, _, fake = api
    fake.post_statuses = (401, 401)
    resp = client.post("/api/chatbot/message", json={"message": "hi"})
    assert resp.status_code == 401
    detail = resp.json()["detail"]
    assert "session" in detail.lower()
    assert "[[" not in detail
