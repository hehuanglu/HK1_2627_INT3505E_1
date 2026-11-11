# Lab 1 — Books API tests

Project pytest dùng API từ repo `../lab08-starter` và SQLite tạm riêng cho từng test. Chạy từ thư mục này với Python 3.11 trở lên.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -v
```

Suite này có 4 test bắt buộc và 1 bonus. Để chạy riêng các test bắt buộc, dùng `.venv/bin/python -m pytest -v -k 'not test_response_extra_field_blocked'`.
