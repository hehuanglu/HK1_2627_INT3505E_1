from flask import Flask, jsonify, request, abort
from data import Post, db
from error import ApiProblem

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.errorhandler(ApiProblem)
def handle_api_problem(error):
    return error.get_response()


@app.route("/api/v1/posts", methods=["GET"])
def get_posts():
    return jsonify([post.to_dict() for post in Post.query.all()])


@app.route("/api/v1/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        raise ApiProblem(
            status=404,
            title="Post not found",
            detail="The requested post does not exist.",
            type_path="post-not-found",
            resource_id=post_id,
        )

    return jsonify(post.to_dict())


@app.route("/api/v1/posts", methods=["POST"])
def create_post():
    body = request.get_json(force=True)

    post = Post(
        title=body["title"],
        content=body["content"]
    )

    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_dict()), 201


@app.route("/api/v1/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        abort(404)

    db.session.delete(post)
    db.session.commit()

    return "", 204


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True
    )
