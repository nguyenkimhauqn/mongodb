# Finance Tracker - Ứng Dụng Quản Lý Tài Chính Cá Nhân 💰

Đồ án cuối kỳ môn MongoDB - Ứng dụng quản lý tài chính cá nhân với Streamlit và MongoDB.

---

## 👥 Thành Viên Nhóm

| STT | Họ và Tên | Vai Trò |
|-----|-----------|---------|
| 1 | **Nguyễn Kim Hậu** | Trưởng nhóm |
| 2 | Nguyễn Hữu Hoanh | Thành viên |
| 3 | Hứa Lê Anh Tuấn | Thành viên |

---

## 📋 Các Topics Đã Thực Hiện (Tổng: 20 điểm)

### 1️⃣ Budget Management System - 6 điểm ✅

**Mô tả:** Hệ thống quản lý ngân sách theo từng danh mục và tháng/năm.

**Các tính năng đã thực hiện:**
- ✅ Collection `budgets` với fields: `user_id`, `category`, `amount`, `month`, `year`, `is_active`
- ✅ CRUD đầy đủ: Create, Read, Update, Delete (soft delete)
- ✅ **Compound Unique Index**: `user_id + category + month + year` đảm bảo mỗi user chỉ có 1 budget cho 1 category trong 1 tháng
- ✅ **MongoDB Aggregation Pipeline**: Tính `spent` (số tiền đã chi) bằng `$match` + `$group`, KHÔNG dùng Python loop
- ✅ **Data Validation**: Chỉ cho phép tạo budget cho Expense categories
- ✅ Hiển thị progress bar (spent/budget) và warning khi vượt ngân sách

**File code:**
- Model: `dataset/budget_model.py`
- View: `view/budget_view.py`

---

### 2️⃣ Orphaned Transactions (Category Delete) - 3 điểm ✅

**Mô tả:** Xử lý transactions khi xóa category để tránh mất dữ liệu.

**Các tính năng đã thực hiện:**
- ✅ Khi xóa category, người dùng có 3 lựa chọn:
  1. **Move to "Others"**: Chuyển tất cả transactions sang category "Others"
  2. **Delete All**: Xóa tất cả transactions liên quan
  3. **Cancel**: Hủy thao tác xóa
- ✅ Sử dụng **MongoDB `update_many()`** và **`delete_many()`**, KHÔNG dùng Python loop
- ✅ Hiển thị số lượng transactions bị ảnh hưởng trước khi xóa

**File code:**
- Model: `dataset/category_model.py` (method `delete_category_with_handling()`)
- View: `view/category_view.py`

---

### 3️⃣ User Deletion Data Leak - 3 điểm ✅

**Mô tả:** Xóa toàn bộ dữ liệu của user khi xóa tài khoản (cascade delete).

**Các tính năng đã thực hiện:**
- ✅ Khi user xóa tài khoản, tự động xóa:
  - Tất cả **transactions** của user
  - Tất cả **budgets** của user
  - Tất cả **categories** của user
  - **User account** trong collection `users`
- ✅ Sử dụng **MongoDB `delete_many()`**, KHÔNG dùng Python loop
- ✅ Hiển thị tổng số items sẽ bị xóa và yêu cầu xác nhận bằng cách gõ "DELETE"
- ✅ Không để lại dữ liệu rác trong database

**File code:**
- Model: `dataset/user_model.py` (method `delete_user_completely()`)
- View: `view/user_view_simple.py`

---

### 4️⃣ Category Update + Transaction Sync - 3 điểm ✅

**Mô tả:** Tự động cập nhật tất cả transactions khi đổi tên category.

**Các tính năng đã thực hiện:**
- ✅ Khi đổi tên category, tự động cập nhật:
  - Tất cả **transactions** có category cũ → category mới
  - Tất cả **budgets** có category cũ → category mới
- ✅ Sử dụng **MongoDB `update_many()`**, KHÔNG dùng Python loop
- ✅ **Validation**: Không cho phép đổi sang tên category đã tồn tại
- ✅ **Block type change**: Không cho phép đổi type (Expense ↔ Income) nếu có transactions/budgets
- ✅ Hiển thị số lượng transactions và budgets đã được cập nhật

**File code:**
- Model: `dataset/category_model.py` (method `update_category()`)
- View: `view/category_view.py`

---

### 5️⃣ Budget Integrity (Category Delete) - 2 điểm ✅

