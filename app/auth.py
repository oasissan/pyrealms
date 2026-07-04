"""Optional HTTP Basic Auth gate for public deployments.

No-op when APP_USERNAME/APP_PASSWORD aren't set (local dev is unaffected).
Set both env vars once the app is reachable over the internet, since the
grader executes submitted code unsandboxed — see README's deployment note.
"""

import base64
import os
import secrets

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class BasicAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        username = os.environ.get("APP_USERNAME")
        password = os.environ.get("APP_PASSWORD")
        if not username or not password:
            return await call_next(request)

        header = request.headers.get("Authorization", "")
        if header.startswith("Basic "):
            try:
                decoded = base64.b64decode(header[6:]).decode()
                given_user, _, given_pass = decoded.partition(":")
            except Exception:
                given_user, given_pass = "", ""
            if secrets.compare_digest(given_user, username) and secrets.compare_digest(
                given_pass, password
            ):
                return await call_next(request)

        return Response(
            status_code=401,
            headers={"WWW-Authenticate": 'Basic realm="Python Zero-to-Hero"'},
        )
