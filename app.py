from flask import Flask, request, jsonify, make_response
import os

app = Flask(__name__)
API_KEY = os.environ.get("EYE_API_KEY", "c20847490727ab12a256d33888ab738b")

@app.route('/api/eyecheck', methods=['POST'])
def eyecheck():
    received_key = request.headers.get('X-API-KEY')
    if received_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    image_data = data.get('image')

    if not image_data:
        return jsonify({"error": "No image provided"}), 400

    # Dummy AI result
    result = {
        "status": "success",
        "data": {
            "fatigue_detected": True,
            "eye_redness": False,
            "suggestion": "Take a short break from screen."
        }
    }

    # ✅ The most critical fix here:
    response = make_response(jsonify(result))
    response_data = response.get_data()
    response.headers["Content-Type"] = "application/json"
    response.headers["Content-Length"] = str(len(response_data))
    return response
