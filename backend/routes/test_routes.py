from flask import Blueprint, request, jsonify
from backend.config.settings import settings
from backend.services.firebase_service import (
    get_collection_docs,
    get_doc,
    query_docs,
    create_doc
)
from backend.utils.token_validator import require_auth

bp = Blueprint("tests", __name__, url_prefix="/api/tests")

@bp.route("/", methods=["GET"])
def list_tests():
    """
    GET /api/tests
    Query params:
      - company_id
      - domain_id
      - test_type
    """
    company_id = request.args.get("company_id")
    domain_id = request.args.get("domain_id")
    test_type = request.args.get("test_type")

    # Build simple filtering
    if company_id:
        results = query_docs(settings.COLLECTION_TESTS, where=("company_id", "==", company_id))
    elif domain_id:
        results = query_docs(settings.COLLECTION_TESTS, where=("domain_id", "==", domain_id))
    elif test_type:
        results = query_docs(settings.COLLECTION_TESTS, where=("test_type", "==", test_type))
    else:
        results = get_collection_docs(settings.COLLECTION_TESTS)

    return jsonify(results), 200

@bp.route("/<test_id>", methods=["GET"])
def get_test(test_id):
    """
    GET /api/tests/<test_id>
    """
    test = get_doc(settings.COLLECTION_TESTS, test_id)
    if not test:
        return jsonify({"error": "test not found"}), 404
    return jsonify(test), 200

@bp.route("/", methods=["POST"])
@require_auth
def create_test():
    """
    POST /api/tests
    Body: test payload
    """
    payload = request.json or {}
    if not payload.get("company_id") or not payload.get("test_type"):
        return jsonify({"error": "company_id and test_type required"}), 400
    test_id = payload.get("test_id")
    doc = create_doc(settings.COLLECTION_TESTS, test_id, payload)
    return jsonify(doc), 201
