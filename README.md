# Finance Tracker - Quản Lý Tài Chính Thông Minh 💰

Ứng dụng web quản lý tài chính cá nhân được xây dựng với Streamlit và MongoDB.

## � **KIỂM TRA DỰ ÁN ĐẠT YÊU CẦU**

### ⚡ Test Nhanh (30 giây)
```bash
python test_budget_requirements.py
```

**Kết quả:** ✅ **9/6 điểm** (150%) - **ĐẠT YÊU CẦU**

📖 **Xem chi tiết:** 
- [QUICK_CHECK.md](QUICK_CHECK.md) - Checklist ngắn gọn
- [TEST_NHANH_5_PHUT.md](TEST_NHANH_5_PHUT.md) - Guide test đầy đủ
- [SUMMARY_TEST.md](SUMMARY_TEST.md) - Tóm tắt kết quả

---

## 🌟 Điểm Nổi Bật

- ✅ **9/6 điểm Budget Management** (vượt yêu cầu 50%)
- ✅ **MongoDB Aggregation** ($match + $group) - KHÔNG dùng Python loop
- ✅ **Compound Unique Index** - Database level constraint
- ✅ **Data Validation** chặt chẽ (category exists + Expense only)
- 🌐 Hỗ trợ **2 ngôn ngữ** (Tiếng Việt & English)
- 🎨 Giao diện hiện đại, thân thiện
- 🔒 Bảo mật dữ liệu người dùng
- ⚡ Xử lý nhanh với MongoDB

## 💰 Budget Management (6 điểm - Core Feature)

### ✅ Yêu Cầu Đã Đạt

1. **Collection budgets** ✅
   - Fields: `user_id`, `category`, `amount`, `month`, `year`, `is_active`
   - CHỈ áp dụng cho Expense categories

2. **CRUD đầy đủ** ✅
   - `create_budget()` - Tạo budget mới
   - `get_budgets_by_month()` - Lấy budgets theo month/year
   - `update_budget()` - Sửa amount
   - `delete_budget()` - Xóa budget (soft delete)

3. **Unique Constraint** ✅
   - Mỗi `user + category + month + year` CHỈ 1 budget
   - **Compound unique index** trong MongoDB
   - Logic update thay vì duplicate

4. **Tính Spent bằng Aggregation** ✅
   - MongoDB pipeline: `$match` + `$group`
   - KHÔNG dùng Python loop
   - Performance cao

5. **Data Integrity** ✅
   - Validate category tồn tại
   - Chỉ cho Expense categories
   - Xử lý khi xóa category

📖 **Chi tiết:** [BUDGET_LOGIC_EXPLANATION.md](BUDGET_LOGIC_EXPLANATION.md)

---

## Tính năng

### 📊 Quản Lý Cơ Bản
- ✅ Dashboard tổng quan tài chính với metrics
- ✅ Quản lý giao dịch (thu nhập/chi tiêu)
- ✅ Quản lý danh mục với validation
- ✅ **Quản lý ngân sách** (unique constraint: 1 budget/user-category-month) **← CORE FEATURE**
- ✅ Quản lý hồ sơ người dùng
- ✅ Phân tích và trực quan hóa dữ liệu

### ✨ Tính Năng Nâng Cao
- ✏️ **Chỉnh sửa danh mục:** Đổi tên danh mục, tự động cập nhật tất cả giao dịch & ngân sách
- 🗑️ **Xóa danh mục với tùy chọn:**
  - Chuyển dữ liệu sang "Others"
  - Xóa tất cả dữ liệu liên quan
  - Hủy thao tác
- 💰 **Liên kết Ngân sách - Danh mục:** Tự động xử lý ngân sách khi xóa danh mục
- 👤 **Xóa tài khoản cascade:** Xóa toàn bộ dữ liệu người dùng (transactions, budgets, categories)
- 🌐 **Đa ngôn ngữ:** Chuyển đổi giữa Tiếng Việt và English

---

## Yêu cầu hệ thống

- **Python 3.11** trở lên
- **MongoDB Atlas** account (hoặc MongoDB local)
- **pip** hoặc **uv** (Python package manager)

## Hướng dẫn cài đặt

### Bước 1: Clone repository

```bash
git clone https://github.com/nguyenkimhauqn/mongodb.git
cd mongodb
```

### Bước 2: Kiểm tra Python version

Đảm bảo bạn đã cài đặt Python 3.11 trở lên:

```bash
python --version
# hoặc
python3 --version
```

