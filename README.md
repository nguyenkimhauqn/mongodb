# Finance Tracker - Quản Lý Tài Chính Thông Minh 💰

Ứng dụng web quản lý tài chính cá nhân được xây dựng với Streamlit và MongoDB.

## 🌟 Điểm Nổi Bật

- ✅ **18/20 điểm yêu cầu** + 1 điểm bonus đa ngôn ngữ
- 🌐 Hỗ trợ **2 ngôn ngữ** (Tiếng Việt & English)
- 🎨 Giao diện hiện đại, thân thiện
- 🔒 Bảo mật dữ liệu người dùng
- ⚡ Xử lý nhanh với MongoDB

## Tính năng

### 📊 Quản Lý Cơ Bản
- ✅ Dashboard tổng quan tài chính với metrics
- ✅ Quản lý giao dịch (thu nhập/chi tiêu)
- ✅ Quản lý danh mục với validation
- ✅ Quản lý ngân sách (unique constraint: 1 budget/user-category-month)
- ✅ Quản lý hồ sơ người dùng
- ✅ Phân tích và trực quan hóa dữ liệu

### ✨ Tính Năng Nâng Cao (Mới!)
- ✏️ **Chỉnh sửa danh mục:** Đổi tên danh mục, tự động cập nhật tất cả giao dịch & ngân sách
- 🗑️ **Xóa danh mục với tùy chọn:**
  - Chuyển dữ liệu sang "Others"
  - Xóa tất cả dữ liệu liên quan
  - Hủy thao tác
- 💰 **Liên kết Ngân sách - Danh mục:** Tự động xử lý ngân sách khi xóa danh mục
- 👤 **Xóa tài khoản cascade:** Xóa toàn bộ dữ liệu người dùng (transactions, budgets, categories)
- 🌐 **Đa ngôn ngữ:** Chuyển đổi giữa Tiếng Việt và English

> 📖 **Xem chi tiết:** [USER_GUIDE.md](USER_GUIDE.md) | [FEATURE_COMPLETION.md](FEATURE_COMPLETION.md)

## Yêu cầu hệ thống

- Python 3.11 trở lên
- MongoDB Atlas account (hoặc MongoDB local)
- pip (Python package manager)

## Hướng dẫn cài đặt

### 1. Clone hoặc tải dự án về máy

```bash
git clone <repository-url>
cd mongoDb
```

### 2. Cài đặt Python

Đảm bảo bạn đã cài đặt Python 3.11 trở lên. Kiểm tra phiên bản:

```bash
python --version
```

### 3. Cài đặt các thư viện cần thiết

Chạy lệnh sau để cài đặt tất cả dependencies:

```bash
python -m pip install streamlit pymongo python-dotenv
```

Hoặc nếu có file `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

### 4. Cấu hình MongoDB

#### Tạo file `.env` trong thư mục gốc của dự án:

```bash
# Trên Windows
type nul > .env

# Trên Linux/Mac
touch .env
```

#### Thêm cấu hình MongoDB vào file `.env`:

```env
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?appName=Cluster0
```

**Lưu ý:** 
- Thay `<username>` bằng tên người dùng MongoDB của bạn
- Thay `<password>` bằng mật khẩu MongoDB của bạn
- Thay `<cluster>` bằng địa chỉ cluster của bạn

**Ví dụ:**
```env
MONGO_URI=mongodb+srv://Hoanh:MyPass123@cluster0.nx6irmd.mongodb.net/?appName=Cluster0
```

### 5. Thiết lập MongoDB Atlas (nếu chưa có)

1. Truy cập [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Tạo tài khoản miễn phí
3. Tạo một Cluster mới
4. Tạo Database User:
   - Vào Database Access → Add New Database User
   - Chọn Password authentication
   - Tạo username và password
5. Thêm IP Address vào whitelist:
   - Vào Network Access → Add IP Address
   - Chọn "Allow Access from Anywhere" (0.0.0.0/0) để test
6. Lấy Connection String:
   - Vào Database → Connect → Connect your application
   - Copy connection string và thay thế vào file `.env`

## Chạy ứng dụng

Sau khi hoàn tất các bước trên, chạy lệnh sau để khởi động ứng dụng:

```bash
python -m streamlit run app.py
```

Ứng dụng sẽ tự động mở trong trình duyệt tại địa chỉ:
- Local URL: http://localhost:8501
- Network URL: http://<your-ip>:8501

## Cấu trúc dự án

```
mongoDb/
├── app.py                 # File chính của ứng dụng
├── config.py             # Cấu hình ứng dụng
├── .env                  # Biến môi trường (không commit lên Git)
├── README.md             # Tài liệu hướng dẫn
├── dataset/              # Models và database
│   ├── user_model.py
│   ├── transaction_model.py
│   ├── category_model.py
│   └── budget_model.py
├── view/                 # Giao diện người dùng
│   ├── home_view.py
│   ├── dashboard_view.py
│   ├── transaction_view.py
│   ├── category_view.py
│   ├── budget_view.py
│   └── user_view.py
└── analytics/            # Phân tích dữ liệu
    ├── analyzer.py
    └── visualizer.py
```

## Xử lý lỗi thường gặp

### Lỗi: "No module named streamlit"
```bash
python -m pip install streamlit
```

### Lỗi: "bad auth: authentication failed"
- Kiểm tra lại username và password trong file `.env`
- Đảm bảo IP của bạn đã được thêm vào whitelist trên MongoDB Atlas
- Kiểm tra connection string có đúng định dạng không

### Lỗi: "No module named dotenv"
```bash
python -m pip install python-dotenv
```

## Ghi chú bảo mật

⚠️ **QUAN TRỌNG:**
- **KHÔNG** commit file `.env` lên Git/GitHub
- Thêm `.env` vào file `.gitignore`
- Không chia sẻ thông tin đăng nhập MongoDB với người khác
- Sử dụng password mạnh cho MongoDB

## Tạo file .gitignore (nếu chưa có)

Tạo file `.gitignore` trong thư mục gốc với nội dung:

```gitignore
# Environment variables
.env

# Python cache
__pycache__/
*.py[cod]
*$py.class
*.so

# Virtual environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

## Hỗ trợ

Nếu gặp vấn đề khi cài đặt hoặc sử dụng, vui lòng liên hệ hoặc tạo issue.

## License

[Thêm thông tin license của bạn]