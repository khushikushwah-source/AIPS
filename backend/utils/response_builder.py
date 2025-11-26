"""
Utility to build consistent JSON API responses.

Use:
    return success("Created", data={...})
    return error("Invalid request", 400)
"""

from flask import jsonify


def success(message="Success", data=None, status=200):
    """Return a success response with consistent structure."""
    return jsonify({
        "status": "success",
        "message": message,
        "data": data or {}
    }), status


def error(message="Error", status=400, details=None):
    """Return an error response with consistent structure."""
    return jsonify({
        "status": "error",
        "message": message,
        "details": details
    }), status


def paginated(data, page=1, page_size=10, total=None, message="Success"):
    """Return a paginated API response."""
    return jsonify({
        "status": "success",
        "message": message,
        "data": data,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total
        }
    }), 200
