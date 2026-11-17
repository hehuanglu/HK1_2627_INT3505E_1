# Lab 4 — Locust

`locustfile.py` bổ sung tìm kiếm năm; 404 dự kiến khi đọc ID ngẫu nhiên được đánh dấu thành công. Không giả lập lỗi. Xem `analysis.md`, các báo cáo `reports/A.html`, `B.html`, `C.html`, log và CSV; `evidence/` chứa ảnh chụp báo cáo HTML thực tế.

Cài dependencies từ `../lab08-starter/requirements.txt`, chạy API với database thử nghiệm, rồi chạy từ thư mục này (thay host nếu cần):

```sh
locust -f locustfile.py --headless -H http://127.0.0.1:5001 -u 10 -r 2 -t 30s --html reports/A.html --csv reports/A
locust -f locustfile.py --headless -H http://127.0.0.1:5001 -u 50 -r 5 -t 60s --html reports/B.html --csv reports/B
locust -f locustfile.py --headless -H http://127.0.0.1:5001 -u 200 -r 50 -t 30s --html reports/C.html --csv reports/C
```

Các POST tạo dữ liệu; nên dùng database riêng. Với mỗi lần so sánh có kiểm soát, khởi tạo cùng dữ liệu ban đầu trước từng kịch bản.

Ảnh A, B, C trong `evidence/` được chụp trực tiếp khi mở các báo cáo HTML do Locust xuất; chúng thể hiện các lần chạy đã lưu, không phải chạy mới. File HTML, log và CSV gốc vẫn nằm trong `reports/`.
