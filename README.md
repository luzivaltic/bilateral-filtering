# billateral-filtering

# Các hàm chính:
  1. extract_and_flatten_channels: Lấy từng kênh màu riêng biệt từ ảnh.
  2. poisson_disk_sampling: Từ mỗi kênh màu, thực hiện chọn ngẫu nhiên một tập giá trị điểm ảnh nhưng đảm bảo các điểm được chọn cách nhau một khoảng tối thiểu (bằng bán kính xác định). Mục đích là lấy một nhóm “mẫu màu” rải đều mà không quá gần nhau.
  3. o1_gaussian_filter: Áp dụng lọc Gauss lên từng kênh màu để làm mờ ảnh (giảm nhiễu, tạo hiệu ứng mịn).
bilinear_interpolation: Lấy một giá trị màu mục tiêu (target) trong số mẫu đã chọn, sau đó nội suy dựa trên các điểm mẫu xung quanh và kết quả lọc Gauss, để ước lượng giá trị màu tương ứng.
  4. main: Sau khi nội suy và lọc, kết hợp lại các kênh R, G, B để tạo ảnh lọc cuối cùng, đồng thời in ra các thời gian xử lý cho từng giai đoạn.
