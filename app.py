from flask import Flask, request, jsonify, make_response
import os
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
API_KEY = os.environ.get("EYE_API_KEY", "c20847490727ab12a256d33888ab738b")

@app.route('/api/eyecheck', methods=['POST'])
def eyecheck():
    # API key validation
    received_key = request.headers.get('X-API-KEY')
    if received_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    image_b64 = data.get('image')
    if not image_b64:
        return jsonify({"error": "No image provided"}), 400

    try:
        # Decode base64 image to OpenCV image
        image_data = base64.b64decode(image_b64)
        image = Image.open(BytesIO(image_data)).convert("RGB")
        image_np = np.array(image)
        image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Convert to HSV for red detection
        hsv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2HSV)

        # Redness detection (HSV range for red)
        lower_red1 = np.array([0, 70, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 70, 50])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = mask1 + mask2

        red_pixels = np.sum(red_mask > 0)
        total_pixels = red_mask.shape[0] * red_mask.shape[1]
        redness_ratio = red_pixels / total_pixels

        # If more than 3% pixels are red, mark as red eyes
        eye_redness = redness_ratio > 0.03
        fatigue = redness_ratio > 0.05

        result = {
            "status": "success",
            "data": {
                "eye_redness": eye_redness,
                "fatigue_detected": fatigue,
                "suggestion": "Take a short break and wash your eyes with cold water." if fatigue else "Eyes look okay."
            }
        }

        response = make_response(jsonify(result))
        response.headers['Content-Length'] = str(len(response.get_data()))
        return response

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
