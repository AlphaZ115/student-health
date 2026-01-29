# 📘 BÁO CÁO DỰ ÁN  
## Hệ thống theo dõi sức khỏe học sinh (Flask + SQLite)

---

## 1. Mô tả về Project

### 1.1 Chủ đề / Ứng dụng  
Dự án xây dựng một **ứng dụng web tương tác với cơ sở dữ liệu SQLite** nhằm hỗ trợ công tác y tế học đường.  
Hệ thống giúp lưu trữ và phân tích dữ liệu sức khỏe học sinh qua nhiều lần khám định kỳ.

### 1.2 Mục tiêu  
- Quản lý thông tin học sinh trong trường  
- Theo dõi các lần khám sức khỏe theo thời gian  
- Phát hiện học sinh có chỉ số BMI bất thường  
- Thống kê và phân tích dữ liệu phục vụ nhà trường  

### 1.3 Các chức năng chính  
Ứng dụng bao gồm các tính năng:

- **Quản lý học sinh**
  - Thêm học sinh mới  
  - Xem danh sách học sinh  
  - Sửa và xóa thông tin học sinh  

- **Quản lý khám sức khỏe**
  - Mỗi học sinh có thể được khám nhiều lần  
  - Lưu chiều cao, cân nặng và ngày khám  

- **Phân tích sức khỏe**
  - Tính BMI và cảnh báo bất thường  
  - Thống kê số lần khám theo tháng  
  - So sánh chiều cao trung bình theo lớp  

---

## 2. Mô tả về Cơ sở dữ liệu

### 2.1 Số lượng bảng  
Cơ sở dữ liệu gồm **2 bảng chính**:

1. `HocSinh`
2. `SucKhoe`

---

### 2.2 Bảng `HocSinh`

Lưu thông tin cơ bản của học sinh.

| Thuộc tính | Kiểu dữ liệu | Ý nghĩa |
|----------|-------------|--------|
| MaHS     | INTEGER     | Khóa chính (ID học sinh) |
| TenHS    | TEXT        | Họ tên học sinh |
| Lop      | TEXT        | Lớp học |
| NgaySinh | TEXT        | Ngày sinh |

---

### 2.3 Bảng `SucKhoe`

Lưu thông tin khám sức khỏe nhiều lần của học sinh.

| Thuộc tính | Kiểu dữ liệu | Ý nghĩa |
|----------|-------------|--------|
| MaSK     | INTEGER     | Khóa chính (ID lần khám) |
| MaHS     | INTEGER     | Khóa ngoại liên kết học sinh |
| ChieuCao | REAL        | Chiều cao (m) |
| CanNang  | REAL        | Cân nặng (kg) |
| NgayKham | TEXT        | Ngày khám |

---

### 2.4 Mối quan hệ giữa các bảng

- Một học sinh có thể khám sức khỏe nhiều lần  
- Bảng `SucKhoe` liên kết với `HocSinh` thông qua khóa ngoại:

```
SucKhoe.MaHS  →  HocSinh.MaHS
```

=> Quan hệ **1 - N (One-to-Many)**

---

### 2.5 Một số truy vấn tiêu biểu

#### a) Tìm học sinh có BMI bất thường

```sql
SELECT HocSinh.TenHS,
       (CanNang / (ChieuCao * ChieuCao)) AS BMI
FROM SucKhoe
JOIN HocSinh ON SucKhoe.MaHS = HocSinh.MaHS
WHERE BMI < 18.5 OR BMI > 25;
```

---

#### b) Thống kê số lần khám theo tháng

(SQLite dùng `strftime`)

```sql
SELECT strftime('%m', NgayKham) AS Thang,
       COUNT(*) AS SoLan
FROM SucKhoe
GROUP BY Thang;
```

---

#### c) So sánh chiều cao trung bình theo lớp

```sql
SELECT Lop,
       AVG(ChieuCao) AS CaoTB
FROM SucKhoe
JOIN HocSinh ON SucKhoe.MaHS = HocSinh.MaHS
GROUP BY Lop;
```

---

## 3. Các công cụ / Framework sử dụng

### 3.1 Ngôn ngữ lập trình
- **Python**

### 3.2 Framework và thư viện

| Công cụ | Vai trò |
|--------|---------|
| Flask  | Xây dựng web backend |
| SQLite3 | Lưu trữ dữ liệu trong file database |
| Bootstrap 5 | Thiết kế giao diện nhanh và đẹp |
| Chart.js (tùy chọn) | Vẽ biểu đồ thống kê dữ liệu |

---

## 4. Hình ảnh / Link / Video Demo

### 4.1 Hình ảnh minh họa
Ứng dụng có thể cung cấp các ảnh chụp màn hình:

- Trang danh sách học sinh  
- Form thêm học sinh  
- Trang nhập dữ liệu khám sức khỏe  
- Trang BMI cảnh báo  
- Trang thống kê theo tháng  
- Trang so sánh chiều cao trung bình  

### 4.2 Link dự án (nếu có)
- GitHub repository: *(có thể bổ sung)*  

### 4.3 Video demo (bonus điểm)
- Video chạy thử ứng dụng: *(có thể quay 1–2 phút)*  

---

# ✅ Kết luận

Dự án **Hệ thống theo dõi sức khỏe học sinh** giúp nhà trường quản lý dữ liệu khám sức khỏe hiệu quả, hỗ trợ phát hiện sớm các trường hợp bất thường thông qua BMI và thống kê tổng hợp.

Ứng dụng có thể mở rộng thêm các chức năng như:
- Xuất báo cáo PDF/Excel  
- Phân quyền tài khoản giáo viên/y tế  
- Dashboard nâng cao  

---

📌 **Tài liệu nộp gồm:**
- Mã nguồn (Flask project)
- File database SQLite
- Báo cáo này (README.md)
