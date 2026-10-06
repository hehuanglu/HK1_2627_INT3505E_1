import base64
import binascii
import json

from flask import Flask, jsonify, request, abort
from data import Post, db
from error import ApiProblem

app = Flask(__name__)

# SQLite lưu file này trong thư mục instance/ của ứng dụng.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts_cursor.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.errorhandler(ApiProblem)
def handle_api_problem(error):
    return error.get_response()


@app.route("/posts", methods=["GET"])
@app.route("/api/v1/posts", methods=["GET"])
def get_posts():
    # 1. Đọc và kiểm tra các tham số trước khi truy vấn database.
    def bad_request(detail):
        raise ApiProblem(400, "Invalid query parameter", detail,
                         type_path="invalid-query")

    try:
        limit = int(request.args.get("limit", "5"))
        author_id = request.args.get("author_id")
        author_id = int(author_id) if author_id is not None else None
    except ValueError:
        bad_request("limit và author_id phải là số nguyên.")

    if not 1 <= limit <= 100:
        bad_request("limit phải nằm trong khoảng 1 đến 100.")
    if author_id is not None and author_id <= 0:
        bad_request("author_id phải lớn hơn 0.")

    status = request.args.get("status")
    if status is not None and status not in ("draft", "published"):
        bad_request("status chỉ nhận draft hoặc published.")

    # Mức cơ bản: sort=id (tăng dần) hoặc sort=-id (giảm dần).
    sort = request.args.get("sort", "id")
    if sort not in ("id", "-id"):
        bad_request("sort chỉ nhận id hoặc -id.")

    allowed_fields = ["id", "title", "content", "status", "author_id"]
    fields_text = request.args.get("fields")
    fields = fields_text.split(",") if fields_text is not None else allowed_fields
    if any(field not in allowed_fields for field in fields):
        bad_request("fields chỉ nhận: " + ", ".join(allowed_fields))

    # 2. Cursor là JSON được mã hóa Base64 URL-safe, chứa ID cuối trang
    # và điều kiện truy vấn. Base64 chỉ là mã hóa biểu diễn, không phải mã hóa bảo mật.
    context = {"sort": sort, "status": status, "author_id": author_id}
    cursor = request.args.get("cursor")
    last_id = None
    if cursor is not None:
        try:
            decoded = base64.b64decode(cursor, altchars=b"-_", validate=True)
            payload = json.loads(decoded)
            if not isinstance(payload, dict):
                raise ValueError
            last_id = payload.get("id")
            # type(...) kiểm tra cả trường hợp JSON true bị coi như số 1.
            if type(last_id) is not int or last_id <= 0:
                raise ValueError
            if payload != {"id": last_id, **context}:
                raise ValueError
        except (ValueError, TypeError, UnicodeDecodeError, binascii.Error):
            bad_request("Cursor hỏng hoặc không khớp sort/status/author_id.")

    # 3. Filter và phân trang ngay trong SQL, không tải toàn bộ bảng.
    query = Post.query
    if status is not None:
        query = query.filter(Post.status == status)
    if author_id is not None:
        query = query.filter(Post.author_id == author_id)

    if sort == "id":
        if last_id is not None:
            query = query.filter(Post.id > last_id)
        query = query.order_by(Post.id.asc())
    else:
        if last_id is not None:
            query = query.filter(Post.id < last_id)
        query = query.order_by(Post.id.desc())

    # Lấy thêm 1 dòng để biết còn trang sau hay không; không dùng OFFSET.
    rows = query.limit(limit + 1).all()
    has_more = len(rows) > limit
    posts = rows[:limit]
    next_cursor = None
    if has_more:
        payload = {"id": posts[-1].id, **context}
        next_cursor = base64.urlsafe_b64encode(
            json.dumps(payload).encode("utf-8")
        ).decode("ascii")

    # 4. Sparse fieldsets: mỗi bài chỉ trả những trường client yêu cầu.
    # Cursor vẫn lấy ID từ model, kể cả khi fields không có id.
    data = []
    for post in posts:
        full_post = post.to_dict()
        data.append({field: full_post[field] for field in fields})

    return jsonify({
        "data": data,
        "pagination": {
            "limit": limit,
            "has_more": has_more,
            "next_cursor": next_cursor,
        },
    })


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
