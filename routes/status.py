from flask import Blueprint, jsonify

status_bp = Blueprint("status", __name__)

@status_bp.route("/estado", methods=["GET"])
def estado():
    return jsonify({"status": "running"}), 200