# 🚀 Postman Testing Guide

## Setup

1. **Base URL:** `http://localhost:5000/api/v2/auth`
2. **Content-Type:** `application/json`

---

## Test Flow (Recommended Order)

### 1️⃣ Đăng ký User mới

**Request:**
```
POST http://localhost:5000/api/v2/auth/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "testuser@example.com",
  "password": "Test123456",
  "phone": "0987654321",
  "dob": "1995-05-15",
  "gender": "Male"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Đăng ký thành công. Vui lòng kiểm tra email để xác nhận tài khoản.",
  "user_id": 1,
  "email_sent": true
}
```

**Note:** Kiểm tra console server để lấy verification token (mock mode)

---

### 2️⃣ Xác nhận Email

**Request:**
```
GET http://localhost:5000/api/v2/auth/verify-email?token=<TOKEN_FROM_EMAIL>
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Email đã được xác nhận thành công"
}
```

---

### 3️⃣ Đăng nhập

**Request:**
```
POST http://localhost:5000/api/v2/auth/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "Test123456"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Đăng nhập thành công",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "user_id": 1,
    "username": "testuser",
    "email": "testuser@example.com",
    "roles": []
  }
}
```

**⚠️ IMPORTANT:** Lưu `access_token` và `refresh_token` để sử dụng cho các request tiếp theo!

---

### 4️⃣ Lấy thông tin Profile

**Request:**
```
GET http://localhost:5000/api/v2/auth/me
Authorization: Bearer <ACCESS_TOKEN>
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "user_info": {
      "UserID": 1,
      "Username": "testuser",
      "Email": "testuser@example.com",
      "PhoneNumber": "0987654321",
      "DateOfBirth": "1995-05-15",
      "Gender": "Male",
      "Status": "ACTIVE",
      "EmailVerified": true,
      "CreatedAt": "2024-01-01T10:00:00"
    },
    "roles": [],
    "permissions": [],
    "functions": []
  }
}
```

---

### 5️⃣ Lấy danh sách quyền

**Request:**
```
GET http://localhost:5000/api/v2/auth/me/permissions
Authorization: Bearer <ACCESS_TOKEN>
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "user_id": 1,
    "permissions": []
  }
}
```

---

### 6️⃣ Test Refresh Token

**Request:**
```
POST http://localhost:5000/api/v2/auth/refresh-token
Content-Type: application/json

{
  "refresh_token": "<REFRESH_TOKEN>"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 7️⃣ Test Forgot Password

**Request:**
```
POST http://localhost:5000/api/v2/auth/forgot-password
Content-Type: application/json

{
  "email": "testuser@example.com"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Email hướng dẫn đặt lại mật khẩu đã được gửi",
  "email_sent": true
}
```

**Note:** Kiểm tra console để lấy reset token

---

### 8️⃣ Test Reset Password

**Request:**
```
POST http://localhost:5000/api/v2/auth/reset-password
Content-Type: application/json

{
  "token": "<RESET_TOKEN>",
  "new_password": "NewPassword123"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Mật khẩu đã được đặt lại thành công"
}
```

---

### 9️⃣ Đăng nhập lại với mật khẩu mới

**Request:**
```
POST http://localhost:5000/api/v2/auth/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "NewPassword123"
}
```

---

## 🔐 Testing RBAC (Admin Functions)

### Setup: Gán Role ADMIN cho user

**Cách 1: Sử dụng SQL trực tiếp**
```sql
-- Gán role ADMIN (RoleID = 1) cho user
INSERT INTO [USER_ROLE] (UserID, RoleID)
VALUES (1, 1);
```

**Cách 2: Sử dụng API (nếu đã có user admin khác)**
```
POST http://localhost:5000/api/v2/auth/admin/users/assign-role
Authorization: Bearer <ADMIN_ACCESS_TOKEN>
Content-Type: application/json

