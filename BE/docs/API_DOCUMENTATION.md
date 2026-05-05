# 📚 API Documentation - RBAC Authentication System

## Base URL
```
http://localhost:5000/api/v2/auth
```

---

## 🔐 Authentication Flow

### 1. Đăng ký (Register)
**Endpoint:** `POST /register`

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "phone": "0123456789",
  "dob": "1990-01-01",
  "gender": "Male"
}
```

**Response (Success - 201):**
```json
{
  "status": "success",
  "message": "Đăng ký thành công. Vui lòng kiểm tra email để xác nhận tài khoản.",
  "user_id": 1,
  "email_sent": true
}
```

**Response (Error - 400):**
```json
{
  "status": "error",
  "message": "Username hoặc Email đã tồn tại"
}
```

---

### 2. Xác nhận Email (Verify Email)
**Endpoint:** `GET /verify-email?token=xxx`

**Query Parameters:**
- `token`: Token nhận được từ email

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Email đã được xác nhận thành công"
}
```

**Response (Error - 400):**
```json
{
  "status": "error",
  "message": "Token đã hết hạn"
}
```

---

### 3. Gửi lại Email Xác nhận (Resend Verification)
**Endpoint:** `POST /resend-verification`

**Request Body:**
```json
{
  "email": "john@example.com"
}
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Email xác nhận đã được gửi lại",
  "email_sent": true
}
```

---

### 4. Đăng nhập (Login)
**Endpoint:** `POST /login`

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "SecurePass123"
}
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Đăng nhập thành công",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "user_id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "roles": ["EMPLOYEE"]
  }
}
```

**Response (Error - 401):**
```json
{
  "status": "error",
  "message": "Email chưa được xác nhận. Vui lòng kiểm tra email của bạn."
}
```

---

### 5. Làm mới Token (Refresh Token)
**Endpoint:** `POST /refresh-token`

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 6. Đăng xuất (Logout)
**Endpoint:** `POST /logout`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Đăng xuất thành công"
}
```

---

## 🔑 Password Management

### 7. Quên mật khẩu (Forgot Password)
**Endpoint:** `POST /forgot-password`

**Request Body:**
```json
{
  "email": "john@example.com"
}
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Email hướng dẫn đặt lại mật khẩu đã được gửi",
  "email_sent": true
}
```

---

### 8. Đặt lại mật khẩu (Reset Password)
**Endpoint:** `POST /reset-password`

**Request Body:**
```json
{
  "token": "abc123xyz...",
  "new_password": "NewSecurePass456"
}
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Mật khẩu đã được đặt lại thành công"
}
```

---

## 👤 User Profile

### 9. Lấy thông tin cá nhân (Get Profile)
**Endpoint:** `GET /me`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "data": {
    "user_info": {
      "UserID": 1,
      "Username": "john_doe",
      "Email": "john@example.com",
      "PhoneNumber": "0123456789",
      "DateOfBirth": "1990-01-01",
      "Gender": "Male",
      "Status": "ACTIVE",
      "EmailVerified": true,
      "CreatedAt": "2024-01-01T10:00:00"
    },
    "roles": [
      {
        "RoleID": 3,
        "RoleName": "EMPLOYEE",
        "Description": "Nhân viên thông thường"
      }
    ],
    "permissions": [
      {
        "PermissionID": 3,
        "PermissionName": "REPORT_VIEW",
        "Description": "Xem báo cáo"
      }
    ],
    "functions": [
      "REPORT_GENERATE",
      "REPORT_EXPORT"
    ]
  }
}
```

---

### 10. Lấy danh sách quyền (Get My Permissions)
**Endpoint:** `GET /me/permissions`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "data": {
    "user_id": 1,
    "permissions": [
      "REPORT_GENERATE",
      "REPORT_EXPORT"
    ]
  }
}
```

---

## 👨‍💼 Admin - User Management

### 11. Gán Role cho User (Assign Role)
**Endpoint:** `POST /admin/users/assign-role`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Required Permission:** `USER_EDIT`

**Request Body:**
```json
{
  "user_id": 5,
  "role_id": 2
}
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Gán role thành công"
}
```

**Response (Error - 403):**
```json
{
  "status": "error",
  "message": "Bạn không có quyền thực hiện chức năng này (USER_EDIT)"
}
```

