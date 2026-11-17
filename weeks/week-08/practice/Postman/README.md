# Lab 3 — Postman / Newman

Collection gồm 5 request CRUD và folder `error-cases` với hai trường hợp: POST thiếu title (400, VALIDATION_ERROR, message và lỗi trường title) và GET sách không tồn tại (404, NOT_FOUND và message).

## Chạy lại

Từ `lab08-starter`, tạo thư mục `instance` nếu chưa có, cài Python dependencies rồi chạy API:

```sh
mkdir -p instance
python -m pip install -r requirements.txt
python -m app --port 5000
```

Trong terminal khác, tại thư mục `Postman`:

```sh
npm ci
./node_modules/.bin/newman run books-api.postman_collection.json -e local.postman_environment.json -r cli,junit --reporter-junit-export reports/junit.xml
```

Collection và environment có thể import vào Postman. Lần chạy đã lưu: 7 requests, 15 assertions, 0 failures; xem `reports/newman.txt` và `reports/junit.xml`. Chạy với database thử nghiệm: GET /books/9999 giả định ID 9999 chưa tồn tại.

Lần chạy lại dùng API tại cổng 18978 và SQLite riêng, với `--env-var base_url=http://127.0.0.1:18978`. `reports/newman.txt` là đầu ra CLI lưu trực tiếp và `reports/junit.xml` do Newman xuất. Ảnh HTML dựng lại trước đây đã được gỡ; chưa có ảnh chụp terminal trực tiếp.
