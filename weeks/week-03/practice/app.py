from flask import Flask, jsonify, request, abort
from data import POSTS

app = Flask(__name__)


@app.route("/api/v1/posts", methods=["GET"])
def get_posts():
    return jsonify(POSTS)


@app.route("/api/v1/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = next((p for p in POSTS if p["id"] == post_id), None)
    if not post:
        abort(404)
    return jsonify(post)


@app.route("/api/v1/posts", methods=["POST"])
def create_post():
    body = request.get_json(force=True)
    new_id = max(p["id"] for p in POSTS) + 1 if POSTS else 1
    post = {"id": new_id, "title": body["title"], "content": body["content"]}
    POSTS.append(post)
    return jsonify(post), 201


@app.route("/api/v1/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = next((p for p in POSTS if p["id"] == post_id), None)
    if not post:
        abort(404)
    POSTS.remove(post)
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
