from flask import Blueprint, request, jsonify
from backend.utils.token_validator import verify_token

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@bp.route("/verify", methods=["POST"])
def verify():
    """
    POST /api/auth/verify
    Body: { id_token }
    Returns decoded token claims on success
    """
    payload = request.json or {}
    id_token = payload.get("id_token")
    if not id_token:
        return jsonify({"error": "id_token required"}), 400

    try:
        claims = verify_token(id_token)
        return jsonify({"claims": claims}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401