**Mô tả:** Xử lý budgets khi xóa category để đảm bảo tính toàn vẹn dữ liệu.

**Các tính năng đã thực hiện:**
- ✅ Khi xóa category, tự động xử lý budgets liên quan:
  - **Move to "Others"**: Chuyển budgets sang category "Others"
  - **Delete All**: Xóa tất cả budgets liên quan
- ✅ Sử dụng **MongoDB `update_many()`** và **`delete_many()`**
- ✅ Hiển thị số lượng budgets bị ảnh hưởng
- ✅ Đảm bảo không có budgets "mồ côi" (orphaned budgets)

**File code:**
- Model: `dataset/category_model.py` (method `delete_category_with_handling()`)

---

### 6️⃣ Transaction Category Validation - 3 điểm ✅

**Mô tả:** Validate category khi thêm/sửa transaction.

**Các tính năng đã thực hiện:**
- ✅ **Validation khi thêm transaction**:
  - Category phải tồn tại trong database
  - Type của category phải khớp với transaction type
  - Ví dụ: Không cho phép tạo Income transaction với Expense category
- ✅ **Validation khi sửa transaction**:
  - Nếu đổi category hoặc type, phải validate lại
- ✅ Hiển thị lỗi rõ ràng khi validation thất bại
- ✅ Đảm bảo data integrity ở database level

**File code:**
- Model: `dataset/transaction_model.py` (method `_validate_category()`, `add_transaction()`, `update_transaction()`)
- View: `view/transaction_view.py`

---

## 🎯 Tính Năng Chính Của Ứng Dụng

### 📊 Quản Lý Cơ Bản
- ✅ **Dashboard**: Hiển thị tổng thu nhập, chi tiêu, số dư
- ✅ **Transaction Management**: Thêm, sửa, xóa, tìm kiếm giao dịch
- ✅ **Category Management**: Quản lý danh mục thu/chi với validation
- ✅ **Budget Management**: Quản lý ngân sách theo category và tháng
- ✅ **User Profile**: Quản lý thông tin tài khoản, xóa tài khoản

### 🌐 Tính Năng Nâng Cao
- ✅ **Đa ngôn ngữ**: Tiếng Việt và English
- ✅ **Login đơn giản**: Chỉ cần email, không cần mật khẩu
- ✅ **Sample Data**: Thêm 50 giao dịch mẫu để test
- ✅ **Data Integrity**: Cascade delete, auto sync khi update
- ✅ **MongoDB Aggregation**: Tính toán thống kê hiệu quả

---

## 🚀 Hướng Dẫn Cài Đặt và Chạy Ứng Dụng

### Yêu Cầu Hệ Thống
- **Python**: 3.11 trở lên
- **MongoDB Atlas**: Account miễn phí
- **Internet**: Để kết nối MongoDB Atlas

---

### Bước 1: Clone Repository

```bash
git clone https://github.com/nguyenkimhauqn/mongodb.git
cd mongodb
```

---

### Bước 2: Cài Đặt Dependencies

**Cách 1: Sử dụng pip**
```bash
pip install -r requirements.txt
```

**Cách 2: Cài từng package**
```bash
pip install streamlit pymongo python-dotenv pandas plotly matplotlib seaborn
```

**Các thư viện cần thiết:**
- `streamlit>=1.30.0` - Web framework
- `pymongo>=4.10.0` - MongoDB driver
- `python-dotenv>=1.0.0` - Quản lý biến môi trường
- `pandas`, `plotly`, `matplotlib`, `seaborn` - Visualization

---

### Bước 3: Cấu Hình MongoDB

#### 3.1. Tạo file `.env`

**Trên Mac/Linux:**
```bash
touch .env
```

**Trên Windows (PowerShell):**
```powershell
New-Item -Path .env -ItemType File
```

**Trên Windows (CMD):**
```cmd
type nul > .env
```

#### 3.2. Thêm MongoDB URI vào `.env`

Mở file `.env` và thêm dòng sau:

```env
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?appName=Cluster0
```

**Ví dụ:**
```env
MONGO_URI=mongodb+srv://myuser:mypassword123@cluster0.abc123.mongodb.net/?appName=Cluster0
```

#### 3.3. Lấy MongoDB URI từ Atlas

