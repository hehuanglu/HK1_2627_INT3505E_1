# Lab 4 — Phân tích kết quả thực đo

Chạy ngày 17/11/2026, Locust 2.47.0, Flask development server threaded và SQLite thử nghiệm trên cùng máy, localhost cổng 5001. Dữ liệu được giữ giữa các kịch bản; POST làm database lớn dần, nên đây không phải phép so sánh có kiểm soát hoàn toàn. Số dưới đây lấy từ bảng cuối log và HTML; CSV được ghi định kỳ nên có thể thiếu những request cuối.

| Kịch bản | Users | Spawn/s | Thời lượng cấu hình | Request | p95 tổng hợp | Failure | RPS trung bình |
|---|---:|---:|---:|---:|---:|---:|---:|
| A | 10 | 2 | 30 s | 147 | 10 ms | 0/147 (0%) | 4.98 |
| B | 50 | 5 | 60 s | 1390 | 11 ms | 0/1390 (0%) | 23.28 |
| C | 200 | 50 | 30 s | 2959 | 41 ms | 0/2959 (0%) | 99.55 |

C có p95 tổng hợp cao nhất (41 ms so với 10 và 11 ms); mức tải đồng thời lớn hơn có thể góp phần tăng thời gian chờ, nhưng một lần chạy không xác định nguyên nhân. Trong C, GET /books có p95 52 ms và POST /books 46 ms. Không endpoint nào có failure được Locust ghi nhận; GET theo ID coi 404 dự kiến là thành công, nên con số này không phải tỷ lệ HTTP không thành công thô. Không có failure giả lập và không kết luận rằng mọi 404 là lỗi máy chủ.

Với ngưỡng giả định p95 < 300 ms, cả ba đạt trong lần đo này. Kết quả gồm thời gian tăng tải, tải có khoảng nghỉ 1–3 giây, chạy ngắn, một máy và database thay đổi; không suy ra SLO production hoặc công suất tối đa.

Để kiểm chứng pool giới hạn 5: cấu hình pool SQLAlchemy thực sự hỗ trợ giới hạn đó, kiểm tra pool class và đo checkout/wait, chạy lại cùng dữ liệu ban đầu và cùng tải với pool 5 so với đối chứng lớn hơn, lặp nhiều lần; so sánh p95, RPS, timeout và wait time. Chưa thực hiện thí nghiệm pool này.
