from functools import wraps
import logging
from flask import request, jsonify, g
from backend.services.firebase_service import verify_id_token

logger = logging.getLogger(__name__)


def _extract_bearer_token():
    """Extract Bearer <token> from Authorization header or id_token in body."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header.split(" ", 1)[1].strip()

    # fallback (used in simple frontend requests)
    body = request.get_json(silent=True) or {}
    return body.get("id_token") or body.get("token")


def verify_token(id_token: str):
    """Verify Firebase ID token and return decoded claims."""
    if not id_token:
        raise ValueError("missing id_token")
    return verify_id_token(id_token)


def require_auth(fn):
    """Decorator to protect endpoints. Validates Firebase ID token."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = _extract_bearer_token()
        if not token:
            return jsonify({"error": "authorization required"}), 401

        try:
            claims = verify_token(token)
            g.user = {
                "uid": claims.get("uid"),
                "email": claims.get("email"),
                "claims": claims,
                "is_admin": claims.get("role") == "admin" or claims.get("admin", False)
            }
            return fn(*args, **kwargs)
        except Exception as e:
            logger.error("Auth failed: %s", e)
            return jsonify({"error": "invalid or expired token"}), 401

    return wrapper


def get_request_user():
    """Return the currently authenticated user from flask.g."""
    return getattr(g, "user", {})
