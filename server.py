from flask import Flask, request, jsonify
import sys
import os

# Add the project root to the Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from run_cycle import run_gim, run_rem

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/run-cycle', methods=['POST'])
def run_cycle_endpoint():
    data = request.get_json()
    cycle = data.get('cycle', '').strip().lower()

    handlers = {
        "gim": run_gim,
        "rem": run_rem,
    }

    if cycle not in handlers:
        return jsonify({
            "success": False,
            "message": "Invalid cycle specified. Must be 'gim' or 'rem'.",
        }), 400

    try:
        payload = handlers[cycle]()
        return jsonify(payload), 200 if payload.get("success") else 500
    except Exception as error:
        return jsonify({
            "success": False,
            "cycle": cycle,
            "message": str(error),
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