{
  "user_id": 1,
  "role_id": 1
}
```

---

### 10. Lấy danh sách Roles (Cần role ADMIN hoặc HR_MANAGER)

**Request:**
```
GET http://localhost:5000/api/v2/auth/admin/roles
Authorization: Bearer <ACCESS_TOKEN>
```

**Expected Response:**
```json
{
  "status": "success",
  "data": [
    {
      "RoleID": 1,
      "RoleName": "ADMIN",
      "Description": "Quản trị viên hệ thống",
      "CreatedAt": "2024-01-01T10:00:00"
    }
  ]
}
```

---

### 11. Lấy danh sách Permissions (Chỉ ADMIN)

**Request:**
```
GET http://localhost:5000/api/v2/auth/admin/permissions
Authorization: Bearer <ACCESS_TOKEN>
```

---

### 12. Lấy danh sách Functions (Chỉ ADMIN)

**Request:**
```
GET http://localhost:5000/api/v2/auth/admin/functions
Authorization: Bearer <ACCESS_TOKEN>
```

---

### 13. Gán Role cho User khác

**Request:**
```
POST http://localhost:5000/api/v2/auth/admin/users/assign-role
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json

{
  "user_id": 2,
  "role_id": 3
}
```

---

### 14. Xem Roles của User

**Request:**
```
GET http://localhost:5000/api/v2/auth/admin/users/2/roles
Authorization: Bearer <ACCESS_TOKEN>
```

---

### 15. Đăng xuất

**Request:**
```
POST http://localhost:5000/api/v2/auth/logout
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json

{
  "refresh_token": "<REFRESH_TOKEN>"
}
```

---

## 🧪 Testing Error Cases

### Test 1: Đăng nhập với email chưa verify

1. Đăng ký user mới
2. **KHÔNG** verify email
3. Thử đăng nhập

**Expected Response:**
```json
{
  "status": "error",
  "message": "Email chưa được xác nhận. Vui lòng kiểm tra email của bạn."
}
```

---

### Test 2: Sử dụng token hết hạn

1. Đợi 15 phút sau khi lấy access token
2. Thử gọi API `/me`

**Expected Response:**
```json
{
  "status": "error",
  "message": "Token không hợp lệ hoặc đã hết hạn"
}
```

---

### Test 3: Truy cập API không có quyền

1. Đăng nhập với user không có role ADMIN
2. Thử gọi API `/admin/permissions`

**Expected Response:**
```json
{
  "status": "error",
  "message": "Bạn không có vai trò phù hợp. Cần một trong: ADMIN"
}
```

---

### Test 4: Sử dụng token đã revoke

1. Đăng xuất (logout)
2. Thử sử dụng refresh token đã logout

**Expected Response:**
```json
{
  "status": "error",
  "message": "Refresh token đã bị thu hồi hoặc không hợp lệ"
}
```

---

## 📋 Postman Environment Variables

Tạo Environment trong Postman với các biến sau:

```
base_url = http://localhost:5000/api/v2/auth
access_token = (sẽ được set tự động)
refresh_token = (sẽ được set tự động)
user_id = (sẽ được set tự động)
```

**Script tự động lưu token sau khi login:**

Thêm vào tab "Tests" của request Login:

```javascript
// Parse response
var jsonData = pm.response.json();

// Save tokens to environment
if (jsonData.status === "success") {
    pm.environment.set("access_token", jsonData.access_token);
    pm.environment.set("refresh_token", jsonData.refresh_token);
    pm.environment.set("user_id", jsonData.user.user_id);
    
    console.log("✅ Tokens saved to environment");
}
```

Sau đó sử dụng `{{access_token}}` trong Authorization header.

---

## 🎯 Quick Test Checklist

- [ ] Đăng ký user mới
- [ ] Xác nhận email
- [ ] Đăng nhập thành công
- [ ] Lấy profile
- [ ] Refresh token
- [ ] Forgot password
- [ ] Reset password
- [ ] Đăng nhập với password mới
- [ ] Gán role ADMIN
- [ ] Test admin APIs
- [ ] Test RBAC permissions
- [ ] Đăng xuất
- [ ] Test error cases

---

## 💡 Tips

1. **Mock Email Mode:** Kiểm tra console server để lấy token
2. **Token Expiry:** Access token hết hạn sau 15 phút
3. **Database:** Kiểm tra database để verify data
4. **Logs:** Xem bảng `UserAccessLog` để theo dõi hoạt động
5. **RBAC Testing:** Cần setup roles trước khi test permissions
