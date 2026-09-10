from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health", method = ["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/echo", method = ["POST"])
def echo():
    data = request.get_json(slient = True) or {} 
    ## silent = True --> nhập đúng định dạng json mới chấp nhận
    return jsonify({"you sent": data}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

## request: curl -X POST http://127.0.0.1:5000/echo \-H "Content-Type: application/json" \-d '{"name": "An", "age": "21"}'
