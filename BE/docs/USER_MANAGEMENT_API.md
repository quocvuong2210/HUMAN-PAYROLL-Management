# 📚 User Management & RBAC API Documentation

## Base URLs
```
User Management: http://localhost:5000/api/v2/users
RBAC Management: http://localhost:5000/api/v2/rbac
```

---

## 🔐 Authentication
Tất cả endpoints yêu cầu Bearer token trong header:
```
Authorization: Bearer <access_token>
```

---

## 👥 USER MANAGEMENT APIs

### 1. Tạo User mới với Roles
**Endpoint:** `POST /users/create`

**Permission Required:** `USER_CREATE`

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "phone": "0123456789",
  "dob": "1990-01-01",
  "gender": "Male",
  "roles": [1, 2, 3]
}
```

**Response (Success - 201):**
```json
{
  "status": "success",
  "message": "Tạo người dùng thành công",
  "data": {
    "user_id": 5,
    "username": "john_doe",
    "email": "john@example.com",
    "assigned_roles": [1, 2, 3],
    "failed_roles": [],
    "verification_token": "abc123xyz..."
  }
}
```

---

### 2. Lấy danh sách tất cả Users
**Endpoint:** `GET /users`

**Permission Required:** `USER_VIEW`

**Response (Success - 200):**
```json
{
  "status": "success",
  "data": [
    {
      "UserID": 1,
      "Username": "admin",
      "Email": "admin@example.com",
      "PhoneNumber": "0123456789",
      "DateOfBirth": "1990-01-01",
      "Gender": "Male",
      "Status": "ACTIVE",
      "EmailVerified": true,
      "CreatedAt": "2024-01-01T10:00:00"
    }
  ]
}
```

---

### 3. Lấy thông tin chi tiết User
**Endpoint:** `GET /users/{user_id}`

**Permission Required:** `USER_VIEW`

**Response (Success - 200):**
```json
{
  "status": "success",
  "data": {
    "user_info": {
      "UserID": 1,
      "Username": "admin",
      "Email": "admin@example.com",
      "Status": "ACTIVE",
      "EmailVerified": true
    },
    "roles": [
      {
        "RoleID": 1,
        "RoleName": "ADMIN",
        "Description": "Quản trị viên hệ thống"
      }
    ],
    "permissions": [
      {
        "PermissionID": 1,
        "PermissionName": "USER_MANAGEMENT",
        "Description": "Quản lý người dùng"
      }
    ],
    "functions": [
      "USER_CREATE",
      "USER_EDIT",
      "USER_DELETE",
      "USER_VIEW"
    ]
  }
}
```

---

### 4. Cập nhật thông tin User
**Endpoint:** `PUT /users/{user_id}`

**Permission Required:** `USER_EDIT`

**Request Body:**
```json
{
  "username": "john_doe_updated",
  "email": "john_new@example.com",
  "phone": "0987654321",
  "dob": "1990-05-15",
  "gender": "Male",
  "status": "ACTIVE"
}
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Cập nhật thành công"
}
```

---

### 5. Xóa User
**Endpoint:** `DELETE /users/{user_id}`

**Permission Required:** `USER_DELETE`

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Xóa người dùng thành công"
}
```

---

## 🎭 USER ROLES MANAGEMENT

### 6. Cập nhật Roles của User
**Endpoint:** `PUT /users/{user_id}/roles`

**Permission Required:** `USER_EDIT`

**Request Body:**
```json
{
  "roles": [1, 2, 3]
}
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Cập nhật roles thành công",
  "data": {
    "assigned_roles": [1, 2, 3],
    "failed_roles": []
  }
}
```

---

### 7. Thêm Role cho User
**Endpoint:** `POST /users/{user_id}/roles`

**Permission Required:** `USER_EDIT`

**Request Body:**
```json
{
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

---

### 8. Xóa Role khỏi User
**Endpoint:** `DELETE /users/{user_id}/roles/{role_id}`

**Permission Required:** `USER_EDIT`

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Xóa role thành công"
}
```

---

## 🛡️ RBAC MANAGEMENT APIs

### 9. Lấy Permissions của Role
**Endpoint:** `GET /rbac/roles/{role_id}/permissions`

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

### 10. Cập nhật Permissions của Role
**Endpoint:** `PUT /rbac/roles/{role_id}/permissions`

**Role Required:** `ADMIN`

**Request Body:**
```json
{
  "permission_ids": [1, 2, 3, 4]
}
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Cập nhật permissions thành công",
  "data": {
    "assigned_permissions": [1, 2, 3, 4],
    "failed_permissions": []
  }
}
```

