from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)

STUDENTS = []

@app.route("/students", methods = ["POST"])
def create_student():
    body = request.get_json(silent = True) or {}
    name = body.get("name")
    if not name:
        return jsonify({"error": "Tên là bắt buộc"}), 400
    student = {
        "id": str(uuid4()),
        "name": name,
        "gpa": body.get("gpa", 0.0)
    }
    STUDENTS.append(student)
    return jsonify({"id": student["id"], "name": student["name"]}), 201

@app.route("/health", methods = ["GET"])
def health():
    return jsonify({"status": "ok"}), 201 

@app.route("/echo", methods = ["POST"])
def echo():
    data = request.get_json(silent = True) or {} 
    ## silent = True --> nhập đúng định dạng json mới chấp nhận
    return jsonify({"you sent": data}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
