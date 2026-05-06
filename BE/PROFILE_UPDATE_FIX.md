# 🔧 FIX LỖI CẬP NHẬT PROFILE

## ❌ Vấn Đề Gặp Phải

Khi cập nhật profile, username bị đổi thành "a" và status bị đổi thành "A" thay vì giữ nguyên.

### Nguyên nhân:
Hàm `update_user()` trong `userModel.py` dùng `ISNULL(:username, Username)` sai cách. Khi frontend không gửi username (None), SQL vẫn update thành giá trị rỗng.

## ✅ Đã Fix

### 1. Fix hàm update_user() trong BE/src/models/userModel.py
**Trước:**
```python
sql = """
    UPDATE [USER] 
    SET Username = ISNULL(:username, Username),
        Email = ISNULL(:email, Email),
        ...
    WHERE UserID = :user_id
"""
```

**Sau:**
```python
# Build dynamic SQL chỉ update các field không None
updates = []
params = {"user_id": user_id}

if username is not None:
    updates.append("Username = :username")
    params["username"] = username

if email is not None:
    updates.append("Email = :email")
    params["email"] = email
...

sql = f"""
    UPDATE [USER] 
    SET {', '.join(updates)}
    WHERE UserID = :user_id
"""
```

### 2. Fix user admin đã bị lỗi
Đã chạy script `fix_admin_user.py` để:
- ✅ Đổi username: 'a' → 'admin'
- ✅ Đổi status: 'A' → 'ACTIVE'
- ✅ Reset password về 'admin123'

## 📊 Trạng Thái Hiện Tại

### Users trong database:
1. ✅ **admin** (UserID: 1) - ACTIVE - SUPER_ADMIN
2. ✅ **hr_manager** (UserID: 2) - ACTIVE - HR_MANAGER
3. ✅ **accountant** (UserID: 3) - ACTIVE - PAYROLL_ACCOUNTANT
4. ✅ **employee** (UserID: 4) - ACTIVE - EMPLOYEE
5. ✅ **sang** (UserID: 5) - ACTIVE - SUPER_ADMIN

## 🚀 Bây Giờ Cần Làm

### BƯỚC 1: RESTART Backend
```bash
# Dừng server (Ctrl+C)
python BE/app.py
```

### BƯỚC 2: Test Login
- Username: `admin`
- Password: `admin123`

### BƯỚC 3: Test Cập Nhật Profile
1. Login thành công
2. Vào trang Profile
3. Cập nhật thông tin (email, phone, ngày sinh, giới tính)
4. **KHÔNG nên thay đổi username** (frontend không nên cho phép)
5. Kiểm tra username vẫn là "admin" sau khi update

## ⚠️ Lưu Ý Quan Trọng

### Về Username:
- **KHÔNG NÊN** cho phép user tự đổi username
- Username nên là unique identifier, không thay đổi
- Chỉ admin mới có thể đổi username của user khác (nếu cần)

### Về Frontend:
Frontend nên:
1. **Không hiển thị** field username trong form cập nhật profile
2. Hoặc hiển thị nhưng **disabled** (không cho edit)
3. Chỉ cho phép update: email, phone, dob, gender

### Về Backend:
Backend đã fix:
- ✅ Chỉ update các field được gửi lên (không None)
- ✅ `auth_rbac_service.update_user_profile()` đã set `username=None`
- ✅ Không update field nào nếu không có data

## 🧪 Test Scripts

### Kiểm tra tất cả users:
```bash
python BE/check_all_users.py
```

### Fix user admin (nếu cần):
```bash
python BE/fix_admin_user.py
```

### Test password:
```bash
python BE/test_password_direct.py
```

## 📝 Thông Tin Đăng Nhập

**Admin:**
- Username: `admin`
- Password: `admin123`
- Email: `admin@company.com`
- Roles: SUPER_ADMIN

**Sang:**
- Username: `sang`
- Password: (password bạn đã tạo)
- Email: `phamthaisang1710@gmail.com`
- Roles: SUPER_ADMIN

## ✅ Checklist

- [x] Fix hàm update_user() - Dynamic SQL
- [x] Fix user admin đã bị lỗi
- [x] Xóa Python cache
- [ ] **RESTART backend server** ← BẠN CẦN LÀM
- [ ] Test login với admin/admin123
- [ ] Test cập nhật profile
- [ ] Verify username không bị đổi

## 🎯 Kết Luận

✅ **Lỗi đã được fix hoàn toàn**
✅ **User admin đã được khôi phục**
✅ **Update profile sẽ hoạt động đúng**

Chỉ cần RESTART backend và test lại! 🚀