---

### 11. Thêm Permission cho Role
**Endpoint:** `POST /rbac/roles/{role_id}/permissions`

**Role Required:** `ADMIN`

**Request Body:**
```json
{
  "permission_id": 3
}
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Thêm permission thành công"
}
```

---

### 12. Xóa Permission khỏi Role
**Endpoint:** `DELETE /rbac/roles/{role_id}/permissions/{permission_id}`

**Role Required:** `ADMIN`

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Xóa permission thành công"
}
```

---

### 13. Lấy Functions của Permission
**Endpoint:** `GET /rbac/permissions/{permission_id}/functions`

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

### 14. Tạo Role mới
**Endpoint:** `POST /rbac/roles`

**Role Required:** `ADMIN`

**Request Body:**
```json
{
  "role_name": "MANAGER",
  "description": "Quản lý cấp trung"
}
```

**Response (Success - 201):**
```json
{
  "status": "success",
  "message": "Tạo role thành công"
}
```

---

### 15. Cập nhật Role
**Endpoint:** `PUT /rbac/roles/{role_id}`

**Role Required:** `ADMIN`

**Request Body:**
```json
{
  "role_name": "SENIOR_MANAGER",
  "description": "Quản lý cấp cao"
}
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Cập nhật role thành công"
}
```

---

### 16. Xóa Role
**Endpoint:** `DELETE /rbac/roles/{role_id}`

**Role Required:** `ADMIN`

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Xóa role thành công"
}
```

---

### 17. Lấy thống kê RBAC
**Endpoint:** `GET /rbac/statistics`

**Response (Success - 200):**
```json
{
  "status": "success",
  "data": {
    "total_roles": 4,
    "total_permissions": 5,
    "total_functions": 14,
    "total_user_role_assignments": 10,
    "total_role_permission_assignments": 15
  }
}
```

---

## 🔒 Error Responses

### 400 - Bad Request
```json
{
  "status": "error",
  "message": "Thiếu trường bắt buộc: username"
}
```

### 401 - Unauthorized
```json
{
  "status": "error",
  "message": "Token không hợp lệ hoặc đã hết hạn"
}
```

### 403 - Forbidden
```json
{
  "status": "error",
  "message": "Bạn không có quyền thực hiện chức năng này (USER_CREATE)"
}
```

### 404 - Not Found
```json
{
  "status": "error",
  "message": "User không tồn tại"
}
```

### 500 - Internal Server Error
```json
{
  "status": "error",
  "message": "Lỗi server: ..."
}
```

---

## 📊 RBAC Flow

```
USER
  └─> USER_ROLE
        └─> ROLE
              └─> ROLE_PERMISSION
                    └─> PERMISSION
                          └─> PERMISSION_FUNCTION
                                └─> SYSTEMFUNCTION
```

**Example:**
1. User `john_doe` có Role `HR_MANAGER`
2. Role `HR_MANAGER` có Permission `HR_MANAGEMENT`
3. Permission `HR_MANAGEMENT` có Function `EMPLOYEE_EDIT`
4. ➡️ User `john_doe` có quyền `EMPLOYEE_EDIT`

---

## 🧪 Testing với cURL

### Tạo User với Roles
```bash
curl -X POST http://localhost:5000/api/v2/users/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test123456",
    "roles": [3]
  }'
```

### Lấy danh sách Users
```bash
curl http://localhost:5000/api/v2/users \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Cập nhật Permissions của Role
```bash
curl -X PUT http://localhost:5000/api/v2/rbac/roles/2/permissions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "permission_ids": [1, 2, 3]
  }'
```

---

## 💡 Best Practices

1. **Luôn kiểm tra permissions** trước khi thực hiện thao tác quan trọng
2. **Sử dụng transactions** khi cập nhật nhiều bảng
3. **Log tất cả thao tác** liên quan đến phân quyền
4. **Validate input** để tránh SQL injection
5. **Cache permissions** trong JWT để giảm database queries
6. **Implement rate limiting** cho các API quan trọng
7. **Backup database** thường xuyên

---

## 🔐 Security Notes

- Chỉ ADMIN mới có thể thay đổi RBAC configuration
- User không thể tự gán role cho mình
- Mỗi thao tác đều được log vào UserAccessLog
- Token hết hạn sau 15 phút (access) và 7 ngày (refresh)
- Password được hash bằng bcrypt
- SQL injection protection với parameterized queries