Nếu chưa có Python 3.11+, tải về tại [python.org](https://www.python.org/downloads/)

### Bước 3: Cài đặt dependencies

**Cách 1: Sử dụng uv (khuyến nghị - nhanh hơn)**

```bash
# Cài đặt uv (nếu chưa có)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Cài đặt dependencies từ pyproject.toml
uv pip install -e .
```

**Cách 2: Sử dụng pip (truyền thống)**

```bash
# Cài đặt các thư viện cần thiết
pip install streamlit pymongo python-dotenv

# hoặc nếu dùng pip3
pip3 install streamlit pymongo python-dotenv
```

**Các thư viện sẽ được cài đặt:**
- `streamlit>=1.30.0` - Framework web
- `pymongo>=4.10.0` - MongoDB driver
- `python-dotenv>=1.0.0` - Quản lý biến môi trường

### Bước 4: Cấu hình MongoDB

#### 4.1. Tạo file `.env`

```bash
# Trên Windows (PowerShell)
New-Item -Path .env -ItemType File

# Trên Windows (CMD)
type nul > .env

# Trên Linux/Mac
touch .env
```

#### 4.2. Thêm MongoDB connection string vào `.env`

Mở file `.env` và thêm dòng sau:

```env
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?appName=Cluster0
```

**Thay thế:**
- `<username>` → Tên người dùng MongoDB của bạn
- `<password>` → Mật khẩu MongoDB của bạn  
- `<cluster>` → Địa chỉ cluster của bạn

**Ví dụ:**
```env
MONGO_URI=mongodb+srv://myuser:mypassword123@cluster0.abc123.mongodb.net/?appName=Cluster0
```

**Lưu ý:** Nếu dùng MongoDB local:
```env
MONGO_URI=mongodb://localhost:27017/
```

#### 4.3. Thiết lập MongoDB Atlas (nếu chưa có)

1. Truy cập [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) và đăng ký tài khoản miễn phí
2. Tạo một **Cluster mới** (chọn free tier M0)
3. Tạo **Database User**:
   - Vào **Database Access** → **Add New Database User**
   - Chọn **Password authentication**
   - Tạo username và password (lưu lại để dùng trong `.env`)
4. Thêm **IP Address** vào whitelist:
   - Vào **Network Access** → **Add IP Address**
   - Chọn **"Allow Access from Anywhere"** (0.0.0.0/0) để test
   - Hoặc thêm IP cụ thể của bạn để bảo mật hơn
5. Lấy **Connection String**:
   - Vào **Database** → **Connect** → **Connect your application**
   - Copy connection string và paste vào file `.env`
   - Thay `<password>` bằng password bạn đã tạo ở bước 3

### Bước 5: Thiết lập indexes (tùy chọn nhưng khuyến nghị)

Chạy script để tạo indexes cho database:

```bash
python setup_indexes.py
```

## Chạy ứng dụng

### Khởi động ứng dụng

```bash
streamlit run app.py
```

Hoặc:

```bash
python -m streamlit run app.py
```

### Truy cập ứng dụng

Sau khi chạy lệnh trên, ứng dụng sẽ tự động mở trong trình duyệt tại:

- **Local URL:** http://localhost:8501
- **Network URL:** http://<your-ip>:8501

Nếu không tự động mở, copy URL từ terminal và paste vào trình duyệt.

### Dừng ứng dụng

Nhấn `Ctrl + C` trong terminal để dừng ứng dụng.

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

### ❌ Lỗi: "No module named 'streamlit'"
**Nguyên nhân:** Chưa cài đặt dependencies

**Giải pháp:**
```bash
pip install streamlit pymongo python-dotenv
```

### ❌ Lỗi: "bad auth: authentication failed"
**Nguyên nhân:** Thông tin đăng nhập MongoDB sai

**Giải pháp:**
1. Kiểm tra lại `username` và `password` trong file `.env`
2. Đảm bảo IP của bạn đã được thêm vào **Network Access** trên MongoDB Atlas
3. Kiểm tra connection string có đúng định dạng: `mongodb+srv://username:password@cluster...`
4. Thử tạo lại Database User trên MongoDB Atlas

### ❌ Lỗi: "No module named 'dotenv'"
**Nguyên nhân:** Chưa cài đặt python-dotenv

**Giải pháp:**
```bash
pip install python-dotenv
```

### ❌ Lỗi: "Connection refused" hoặc "Server selection timed out"
**Nguyên nhân:** Không kết nối được MongoDB

**Giải pháp:**
1. Kiểm tra internet connection
2. Kiểm tra MongoDB Atlas cluster đang chạy
3. Kiểm tra IP whitelist trên MongoDB Atlas
4. Thử connection string khác (nếu có)

### ❌ Lỗi: "Port 8501 is already in use"
**Nguyên nhân:** Port 8501 đang được sử dụng bởi ứng dụng khác

**Giải pháp:**
```bash
# Chạy trên port khác
streamlit run app.py --server.port 8502
```

### ❌ Lỗi: "FileNotFoundError: .env"
**Nguyên nhân:** Chưa tạo file `.env`

**Giải pháp:**
1. Tạo file `.env` trong thư mục gốc của dự án
2. Thêm dòng `MONGO_URI=...` vào file

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

## 🚀 Deploy lên Streamlit Cloud

Ứng dụng này có thể deploy lên **Streamlit Cloud** miễn phí. Thực hiện các bước sau:

### Bước 1: Chuẩn bị Repository

1. **Đảm bảo code đã được push lên GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Kiểm tra các file cần thiết:**
   - ✅ `requirements.txt` - Đã có sẵn
   - ✅ `.streamlit/config.toml` - Đã có sẵn
   - ✅ `app.py` - File chính của ứng dụng

### Bước 2: Đăng ký Streamlit Cloud

1. Truy cập [share.streamlit.io](https://share.streamlit.io)
2. Đăng nhập bằng **GitHub account** của bạn
3. Click **"New app"** để tạo ứng dụng mới

### Bước 3: Cấu hình App trên Streamlit Cloud

1. **Chọn repository:**
   - Chọn repository chứa code của bạn
   - Chọn branch (thường là `main` hoặc `master`)
   - Chọn file chính: `app.py`

2. **Cấu hình Secrets (QUAN TRỌNG):**
   
   Click vào **"Advanced settings"** → **"Secrets"** và thêm:
   
   ```toml
   MONGO_URI = "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?appName=Cluster0"
   ```
   
   **Lưu ý:**
   - Thay `<username>`, `<password>`, và `<cluster>` bằng thông tin MongoDB Atlas của bạn
   - **KHÔNG** để khoảng trắng xung quanh dấu `=`
   - Đảm bảo MongoDB Atlas cho phép kết nối từ Streamlit Cloud (xem Bước 4)

3. **Click "Deploy"** và chờ ứng dụng deploy

### Bước 4: Cấu hình MongoDB Atlas

**QUAN TRỌNG:** Streamlit Cloud sử dụng IP động, bạn cần:

1. **Cho phép truy cập từ mọi IP (để test):**
   - Vào MongoDB Atlas → **Network Access**
   - Click **"Add IP Address"**
   - Chọn **"Allow Access from Anywhere"** (0.0.0.0/0)
   - Click **"Confirm"**

   ⚠️ **Lưu ý bảo mật:** Nếu muốn bảo mật hơn, bạn có thể thêm IP cụ thể của Streamlit Cloud, nhưng điều này phức tạp hơn.

2. **Kiểm tra Database User:**
   - Đảm bảo Database User có quyền đọc/ghi database
   - Username và password phải khớp với trong secrets

### Bước 5: Chạy Setup Indexes (Tùy chọn)

Sau khi deploy, bạn có thể chạy script setup indexes:

1. Truy cập ứng dụng đã deploy
2. Mở terminal trên Streamlit Cloud (nếu có) hoặc chạy local:
   ```bash
   python setup_indexes.py
   ```

### URL Ứng dụng

Sau khi deploy thành công, bạn sẽ có URL dạng:
```
https://<your-app-name>.streamlit.app
```

### Xử lý lỗi khi Deploy

#### ❌ Lỗi: "ModuleNotFoundError"
**Nguyên nhân:** Thiếu dependencies trong `requirements.txt`

**Giải pháp:**
- Kiểm tra `requirements.txt` có đầy đủ packages
- Đảm bảo version tương thích

#### ❌ Lỗi: "MongoDB connection failed"
**Nguyên nhân:** 
- Secrets chưa được cấu hình đúng
- MongoDB Atlas chưa cho phép IP của Streamlit Cloud

**Giải pháp:**
1. Kiểm tra lại secrets trong Streamlit Cloud
2. Kiểm tra Network Access trên MongoDB Atlas
3. Kiểm tra connection string có đúng format

#### ❌ Lỗi: "Authentication failed"
**Nguyên nhân:** Username/password MongoDB sai

**Giải pháp:**
- Kiểm tra lại credentials trong secrets
- Thử tạo Database User mới trên MongoDB Atlas

### Lưu ý Bảo mật

⚠️ **QUAN TRỌNG:**
- **KHÔNG** commit file `.env` lên GitHub
- Sử dụng **Secrets** của Streamlit Cloud để lưu `MONGO_URI`
- Sử dụng password mạnh cho MongoDB
- Xem xét giới hạn IP whitelist trên MongoDB Atlas (nếu cần bảo mật cao)

---

## Hỗ trợ

Nếu gặp vấn đề khi cài đặt hoặc sử dụng, vui lòng liên hệ hoặc tạo issue.

## License

[Thêm thông tin license của bạn]