1. Truy cập [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Đăng nhập hoặc tạo tài khoản miễn phí
3. Tạo **Cluster** (chọn Free tier M0)
4. Tạo **Database User**:
   - Vào **Database Access** → **Add New Database User**
   - Tạo username và password (lưu lại)
5. Thêm **IP Whitelist**:
   - Vào **Network Access** → **Add IP Address**
   - Chọn **"Allow Access from Anywhere"** (0.0.0.0/0)
6. Lấy **Connection String**:
   - Vào **Database** → **Connect** → **Connect your application**
   - Copy connection string
   - Thay `<password>` bằng password đã tạo ở bước 4
   - Paste vào file `.env`

---

### Bước 4: Chạy Ứng Dụng

```bash
streamlit run app.py
```

Hoặc:

```bash
python -m streamlit run app.py
```

**Ứng dụng sẽ tự động mở tại:**
- **Local URL:** http://localhost:8501

---

### Bước 5: Đăng Nhập và Test

1. **Đăng nhập**: Nhập email bất kỳ (ví dụ: `test@example.com`)
   - Không cần mật khẩu
   - Tài khoản sẽ được tự động tạo nếu chưa tồn tại

2. **Thêm dữ liệu mẫu** (khuyến nghị):
   - Click **"🎲 Thêm Dữ Liệu Mẫu"** trong sidebar
   - Hệ thống sẽ tự động tạo:
     - 11 categories (7 Expense + 4 Income)
     - 50 transactions ngẫu nhiên trong 3 tháng gần đây

3. **Khám phá các tính năng**:
   - **Home**: Xem dashboard và thống kê
   - **Categories**: Quản lý danh mục, test xóa/sửa category
   - **Transactions**: Thêm/sửa/xóa giao dịch
   - **Budgets**: Tạo ngân sách, xem progress

---

## 🧪 Hướng Dẫn Test Các Topics

### Test Topic 1: Budget Management System

1. Vào **Budgets** tab
2. Click **"Tạo Ngân Sách Mới"**
3. Chọn category (chỉ hiện Expense categories)
4. Nhập số tiền và chọn tháng/năm
5. Kiểm tra:
   - ✅ Chỉ tạo được 1 budget cho 1 category trong 1 tháng
   - ✅ Progress bar hiển thị đúng (spent/budget)
   - ✅ Warning khi vượt ngân sách
   - ✅ Có thể sửa/xóa budget

### Test Topic 2: Orphaned Transactions

1. Vào **Categories** tab
2. Chọn 1 category có transactions (ví dụ: "Food & Dining")
3. Click **"Xóa"**
4. Chọn 1 trong 3 options:
   - **Move to Others**: Transactions chuyển sang "Others"
   - **Delete All**: Transactions bị xóa
   - **Cancel**: Hủy thao tác
5. Kiểm tra số lượng transactions affected

### Test Topic 3: User Deletion Data Leak

1. Click vào avatar/tên user trong sidebar
2. Click **"⚙️ Cài Đặt Tài Khoản"**
3. Mở **"⚠️ Xóa Tài Khoản Vĩnh Viễn"**
4. Click **"🗑️ Xóa Tài Khoản Vĩnh Viễn"**
5. Xem tổng số items sẽ bị xóa
6. Gõ "DELETE" để xác nhận
7. Kiểm tra: Tất cả data đã bị xóa, redirect về login

### Test Topic 4: Category Update + Transaction Sync

1. Vào **Categories** tab
2. Click **"Sửa"** một category có transactions
3. Đổi tên category
4. Kiểm tra:
   - ✅ Tất cả transactions đã được cập nhật tên mới
   - ✅ Tất cả budgets đã được cập nhật tên mới
   - ✅ Hiển thị số lượng items đã sync

### Test Topic 5: Budget Integrity

1. Vào **Budgets** tab, tạo budget cho 1 category
2. Vào **Categories** tab
3. Xóa category đó
4. Chọn **"Move to Others"** hoặc **"Delete All"**
5. Kiểm tra:
   - ✅ Budgets được xử lý đúng (moved hoặc deleted)
   - ✅ Hiển thị số budgets affected

### Test Topic 6: Transaction Category Validation

1. Vào **Transactions** tab
2. Click **"Thêm Giao Dịch"**
3. Thử các trường hợp:
   - Chọn type "Expense" → Chỉ hiện Expense categories
   - Chọn type "Income" → Chỉ hiện Income categories
4. Thử sửa transaction, đổi type:
   - ✅ Category dropdown tự động update theo type mới
   - ✅ Không cho phép category không hợp lệ

---

## 🗂️ Cấu Trúc Dự Án

```
mongoDb/
├── app.py                      # Main app (simple login)
├── app_google_oauth.py         # Backup (Google OAuth version)
├── config.py                   # App configuration
├── add_sample_data.py          # Script thêm dữ liệu mẫu
│
├── dataset/                    # Models
│   ├── database_manager.py    # MongoDB connection
│   ├── user_model.py          # User CRUD + cascade delete
│   ├── category_model.py      # Category CRUD + sync
│   ├── transaction_model.py   # Transaction CRUD + validation
│   └── budget_model.py        # Budget CRUD + aggregation
│
├── view/                       # Views
│   ├── home_view.py           # Dashboard
│   ├── category_view.py       # Category management
│   ├── transaction_view.py    # Transaction management
│   ├── budget_view.py         # Budget management
│   └── user_view_simple.py    # User profile + delete account
│
├── analytics/                  # Analytics
│   ├── analyzer.py            # Data analysis
│   └── visualizer.py          # Charts
│
├── locales/                    # Đa ngôn ngữ
│   ├── vi.py                  # Tiếng Việt
│   └── en.py                  # English
│
├── requirements.txt            # Dependencies
├── .env                        # MongoDB URI (không commit)
└── README.md                   # Tài liệu này
```

---

## 📊 Database Schema

### Collection: users
```javascript
{
  _id: ObjectId,
  email: String,
  created_at: DateTime,
  is_active: Boolean
}
```

### Collection: categories
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  name: String,
  type: String,  // "Expense" hoặc "Income"
  created_at: DateTime,
  last_modified: DateTime
}
```

### Collection: transactions
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  type: String,       // "Expense" hoặc "Income"
  category: String,
  amount: Number,
  date: DateTime,
  description: String,
  created_at: DateTime,
  last_modified: DateTime
}
```

