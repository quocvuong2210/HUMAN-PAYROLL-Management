# 🔧 Hướng Dẫn Fix Lỗi Login - Complete Guide

## ❌ Lỗi Gặp Phải
```
Invalid column name 'Password'
(pyodbc.ProgrammingError) ('42S22', "[42S22] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Invalid column name 'Password'.")
```

## 🔍 Nguyên Nhân
- **Database schema** dùng cột tên: `PasswordHash`
- **Python code** đang dùng: `Password`
- Khi SELECT không tìm thấy cột → Lỗi SQL

## ✅ Đã Sửa Các Files Sau

### 1. BE/src/models/userModel.py
- ✅ `register()` - Đổi INSERT `[Password]` → `[PasswordHash]`
- ✅ `login()` - Đổi SELECT `[Password]` → `[PasswordHash]`
- ✅ `change_password()` - Đổi SELECT và UPDATE `[Password]` → `[PasswordHash]`

### 2. BE/src/models/authModel.py
- ✅ `register()` - Đổi INSERT `[Password]` → `[PasswordHash]`
- ✅ `login()` - Đổi SELECT `[Password]` → `[PasswordHash]`
- ✅ `reset_password()` - Đổi UPDATE `[Password]` → `[PasswordHash]`

### 3. BE/src/models/user_model_v2.py
- ✅ `create_user()` - Đổi INSERT `[Password]` → `[PasswordHash]`

### 4. BE/create_admin_user.py
- ✅ Đã dùng đúng `PasswordHash` từ đầu

## 🚀 Các Bước Thực Hiện

### Bước 1: Xóa Python Cache (ĐÃ THỰC HIỆN)
```bash
# Đã xóa tất cả __pycache__ folders
```

### Bước 2: Kiểm Tra User Admin
```bash
python BE/check_admin_user.py
```

**Nếu user admin chưa tồn tại:**
```bash
python BE/create_admin_user.py
```

### Bước 3: Restart Backend Server
```bash
# Stop server hiện tại (Ctrl+C)
# Sau đó chạy lại:
python BE/app.py
```

### Bước 4: Test Login
Dùng file: `BE/https/test_login_simple.http`

```http
POST http://localhost:5000/api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

## 📋 Checklist

- [x] Sửa tất cả references từ `[Password]` → `[PasswordHash]`
- [x] Xóa Python cache (`__pycache__`)
- [ ] Chạy `python BE/check_admin_user.py` để kiểm tra
- [ ] Nếu cần, chạy `python BE/create_admin_user.py`
- [ ] Restart backend server
- [ ] Test login với admin/admin123

## 🎯 Kết Quả Mong Đợi

### Login Thành Công (200 OK)
```json
{
  "status": "success",
  "message": "Đăng nhập thành công",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refreshToken": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "userId": 1,
    "username": "admin",
    "email": "admin@company.com",
    "roles": ["SUPER_ADMIN"],
    "permissions": [...],
    "functions": [...]
  }
}
```

### Login Thất Bại - Sai Password (401 Unauthorized)
```json
{
  "status": "error",
  "message": "Mật khẩu không đúng"
}
```

### Login Thất Bại - User Không Tồn Tại (401 Unauthorized)
```json
{
  "status": "error",
  "message": "Tài khoản không tồn tại"
}
```

## 🔐 Default Admin Credentials
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@company.com`
- **Status**: `ACTIVE`
- **EmailVerified**: `1`

## 📝 Lưu Ý Quan Trọng

1. **Luôn restart server** sau khi sửa code Python
2. **Xóa cache** nếu thay đổi không có hiệu lực
3. **Kiểm tra database** trước khi test login
4. **Password phải dùng bcrypt** - không dùng werkzeug nữa

## 🆘 Nếu Vẫn Lỗi

### Lỗi: "Invalid column name 'Password'"
→ Có file nào đó chưa được sửa hoặc cache chưa được xóa
→ Chạy lại: `Get-ChildItem -Path BE -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force`

### Lỗi: "Tài khoản không tồn tại"
→ User admin chưa được tạo trong database
→ Chạy: `python BE/create_admin_user.py`

### Lỗi: "Invalid hash method ''"
→ Password hash trong database không đúng format bcrypt
→ Xóa user cũ và tạo lại bằng script `create_admin_user.py`

### Lỗi: "Mật khẩu không đúng"
→ Password hash không khớp
→ Kiểm tra bằng: `python BE/check_admin_user.py`

## 📞 Support Files
- `BE/check_admin_user.py` - Kiểm tra user admin
- `BE/create_admin_user.py` - Tạo user admin
- `BE/https/test_login_simple.http` - Test login
- `BE/docs/LOGIN_FIX_SUMMARY.md` - Tóm tắt fix
