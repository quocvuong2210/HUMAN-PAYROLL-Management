# 🔧 Sửa Lỗi Tạo Người Dùng - RBAC Model

## 📋 Tóm Tắt
Sửa lỗi `'RBACModel' object has no attribute 'get_role_by_id'` khi tạo người dùng mới với roles.

---

## 🐛 Lỗi Gốc

### Mô tả lỗi:
```
Lỗi server: 'RBACModel' object has no attribute 'get_role_by_id'
```

### Nguyên nhân:
- File `BE/src/services/auth_rbac_service.py` gọi method `self.rbac_model.get_role_by_id(role_id)` 
- Nhưng method này không tồn tại trong `BE/src/models/rbacModel.py`
- Dẫn đến lỗi khi tạo user và gán roles

### Vị trí lỗi:
```python
# BE/src/services/auth_rbac_service.py (line ~425)
for role_id in role_ids:
    success, msg = self.rbac_model.assign_role_to_user(user_id, role_id)
    if success:
        # Lấy role name
        role_info = self.rbac_model.get_role_by_id(role_id)  # ❌ Method không tồn tại
        if role_info:
            assigned_roles.append(role_info['RoleName'])
```

---

## ✅ Giải Pháp

### 1. Thêm method `get_role_by_id` vào RBACModel

**File:** `BE/src/models/rbacModel.py`

```python
def get_role_by_id(self, role_id):
    """Lấy thông tin role theo ID"""
    sql = "SELECT RoleID, RoleName, Description, CreatedAt FROM [ROLE] WHERE RoleID = :role_id"
    result = self._execute(sql, {"role_id": role_id}, fetch=True)
    return result[0] if result else None
```

**Vị trí:** Thêm sau method `get_all_roles()` (line ~23)

---

### 2. Thêm API endpoint để lấy danh sách roles

Frontend cần endpoint để load danh sách roles khi tạo user.

#### a) Thêm method vào Controller

**File:** `BE/src/controllers/auth_rbac_controller.py`

```python
@jwt_required
def get_all_roles(self, **kwargs):
    """
    GET /api/v1/auth/roles
    Lấy danh sách tất cả các roles (Yêu cầu đăng nhập)
    
    Headers:
        - Authorization: Bearer <access_token>
    
    Response:
        200: Danh sách roles
        401: Chưa đăng nhập
        500: Lỗi server
    """
    try:
        result = self.auth_service.get_all_roles()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Lỗi server: {str(e)}"
        }), 500
```

#### b) Thêm method vào Service

**File:** `BE/src/services/auth_rbac_service.py`

```python
def get_all_roles(self):
    """
    Lấy danh sách tất cả các roles
    
    Returns:
        dict: Response với danh sách roles
    """
    roles = self.rbac_model.get_all_roles()
    
    return {
        "status": "success",
        "data": roles
    }
```

#### c) Thêm route

**File:** `BE/src/routes/auth_rbac_route.py`

```python
# Get all roles (yêu cầu đăng nhập)
auth_rbac_bp.route('/roles', methods=['GET'])(controller.get_all_roles)
```

---

## 🧪 Kiểm Tra

### 1. Test API lấy danh sách roles

```http
GET http://localhost:5000/api/v1/auth/roles
Authorization: Bearer <your_access_token>
```

**Response mong đợi:**
```json
{
  "status": "success",
  "data": [
    {
      "RoleID": 1,
      "RoleName": "SUPER_ADMIN",
      "Description": "Quản trị viên hệ thống - Toàn quyền",
      "CreatedAt": "2024-01-01T00:00:00"
    },
    {
      "RoleID": 2,
      "RoleName": "HR_MANAGER",
      "Description": "Quản lý nhân sự - Quản lý nhân viên, chấm công",
      "CreatedAt": "2024-01-01T00:00:00"
    },
    {
      "RoleID": 3,
      "RoleName": "PAYROLL_ACCOUNTANT",
      "Description": "Kế toán lương - Tính lương, báo cáo",
      "CreatedAt": "2024-01-01T00:00:00"
    },
    {
      "RoleID": 4,
      "RoleName": "EMPLOYEE",
      "Description": "Nhân viên - Xem thông tin cá nhân",
      "CreatedAt": "2024-01-01T00:00:00"
    }
  ]
}
```

### 2. Test tạo user với roles

```http
POST http://localhost:5000/api/v1/auth/users
Authorization: Bearer <super_admin_token>
Content-Type: application/json

{
  "username": "testuser",
  "email": "testuser@company.com",
  "password": "password123",
  "phoneNumber": "0123456789",
  "dateOfBirth": "1990-01-01",
  "gender": "Nam",
  "roleIds": [2, 4]
}
```

**Response mong đợi:**
```json
{
  "status": "success",
  "message": "Tạo user thành công",
  "data": {
    "userId": 5,
    "username": "testuser",
    "email": "testuser@company.com",
    "roles": ["HR_MANAGER", "EMPLOYEE"]
  }
}
```

---

## 📝 Tóm Tắt Thay Đổi

### Files đã sửa:
1. ✅ `BE/src/models/rbacModel.py` - Thêm method `get_role_by_id()`
2. ✅ `BE/src/controllers/auth_rbac_controller.py` - Thêm method `get_all_roles()`
3. ✅ `BE/src/services/auth_rbac_service.py` - Thêm method `get_all_roles()`
4. ✅ `BE/src/routes/auth_rbac_route.py` - Thêm route `/roles`

### API Endpoints mới:
- `GET /api/v1/auth/roles` - Lấy danh sách roles (yêu cầu đăng nhập)

### Lỗi đã sửa:
- ✅ AttributeError: 'RBACModel' object has no attribute 'get_role_by_id'
- ✅ Frontend không load được danh sách roles

---

## 🎯 Kết Quả

- ✅ Tạo user mới với roles thành công
- ✅ Frontend load được danh sách roles
- ✅ Hiển thị role names trong response
- ✅ Không còn lỗi AttributeError

---

**Ngày sửa:** 2026-05-06  
**Người thực hiện:** Kiro AI Assistant
