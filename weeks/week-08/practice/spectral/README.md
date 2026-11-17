# Lab 2 — OpenAPI / Spectral

Spec đang dùng là `../lab08-starter/openapi.yaml`. Ba lỗi của đề đã được sửa trong spec: `GET /books` có `operationId`, response 204 của DELETE không có body, và `Book.year` có kiểu integer. Rule `response-200-has-fields` kiểm tra schema của response 200 có ít nhất một property, kể cả schema mảng và các schema hợp thành được Spectral phân giải.

## Chạy lại

Từ thư mục này (cần Node.js 18+):

```sh
npm ci
mkdir -p reports
./node_modules/.bin/spectral lint ../lab08-starter/openapi.yaml --ruleset .spectral.yaml --format stylish --fail-severity error --output reports/spectral.txt
./node_modules/.bin/spectral lint ../lab08-starter/openapi.yaml --ruleset .spectral.yaml --format json --fail-severity error --output reports/spectral.json
```

Lần chạy đã lưu: **0 errors, 13 warnings**, exit code 0. Các cảnh báo còn lại về `info.contact`, mô tả và tags của operation; chi tiết ở `reports/spectral.txt`. Các file `reports/spectral.txt` và `reports/spectral.json` là đầu ra trực tiếp của Spectral. Chưa có ảnh chụp terminal trực tiếp; ảnh HTML dựng lại trước đây đã được gỡ.

Đã kiểm tra rule bằng một bản sao tạm của spec với `GET /health` có `properties: {}`: Spectral báo lỗi `response-200-has-fields` và thoát với mã 1; kết quả ở `reports/custom-rule-negative.txt`. Bộ test Lab 1 cũng chạy thành công 5/5 test. Spectral không tự đối chiếu spec với hành vi Flask; cần test contract để kiểm chứng hành vi thực tế.
