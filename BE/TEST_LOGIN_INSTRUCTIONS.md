# 🧪 TEST LOGIN - HƯỚNG DẪN CHI TIẾT

## 🎯 Mục đích
Tạo một test server riêng để debug login mà không ảnh hưởng đến backend chính.

## 📝 Các bước thực hiện

### BƯỚC 1: Chạy Test Server
Mở terminal mới và chạy:
```bash
python BE/test_login_endpoint.py
```

Server sẽ chạy trên: **http://localhost:5001**

### BƯỚC 2: Test Login với Debug
Có 2 cách test:

#### Cách 1: Dùng file HTTP (Khuyến nghị)
1. Mở file: `BE/https/test_debug_login.http`
2. Click vào "Send Request" ở request đầu tiên
3. Xem response với debug chi tiết

#### Cách 2: Dùng curl
```bash
curl -X POST http://localhost:5001/test/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

### BƯỚC 3: Xem Debug Info
Response sẽ có format:
```json
{
  "status": "success" hoặc "error",
  "message": "...",
  "debug": {
    "step": "Bước hiện tại",
    "details": [
      "✅ User found: UserID=1",
      "✅ Status is ACTIVE",
      "✅ Password CORRECT!"
    ]
  }
}
```

### BƯỚC 4: Nếu Password Sai - Fix Ngay
Nếu test login báo password sai, chạy request fix:
```bash
curl -X POST http://localhost:5001/test/fix-password \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

Hoặc dùng file HTTP: Request thứ 2 trong `test_debug_login.http`

### BƯỚC 5: Test Lại
Sau khi fix, test login lại để xác nhận.

## 🔍 Các Endpoint Test

### 1. POST /test/login
Test login với debug chi tiết
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response thành công:**
```json
{
  "status": "success",
  "message": "Đăng nhập thành công",
  "user": {
    "userId": 1,
    "username": "admin"
  },
  "debug": {
    "step": "4. Login SUCCESS",
    "details": [...]
  }
}
```

**Response thất bại:**
```json
{
  "status": "error",
  "message": "Mật khẩu không đúng",
  "debug": {
    "step": "3. Verifying password",
    "details": [
      "❌ Password INCORRECT!",
      "Correct hash would be: $2b$12$..."
    ]
  }
}
```

### 2. POST /test/fix-password
Fix password hash cho user
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Password updated for user 'admin'",
  "new_hash": "$2b$12$...",
  "password": "admin123"
}
```

### 3. POST /test/check-hash
Kiểm tra password hash có hợp lệ không
```json
{
  "password": "admin123",
  "hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWEgEjqK"
}
```

**Response:**
```json
{
  "status": "success",
  "is_valid": true,
  "password": "admin123",
  "hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN..."
}
```

### 4. GET /test/info
Thông tin test server
```
GET http://localhost:5001/test/info
```

## 🐛 Debug Flow

Test server sẽ kiểm tra từng bước:

1. **Check user exists**
   - ✅ User tồn tại → Tiếp tục
   - ❌ User không tồn tại → Trả về lỗi

2. **Check status**
   - ✅ Status = ACTIVE → Tiếp tục
   - ❌ Status khác → Trả về lỗi

3. **Verify password**
   - ✅ Password đúng → Login thành công
   - ❌ Password sai → Trả về lỗi + hash đúng

## 📊 Kết quả mong đợi

Sau khi test, bạn sẽ biết chính xác:
- ✅ User có tồn tại không
- ✅ Status có phải ACTIVE không
- ✅ Password hash có đúng format bcrypt không
- ✅ Password có khớp với hash không
- 🔧 Nếu sai, hash đúng phải là gì

## 🔄 Sau khi Fix

1. Test login trên test server (port 5001) → Phải thành công
2. Restart backend chính (port 5000)
3. Test login từ frontend → Phải thành công

## ⚠️ Lưu ý

- Test server chạy trên port **5001** (khác với backend chính port 5000)
- Test server chỉ để debug, không thay thế backend chính
- Sau khi fix xong, phải restart backend chính để áp dụng

## 🎯 Checklist

- [ ] Chạy test server: `python BE/test_login_endpoint.py`
- [ ] Test login: POST /test/login
- [ ] Xem debug info trong response
- [ ] Nếu sai, fix: POST /test/fix-password
- [ ] Test lại login
- [ ] Restart backend chính
- [ ] Test từ frontend
