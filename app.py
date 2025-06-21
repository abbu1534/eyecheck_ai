from flask import Flask, request, jsonify, make_response
import os

app = Flask(__name__)
API_KEY = os.environ.get("EYE_API_KEY", "c20847490727ab12a256d33888ab738b")

@app.route('/api/eyecheck', methods=['POST'])
def eyecheck():
    received_key = request.headers.get('X-API-KEY')
    if received_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    # Dummy response
    result = {
        "status": "success",
        "data": {
            "fatigue_detected": True,
            "eye_redness": False,
            "suggestion": "Take a short break from screen."
        }
    }

    # ✅ Fix: Add Content-Length manually
    response = make_response(jsonify(result))
    response.headers['Content-Length'] = str(len(response.get_data()))
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