---

### 12. Xóa Role khỏi User (Remove Role)
**Endpoint:** `POST /admin/users/remove-role`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Required Permission:** `USER_EDIT`

**Request Body:**
```json
{
  "user_id": 5,
  "role_id": 2
}
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Xóa role thành công"
}
```

---

### 13. Lấy Roles của User (Get User Roles)
**Endpoint:** `GET /admin/users/{user_id}/roles`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Required Permission:** `USER_VIEW`

**Response (Success - 200):**
```json
{
  "status": "success",
  "data": {
    "user_id": 5,
    "roles": [
      {
        "RoleID": 2,
        "RoleName": "HR_MANAGER",
        "Description": "Quản lý nhân sự"
      }
    ]
  }
}
```

---

## 🔧 Admin - RBAC Management

### 14. Lấy tất cả Roles (Get All Roles)
**Endpoint:** `GET /admin/roles`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Required Role:** `ADMIN` hoặc `HR_MANAGER`

**Response (Success - 200):**
```json
{
  "status": "success",
  "data": [
    {
      "RoleID": 1,
      "RoleName": "ADMIN",
      "Description": "Quản trị viên hệ thống",
      "CreatedAt": "2024-01-01T10:00:00"
    },
    {
      "RoleID": 2,
      "RoleName": "HR_MANAGER",
      "Description": "Quản lý nhân sự",
      "CreatedAt": "2024-01-01T10:00:00"
    }
  ]
}
```

---

### 15. Lấy tất cả Permissions (Get All Permissions)
**Endpoint:** `GET /admin/permissions`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Required Role:** `ADMIN`

**Response (Success - 200):**
```json
{
  "status": "success",
  "data": [
    {
      "PermissionID": 1,
      "PermissionName": "USER_MANAGEMENT",
      "Description": "Quản lý người dùng"
    },
    {
      "PermissionID": 2,
      "PermissionName": "HR_MANAGEMENT",
      "Description": "Quản lý nhân sự"
    }
  ]
}
```

---

### 16. Lấy tất cả Functions (Get All Functions)
**Endpoint:** `GET /admin/functions`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Required Role:** `ADMIN`

**Response (Success - 200):**
```json
{
  "status": "success",
  "data": [
    {
      "FunctionID": 1,
      "FunctionName": "USER_CREATE",
      "Description": "Tạo người dùng mới"
    },
    {
      "FunctionID": 2,
      "FunctionName": "USER_EDIT",
      "Description": "Chỉnh sửa thông tin người dùng"
    }
  ]
}
```

---

## 🏥 Health Check

### 17. Health Check
**Endpoint:** `GET /health`

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Enhanced Auth API is running",
  "version": "1.0.0"
}
```

---

## 🔒 Error Codes

| Status Code | Meaning |
|-------------|---------|
| 200 | Success |
| 201 | Created (Đăng ký thành công) |
| 400 | Bad Request (Thiếu thông tin hoặc dữ liệu không hợp lệ) |
| 401 | Unauthorized (Token không hợp lệ hoặc chưa đăng nhập) |
| 403 | Forbidden (Không có quyền truy cập) |
| 404 | Not Found (Không tìm thấy resource) |
| 500 | Internal Server Error (Lỗi server) |

---

## 🛡️ Security Notes

1. **Access Token:** Hết hạn sau 15 phút
2. **Refresh Token:** Hết hạn sau 7 ngày
3. **Email Verification Token:** Hết hạn sau 15 phút
4. **Password Reset Token:** Hết hạn sau 15 phút
5. **Password:** Được hash bằng bcrypt
6. **Token Format:** Bearer token trong Authorization header

---

## 📝 RBAC Hierarchy

```
USER
  └─> USER_ROLE
        └─> ROLE
              └─> ROLE_PERMISSION
                    └─> PERMISSION
                          └─> PERMISSION_FUNCTION
                                └─> SYSTEMFUNCTION
```

**Ví dụ:**
- User `john_doe` có Role `HR_MANAGER`
- Role `HR_MANAGER` có Permission `HR_MANAGEMENT`
- Permission `HR_MANAGEMENT` có Function `EMPLOYEE_EDIT`
- => User `john_doe` có quyền `EMPLOYEE_EDIT`
