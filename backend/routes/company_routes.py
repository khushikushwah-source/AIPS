from flask import Blueprint, request, jsonify
from backend.config.settings import settings
from backend.services.firebase_service import (
    get_collection_docs,
    get_doc,
    create_doc,
    query_docs
)
from backend.utils.token_validator import require_auth

bp = Blueprint("companies", __name__, url_prefix="/api/companies")

@bp.route("/", methods=["GET"])
def list_companies():
    """
    GET /api/companies
    Optional query: ?domain_id=...
    """
    domain_id = request.args.get("domain_id")
    if domain_id:
        results = query_docs(
            settings.COLLECTION_COMPANIES,
            where=("domain_ids", "array_contains", domain_id)
        )
    else:
        results = get_collection_docs(settings.COLLECTION_COMPANIES)
    return jsonify(results), 200

@bp.route("/<company_id>", methods=["GET"])
def get_company(company_id):
    """
    GET /api/companies/<company_id>
    """
    doc = get_doc(settings.COLLECTION_COMPANIES, company_id)
    if not doc:
        return jsonify({"error": "company not found"}), 404
    return jsonify(doc), 200

@bp.route("/", methods=["POST"])
@require_auth
def create_company():
    """
    POST /api/companies
    Body: { company_id?, name, domain_ids, hiring_flow, logo_url }
    """
    payload = request.json or {}
    if not payload.get("name"):
        return jsonify({"error": "name is required"}), 400
    company_id = payload.get("company_id")
    doc = create_doc(settings.COLLECTION_COMPANIES, company_id, payload)
    return jsonify(doc), 201