### Collection: budgets
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  category: String,    // Chỉ Expense categories
  amount: Number,
  month: Number,       // 1-12
  year: Number,
  is_active: Boolean,
  created_at: DateTime,
  last_modified: DateTime
}
```

**Index (Compound Unique):**
```javascript
{ user_id: 1, category: 1, month: 1, year: 1, is_active: 1 }
```

---

## 🌐 Demo Trực Tuyến

**URL:** https://doancuoiky-hau-hoanh-tuan.streamlit.app/

**Test account:** Nhập email bất kỳ (không cần password)

---

## ⚙️ Xử Lý Lỗi Thường Gặp

### ❌ Lỗi: "No module named 'streamlit'"
**Giải pháp:**
```bash
pip install -r requirements.txt
```

### ❌ Lỗi: "MongoDB connection failed"
**Nguyên nhân:**
- File `.env` không tồn tại hoặc MONGO_URI sai
- IP chưa được whitelist trên MongoDB Atlas

**Giải pháp:**
1. Kiểm tra file `.env` có đúng format
2. Vào MongoDB Atlas → Network Access → Allow 0.0.0.0/0

### ❌ Lỗi: "Port 8501 is already in use"
**Giải pháp:**
```bash
streamlit run app.py --server.port 8502
```

---

## 🎓 Kết Luận

Dự án đã hoàn thành **6 topics** với tổng điểm **20/20**:

1. ✅ **Budget Management System** - 6 điểm
2. ✅ **Orphaned Transactions** - 3 điểm
3. ✅ **User Deletion Data Leak** - 3 điểm
4. ✅ **Category Update + Transaction Sync** - 3 điểm
5. ✅ **Budget Integrity** - 2 điểm
6. ✅ **Transaction Category Validation** - 3 điểm

**Công nghệ sử dụng:**
- **Backend**: Python, MongoDB (PyMongo)
- **Frontend**: Streamlit
- **Database**: MongoDB Atlas
- **Deployment**: Streamlit Cloud

**Highlights:**
- ✅ Sử dụng MongoDB Aggregation Pipeline (không loop)
- ✅ Compound Unique Index cho budgets
- ✅ Data Integrity đảm bảo (cascade delete, auto sync)
- ✅ UI/UX hiện đại, dễ sử dụng
- ✅ Đa ngôn ngữ (Tiếng Việt + English)

---

## 📞 Liên Hệ

**Giảng viên hướng dẫn:** [Tên giảng viên]

**Nhóm thực hiện:**
- Nguyễn Kim Hậu (Trưởng nhóm)
- Nguyễn Hữu Hoanh
- Hứa Lê Anh Tuấn

**Năm học:** 2024-2025

---

© 2025 Finance Tracker - APTECH MongoDB Project
