from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "success",
        "message": "Chào mừng đến với bài thực hành tuần 1 - SOA UET!",
        "service": "Flask API Starter"
    })

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
