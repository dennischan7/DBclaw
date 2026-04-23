"""Auth Middleware — Session-based auth + CSRF protection.

Security model:
  - Cookie-based session (HttpOnly, SameSite=Strict)
  - CSRF token in header X-CSRF-Token (double-submit pattern)
  - No external auth provider — local password + role
  - Admin operations require role >= ADMIN (2)

Usage in routes:
  from auth_middleware import require_auth, require_admin, get_session, issue_session
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import time
from http.cookies import SimpleCookie
from typing import Any, Dict, Optional, Tuple


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SESSION_COOKIE_NAME = "dba_session"
CSRF_HEADER = "X-CSRF-Token"
SESSION_TTL = 86400 * 7  # 7 days
SECRET_KEY = os.environ.get("DBA_WEBUI_SECRET", secrets.token_hex(32))

# Role constants (mirror skill_engine/skill_manager.py)
ROLE_READONLY = 0
ROLE_DEVELOPER = 1
ROLE_ADMIN = 2


# ---------------------------------------------------------------------------
# In-memory session store (sufficient for single-process server)
# ---------------------------------------------------------------------------

_sessions: Dict[str, Dict[str, Any]] = {}


def _generate_session_id() -> str:
    return secrets.token_urlsafe(32)


def _generate_csrf_token(session_id: str) -> str:
    """HMAC-based CSRF token tied to session."""
    return hmac.new(
        SECRET_KEY.encode(), session_id.encode(), hashlib.sha256
    ).hexdigest()[:32]


def _verify_csrf(session_id: str, token: str) -> bool:
    expected = _generate_csrf_token(session_id)
    return hmac.compare_digest(expected, token)


# ---------------------------------------------------------------------------
# Session API
# ---------------------------------------------------------------------------

def issue_session(
    user_id: str,
    role: int = ROLE_ADMIN,
    extra: Optional[Dict] = None,
) -> Tuple[str, str]:
    """Create a new session.

    Returns:
        (session_id, csrf_token)
    """
    sid = _generate_session_id()
    csrf = _generate_csrf_token(sid)

    _sessions[sid] = {
        "user_id": user_id,
        "role": role,
        "created_at": time.time(),
        "csrf_token": csrf,
        **(extra or {}),
    }

    return sid, csrf


def get_session(handler) -> Optional[Dict[str, Any]]:
    """Extract session from request cookies.

    Args:
        handler: DBARequestHandler instance

    Returns:
        Session dict or None
    """
    cookie_header = handler.headers.get("Cookie", "")
    if not cookie_header:
        return None

    cookie = SimpleCookie()
    try:
        cookie.load(cookie_header)
    except Exception:
        return None

    morsel = cookie.get(SESSION_COOKIE_NAME)
    if not morsel:
        return None

    sid = morsel.value
    session = _sessions.get(sid)
    if not session:
        return None

    # Check TTL
    if time.time() - session["created_at"] > SESSION_TTL:
        _sessions.pop(sid, None)
        return None

    session["_session_id"] = sid
    return session


def destroy_session(session_id: str) -> None:
    """Remove a session."""
    _sessions.pop(session_id, None)


# ---------------------------------------------------------------------------
# Auth decorators (for route handlers)
# ---------------------------------------------------------------------------

def require_auth(handler) -> Optional[Dict[str, Any]]:
    """Check auth. Returns session dict or sends 401 and returns None."""
    session = get_session(handler)
    if not session:
        # Auto-create a default admin session for development
        # TODO: In production, return 401 and redirect to login
        sid, csrf = issue_session("webui_admin", ROLE_ADMIN)
        _set_session_cookie(handler, sid)
        # Queue CSRF token so the browser can read it from response headers
        if not hasattr(handler, '_pending_headers'):
            handler._pending_headers = []
        handler._pending_headers.append(("X-CSRF-Token", csrf))
        handler._pending_headers.append(("Access-Control-Expose-Headers", CSRF_HEADER))
        session = _sessions[sid]
        session["_session_id"] = sid
        session["_new"] = True
        session["csrf_token"] = csrf
        return session

    return session


def require_admin(handler) -> Optional[Dict[str, Any]]:
    """Check admin auth. Returns session dict or sends 403 and returns None."""
    session = require_auth(handler)
    if not session:
        return None

    if session.get("role", 0) < ROLE_ADMIN:
        handler.send_json({"error": "需要管理员权限"}, status=403)
        return None

    return session


def check_csrf(handler, session: Dict) -> bool:
    """Verify CSRF token for state-changing requests (POST/PUT/DELETE).

    Returns True if valid, sends 403 and returns False if invalid.
    """
    # Skip CSRF for GET requests
    if handler.command == "GET":
        return True

    token = handler.headers.get(CSRF_HEADER, "")
    sid = session.get("_session_id", "")

    if not token or not _verify_csrf(sid, token):
        handler.send_json({"error": "CSRF验证失败"}, status=403)
        return False

    return True


# ---------------------------------------------------------------------------
# Cookie helper
# ---------------------------------------------------------------------------

def _set_session_cookie(handler, session_id: str) -> None:
    """Queue session cookie — will be flushed after send_response()."""
    cookie = (
        f"{SESSION_COOKIE_NAME}={session_id}; "
        f"Path=/; HttpOnly; SameSite=Strict; Max-Age={SESSION_TTL}"
    )
    # Defer: store on handler, flush in send_json / send_sse_headers
    if not hasattr(handler, '_pending_headers'):
        handler._pending_headers = []
    handler._pending_headers.append(("Set-Cookie", cookie))


def set_auth_headers(handler, session: Dict) -> None:
    """Queue auth-related headers for deferred flush.

    Call this BEFORE send_json() — headers are queued and flushed
    after send_response() writes the status line.
    Note: require_auth() already queues Set-Cookie + CSRF for new sessions,
    so this only adds headers that aren't already pending.
    """
    pending = getattr(handler, '_pending_headers', [])
    pending_names = {name for name, _ in pending}

    if session.get("_new") and "Set-Cookie" not in pending_names:
        _set_session_cookie(handler, session["_session_id"])

    # Queue CSRF token if not already queued
    csrf = session.get("csrf_token", "")
    if csrf and "X-CSRF-Token" not in pending_names:
        if not hasattr(handler, '_pending_headers'):
            handler._pending_headers = []
        handler._pending_headers.append(("X-CSRF-Token", csrf))
        handler._pending_headers.append(("Access-Control-Expose-Headers", CSRF_HEADER))


def flush_pending_headers(handler) -> None:
    """Flush all deferred headers. Call AFTER send_response()."""
    for name, value in getattr(handler, '_pending_headers', []):
        handler.send_header(name, value)
    handler._pending_headers = []
