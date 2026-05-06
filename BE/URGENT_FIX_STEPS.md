# 🚨 URGENT: Các Bước Fix Lỗi Login Ngay

## ❌ Lỗi hiện tại:
```
Invalid column name 'Password'
```

## ✅ Code đã được sửa - Bạn cần làm theo thứ tự:

### BƯỚC 1: Xóa tất cả Python cache (ĐÃ THỰC HIỆN)
```powershell
# Đã xóa xong
```

### BƯỚC 2: DỪNG Backend Server
```
Nhấn Ctrl+C trong terminal đang chạy backend
```

### BƯỚC 3: Kiểm tra user admin có tồn tại không
```bash
python BE/check_admin_user.py
```

**Nếu user admin CHƯA TỒN TẠI:**
```bash
python BE/create_admin_user.py
```

### BƯỚC 4: Test login trực tiếp (Optional - để debug)
```bash
python BE/test_login_direct.py
```

### BƯỚC 5: KHỞI ĐỘNG LẠI Backend Server
```bash
python BE/app.py
```

### BƯỚC 6: Test từ Frontend
- Mở trình duyệt
- Vào trang login
- Nhập:
  - Username: `admin`
  - Password: `admin123`
- Nhấn Đăng nhập

## 🔍 Nếu vẫn lỗi:

### Kiểm tra 1: Backend có đang chạy không?
```
Terminal phải hiển thị:
* Running on http://0.0.0.0:5000
```

### Kiểm tra 2: Database connection
```
Kiểm tra file BE/config.py
SQL_SERVER_PERMISSION_CONN phải đúng
```

### Kiểm tra 3: User admin trong database
```bash
python BE/check_admin_user.py
```
Phải hiển thị:
```
✅ User 'admin' tồn tại trong database
✅ Password 'admin123' ĐÚNG với hash trong database
```

## 📋 Checklist Hoàn Chỉnh

- [x] Code đã sửa từ `[Password]` → `[PasswordHash]`
- [x] Python cache đã xóa
- [ ] Backend server đã DỪNG
- [ ] Kiểm tra user admin (chạy check_admin_user.py)
- [ ] Nếu cần, tạo user admin (chạy create_admin_user.py)
- [ ] Backend server đã KHỞI ĐỘNG LẠI
- [ ] Test login từ frontend

## ⚠️ LƯU Ý QUAN TRỌNG

**PHẢI RESTART BACKEND SERVER!**

Python sẽ cache code cũ trong memory. Nếu không restart, code mới sẽ KHÔNG được load!

```bash
# 1. Dừng server (Ctrl+C)
# 2. Chờ 2 giây
# 3. Chạy lại:
python BE/app.py
```

## 🎯 Kết quả mong đợi

Sau khi làm đúng các bước trên, login sẽ thành công và trả về:

```json
{
  "status": "success",
  "message": "Đăng nhập thành công",
  "token": "eyJ0eXAi...",
  "user": {
    "userId": 1,
    "username": "admin",
    "email": "admin@company.com",
    "roles": ["SUPER_ADMIN"]
  }
}
```

## 📞 Debug Commands

```bash
# Kiểm tra user admin
python BE/check_admin_user.py

# Tạo user admin
python BE/create_admin_user.py

# Test login trực tiếp
python BE/test_login_direct.py

# Xóa cache
Get-ChildItem -Path BE -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
```
