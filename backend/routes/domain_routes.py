from flask import Blueprint, request, jsonify, current_app
from backend.config.settings import settings
from backend.services.firebase_service import (
    get_collection_docs,
    get_doc,
    create_doc
)
from backend.utils.token_validator import require_auth

bp = Blueprint("domains", __name__, url_prefix="/api/domains")

@bp.route("/", methods=["GET"])
def list_domains():
    """
    GET /api/domains/
    Optional query params: ?limit=20
    """
    limit = request.args.get("limit", None)
    docs = get_collection_docs(settings.COLLECTION_DOMAINS, limit=limit)
    return jsonify(docs), 200

@bp.route("/<domain_id>", methods=["GET"])
def get_domain(domain_id):
    """
    GET /api/domains/<domain_id>
    """
    doc = get_doc(settings.COLLECTION_DOMAINS, domain_id)
    if not doc:
        return jsonify({"error": "domain not found"}), 404
    return jsonify(doc), 200

@bp.route("/", methods=["POST"])
@require_auth  # only authenticated users (or admins) should create
def create_domain():
    """
    POST /api/domains/
    Body: { "domain_id": "...", "name": "...", "description": "...", "tags": [...] }
    """
    payload = request.json or {}
    if not payload.get("name"):
        return jsonify({"error": "name is required"}), 400

    domain_id = payload.get("domain_id")
    doc = create_doc(settings.COLLECTION_DOMAINS, domain_id, payload)
    return jsonify(doc), 201
