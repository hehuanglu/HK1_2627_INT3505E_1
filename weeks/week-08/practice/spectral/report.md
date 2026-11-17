# Kết quả Lab 2

- Spectral: **0 errors, 13 warnings**, mã thoát 0 khi dùng `--fail-severity error`.
- Các cảnh báo: thiếu `info.contact`, `description` và `tags` của các operation. Chi tiết: [spectral.txt](reports/spectral.txt).
- Custom rule: phát hiện schema rỗng trong bản sao thử nghiệm, báo 1 error; xem [custom-rule-negative.txt](reports/custom-rule-negative.txt).
- Pytest Lab 1: 5 test thành công.
- Minh chứng gốc: [đầu ra Spectral](reports/spectral.txt) và [JSON](reports/spectral.json). Chưa có ảnh terminal trực tiếp.

Cách chạy và phạm vi kiểm tra nằm trong [README](README.md).
