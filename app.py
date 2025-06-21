from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/eyecheck', methods=['POST'])
def eyecheck():
    data = request.get_json()
    image_data = data.get('image')

    if not image_data:
        return jsonify({"error": "No image provided"}), 400

    # 👉 Dummy fixed response
    result = {
        "fatigue_detected": True,
        "eye_redness": False,
        "suggestion": "Take a short break from screen use every 20 minutes."
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
