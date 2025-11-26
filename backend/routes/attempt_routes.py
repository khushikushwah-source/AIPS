from flask import Blueprint, request, jsonify
from uuid import uuid4
from datetime import datetime
from backend.config.settings import settings
from backend.services.firebase_service import (
    get_doc,
    create_doc,
    save_attempt,
    get_attempts_by_user
)
from backend.services.ai_service import score_answers  # simple scoring helper
from backend.utils.token_validator import require_auth, get_request_user

bp = Blueprint("attempts", __name__, url_prefix="/api/attempts")

@bp.route("/start", methods=["POST"])
@require_auth
def start_attempt():
    """
    POST /api/attempts/start
    Body: { test_id }
    Returns: { attempt_id, test, started_at, questions (if included) }
    """
    user = get_request_user()
    payload = request.json or {}
    test_id = payload.get("test_id")
    if not test_id:
        return jsonify({"error": "test_id required"}), 400

    attempt_id = str(uuid4())
    started_at = datetime.utcnow().isoformat()
    attempt = {
        "attempt_id": attempt_id,
        "user_id": user.get("uid"),
        "test_id": test_id,
        "started_at": started_at,
        "answers": [],
        "score": None
    }
    # Persist minimal attempt (backend/service will create document)
    save_attempt(attempt_id, attempt)
    # Optionally return test doc and question IDs; frontend can fetch test separately
    test_doc = get_doc(settings.COLLECTION_TESTS, test_id)
    return jsonify({"attempt_id": attempt_id, "started_at": started_at, "test": test_doc}), 201

@bp.route("/submit", methods=["POST"])
@require_auth
def submit_attempt():
    """
    POST /api/attempts/submit
    Body: { attempt_id, answers: [{question_id, response}], media_urls? }
    """
    user = get_request_user()
    payload = request.json or {}
    attempt_id = payload.get("attempt_id")
    answers = payload.get("answers", [])
    media_urls = payload.get("media_urls", [])

    if not attempt_id or not isinstance(answers, list):
        return jsonify({"error": "attempt_id and answers[] required"}), 400

    # Load existing attempt (optional validation)
    # For simplicity, assume attempt exists
    # Score answers (delegates to AI / scoring service)
    score_details = score_answers(answers)  # returns {score: int, per_question: [...]}
    finished_at = datetime.utcnow().isoformat()

    # Build attempt doc update
    attempt_doc = {
        "attempt_id": attempt_id,
        "finished_at": finished_at,
        "answers": score_details.get("per_question", answers),
        "score": score_details.get("score"),
        "media_urls": media_urls
    }

    # Save final attempt
    save_attempt(attempt_id, attempt_doc, merge=True)
    return jsonify({"attempt_id": attempt_id, "score": score_details.get("score")}), 200

@bp.route("/user/<user_id>", methods=["GET"])
@require_auth
def user_attempts(user_id):
    """
    GET /api/attempts/user/<user_id>
    Returns attempts for a given user (admins can query others)
    """
    requester = get_request_user()
    # allow if requester.uid == user_id OR requester is admin (admin check is left to firebase_service or token)
    if requester.get("uid") != user_id and not requester.get("is_admin", False):
        return jsonify({"error": "forbidden"}), 403

    attempts = get_attempts_by_user(user_id)
    return jsonify(attempts), 200
