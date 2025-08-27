from flask import Blueprint, request, jsonify
import subprocess, os

sync_bp = Blueprint("sync", __name__)

@sync_bp.route("/execute-sync", methods=["POST"])
def execute_sync():
    data = request.json
    device_ip = data.get("device_ip")
    device_port = data.get("device_port")

    if not device_ip or not device_port:
        return jsonify({"error": "Parámetros inválidos"}), 400

    exe_path = os.path.join(os.getcwd(), "ZKTeco-Sync.exe")
    subprocess.Popen([exe_path, "--ip", device_ip, "--port", str(device_port)])
    return jsonify({"status": "sync started"}), 200
