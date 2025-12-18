<!-- Cài Đặt Thư Viện -->

### Cách 1: Cài đặt thủ công (Khuyến nghị)

```bash
# Cài đặt các thư viện cần thiết
pip install streamlit pymongo python-dotenv pandas matplotlib seaborn plotly

# Hoặc với Python 3 trên Linux/macOS
pip3 install streamlit pymongo python-dotenv pandas matplotlib seaborn plotly
```
### Cách 2: Sử dụng requirements.txt (Nếu có)

```bash
pip install -r requirements.txt
```

### Kiểm tra cài đặt:

```bash
# Kiểm tra Streamlit
streamlit --version

# Kiểm tra các thư viện
python -c "import streamlit, pymongo, dotenv; print('All packages installed!')"
```
```bash
# Cài lại Streamlit
pip install --upgrade streamlit

# Hoặc chạy trực tiếp
python -m streamlit run app.py
```

---

# Chạy ứng dụng
streamlit run app.py
```
