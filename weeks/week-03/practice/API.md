# Blog API – Thiết kế Resource

## Resources

- **users** – người dùng
- **posts** – bài viết
- **comments** – bình luận (sub-resource của post)
- **tags** – thẻ phân loại
- **follows** – quan hệ theo dõi (sub-resource của user)

## Phân loại collection / item / sub-resource

| Loại           | Ví dụ                              | Giải thích                         |
|----------------|-------------------------------------|------------------------------------|
| Collection     | `/posts`, `/users`, `/tags`         | Danh sách, dùng danh từ số nhiều   |
| Item           | `/posts/1`, `/users/2`              | Một phần tử, truy cập qua ID      |
| Sub-resource   | `/posts/1/comments`, `/users/2/following` | Tài nguyên con, thuộc về cha |

## Sơ đồ cây Endpoint

```
/api/v1
├── /users
│   ├── GET, POST
│   └── /{user_id}
│       ├── GET, PUT, DELETE
│       ├── /posts          → GET
│       ├── /followers      → GET
│       └── /following      → GET, POST
│
├── /posts
│   ├── GET, POST
│   └── /{post_id}
│       ├── GET, PUT, DELETE
│       ├── /comments       → GET, POST
│       └── /tags           → GET, POST, DELETE
│
├── /comments/{comment_id}  → GET, PUT, DELETE
│
└── /tags
    ├── GET, POST
    └── /{tag_id}           → GET, PUT, DELETE
```

## Quyết định version segment

Chọn đặt version trong **URL path**: `/api/v1/...`
