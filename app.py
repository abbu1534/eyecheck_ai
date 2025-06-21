from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/eyecheck', methods=['POST'])
def eyecheck():
    return jsonify({
        "status": "success",
        "message": "EyeCheck API is working!"
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
