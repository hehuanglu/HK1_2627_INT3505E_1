# Hướng dẫn Môi trường Thực hành (Week 01 - Practice)

Mục này được thiết lập môi trường ảo Python và cài đặt Flask cho bài thực hành SOA.

## 1. Kích hoạt Virtual Environment

Mở terminal tại thư mục này (`weeks/week-01/practice`):

```bash
# Trên macOS / Linux:
source .venv/bin/activate

# Khi muốn thoát khỏi môi trường ảo:
deactivate
```

## 2. Quản lý Dependencies

- Các thư viện đã được xuất tại [requirements.txt](file:///Users/hahoangloc/Working/UET/SOA/weeks/week-01/practice/requirements.txt).
- Nếu cần cài lại hoặc cài thêm package mới:
  ```bash
  pip install -r requirements.txt
  ```

## 3. Chạy ứng dụng mẫu

Chạy ứng dụng Flask [app.py](file:///Users/hahoangloc/Working/UET/SOA/weeks/week-01/practice/app.py):

```bash
python app.py
```

Truy cập kiểm tra tại trình duyệt hoặc curl:
- `http://127.0.0.1:5000/`
- `http://127.0.0.1:5000/health`
