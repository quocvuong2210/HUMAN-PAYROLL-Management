# 🔐 RBAC Authentication System

Hệ thống xác thực và phân quyền dựa trên Role-Based Access Control (RBAC) với đầy đủ tính năng bảo mật chuẩn production.

## ✨ Features

### 🔑 Authentication
- ✅ Đăng ký với email verification
- ✅ Đăng nhập với JWT (Access + Refresh Token)
- ✅ Email verification (token hết hạn 15 phút)
- ✅ Password reset (token hết hạn 15 phút)
- ✅ Refresh token (hết hạn 7 ngày)
- ✅ Logout (revoke refresh token)
- ✅ Resend verification email

### 🛡️ Security
- ✅ Password hashing (bcrypt)
- ✅ JWT với secret keys riêng biệt
- ✅ Token expiration
- ✅ SQL injection protection (parameterized queries)
- ✅ Input validation
- ✅ User access logging

### 👥 RBAC (Role-Based Access Control)
- ✅ Multi-role support
- ✅ Permission-based authorization
- ✅ Function-level access control
- ✅ Middleware decorators (@require_permission, @require_role)
- ✅ Dynamic permission checking

### 📊 User Management
- ✅ Get user profile
- ✅ Get user permissions
- ✅ Assign/Remove roles
- ✅ View user roles
- ✅ Admin dashboard APIs

### 📧 Email Service
- ✅ Email verification
- ✅ Password reset
- ✅ Welcome email
- ✅ Mock mode for development
- ✅ SMTP support for production

### 📝 Logging
- ✅ User access logs
- ✅ Login/Logout tracking
- ✅ IP address logging
- ✅ User agent tracking

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    FLASK ROUTES                             │
│  /register, /login, /verify-email, /forgot-password, etc.  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    MIDDLEWARE                               │
│  @token_required, @require_permission, @require_role        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    CONTROLLERS                              │
│  EnhancedAuthController                                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    SERVICES                                 │
│  EnhancedAuthService, EmailService, JWTHelper               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    MODELS                                   │
│  AuthModel, RBACModel                                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    SQL SERVER                               │
│  USER, ROLE, PERMISSION, SYSTEMFUNCTION, etc.               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
BE/
├── app.py                          # Main Flask application
├── config.py                       # Configuration
├── requirement.txt                 # Dependencies
├── .env.example                    # Environment variables template
│
├── database/
│   └── rbac_system.sql            # Database schema & sample data
│
├── docs/
│   ├── API_DOCUMENTATION.md       # Complete API docs
│   ├── POSTMAN_EXAMPLES.md        # Postman testing guide
│   └── SETUP_GUIDE.md             # Installation guide
│
└── src/
    ├── controllers/
    │   └── enhanced_auth_controller.py
    │
    ├── services/
    │   └── enhanced_auth_service.py
    │
    ├── models/
    │   ├── authModel.py           # Authentication model
    │   └── rbacModel.py           # RBAC model
    │
    ├── middleware/
    │   └── rbac_middleware.py     # RBAC decorators
    │
    ├── routes/
    │   └── enhanced_auth_route.py # API routes
    │
    └── utils/
        ├── jwt_helper.py          # JWT utilities
        ├── email_service.py       # Email service
        ├── token_generator.py     # Token generation
        └── inspector.py           # Request inspection
```

---

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirement.txt

# Setup database
sqlcmd -S localhost\SQLEXPRESS -d PERMISSION -i database/rbac_system.sql

# Configure environment
cp .env.example .env
# Edit .env with your settings
```

### 2. Run Application

```bash
python app.py
```

### 3. Test API

```bash
# Health check
curl http://localhost:5000/api/v2/auth/health

# Register
curl -X POST http://localhost:5000/api/v2/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"Test123"}'
```

📖 **Full documentation:** See `docs/SETUP_GUIDE.md`

---

## 📚 API Endpoints

### Public Endpoints (No authentication required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Đăng ký user mới |
| GET | `/verify-email` | Xác nhận email |
| POST | `/resend-verification` | Gửi lại email xác nhận |
| POST | `/login` | Đăng nhập |
| POST | `/refresh-token` | Làm mới access token |
| POST | `/forgot-password` | Yêu cầu reset password |
| POST | `/reset-password` | Đặt lại password |
| GET | `/health` | Health check |

### Protected Endpoints (Require authentication)

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/logout` | Đăng xuất | - |
| GET | `/me` | Lấy profile | - |
| GET | `/me/permissions` | Lấy quyền của user | - |

### Admin Endpoints

| Method | Endpoint | Description | Permission/Role |
|--------|----------|-------------|-----------------|
| POST | `/admin/users/assign-role` | Gán role | USER_EDIT |
| POST | `/admin/users/remove-role` | Xóa role | USER_EDIT |
| GET | `/admin/users/{id}/roles` | Xem roles | USER_VIEW |
| GET | `/admin/roles` | Danh sách roles | ADMIN/HR_MANAGER |
| GET | `/admin/permissions` | Danh sách permissions | ADMIN |
| GET | `/admin/functions` | Danh sách functions | ADMIN |

📖 **Full API docs:** See `docs/API_DOCUMENTATION.md`

---

## 🎯 RBAC Hierarchy

```
USER
  └─> USER_ROLE
        └─> ROLE (ADMIN, HR_MANAGER, EMPLOYEE, VIEWER)
              └─> ROLE_PERMISSION
                    └─> PERMISSION (USER_MANAGEMENT, HR_MANAGEMENT, etc.)
                          └─> PERMISSION_FUNCTION
                                └─> SYSTEMFUNCTION (USER_CREATE, USER_EDIT, etc.)
```

### Example Flow

1. User `john_doe` được gán Role `HR_MANAGER`
2. Role `HR_MANAGER` có Permission `HR_MANAGEMENT`
3. Permission `HR_MANAGEMENT` có Function `EMPLOYEE_EDIT`
4. ➡️ User `john_doe` có quyền thực hiện `EMPLOYEE_EDIT`

---

## 🔒 Security Features

### Password Security
- ✅ Bcrypt hashing
- ✅ Minimum length validation
- ✅ No plain text storage

### Token Security
- ✅ Separate secrets for access & refresh tokens
- ✅ Short-lived access tokens (15 minutes)
- ✅ Long-lived refresh tokens (7 days)
- ✅ Token revocation support
- ✅ JWT signature verification

### Email Security
- ✅ Time-limited verification tokens (15 minutes)
- ✅ One-time use tokens
- ✅ Secure token generation (secrets module)

### Database Security
- ✅ Parameterized queries (SQL injection protection)
- ✅ Foreign key constraints
- ✅ Cascade deletes
- ✅ Unique constraints

### Access Control
- ✅ Role-based authorization
- ✅ Permission-based authorization
- ✅ Function-level access control
- ✅ Middleware protection

---

## 🧪 Testing

### Using Postman

1. Import collection from `docs/POSTMAN_EXAMPLES.md`
2. Set environment variables
3. Follow test flow

### Using cURL

```bash
# 1. Register
curl -X POST http://localhost:5000/api/v2/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"Test123"}'

# 2. Verify email (get token from console)
curl "http://localhost:5000/api/v2/auth/verify-email?token=YOUR_TOKEN"

# 3. Login
curl -X POST http://localhost:5000/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"Test123"}'

# 4. Get profile
curl http://localhost:5000/api/v2/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

📖 **Full testing guide:** See `docs/POSTMAN_EXAMPLES.md`

---

## 🛠️ Configuration

### Environment Variables

```env
# Database
SQL_SERVER_PERMISSION_CONN=mssql+pyodbc://...

# JWT
JWT_ACCESS_SECRET=your-secret-key
JWT_REFRESH_SECRET=your-refresh-secret
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email
EMAIL_MOCK_MODE=True
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

---

## 📊 Database Tables

### Core Tables
- `USER` - User accounts
- `EmailVerification` - Email verification tokens
- `PasswordReset` - Password reset tokens
- `RefreshToken` - Refresh tokens
- `UserAccessLog` - Access logs

### RBAC Tables
- `ROLE` - Roles (ADMIN, HR_MANAGER, etc.)
- `USER_ROLE` - User-Role mapping
- `PERMISSION` - Permissions
- `SYSTEMFUNCTION` - System functions
- `ROLE_PERMISSION` - Role-Permission mapping
- `PERMISSION_FUNCTION` - Permission-Function mapping

---

## 🎨 Usage Examples

### Middleware Usage

```python
from src.middleware.rbac_middleware import token_required, require_permission, require_role

# Require authentication
@app.route('/protected')
@token_required
def protected_route(**kwargs):
    user_id = kwargs['current_user_id']
    return {"message": f"Hello user {user_id}"}

# Require specific permission
@app.route('/edit-user')
@token_required
@require_permission("USER_EDIT")
def edit_user(**kwargs):
    return {"message": "You can edit users"}

# Require specific role
@app.route('/admin-only')
@token_required
@require_role("ADMIN")
def admin_only(**kwargs):
    return {"message": "Admin access granted"}

# Require any of multiple permissions
@app.route('/view-or-edit')
@token_required
@require_any_permission("USER_VIEW", "USER_EDIT")
def view_or_edit(**kwargs):
    return {"message": "You can view or edit"}
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** Cannot connect to database
```bash
# Check ODBC driver
odbcinst -q -d

# Test connection
sqlcmd -S localhost\SQLEXPRESS -U username -P password
```

**Issue:** Token not working
```python
# Verify JWT secret is loaded
from dotenv import load_dotenv
load_dotenv()
```

**Issue:** Email not sending
```env
# Use mock mode for development
EMAIL_MOCK_MODE=True
```

📖 **Full troubleshooting:** See `docs/SETUP_GUIDE.md`

---

## 📈 Performance

- **Token Verification:** O(1) - JWT decode
- **Permission Check:** O(n) - Database query with joins
- **Login:** O(1) - Single user lookup + hash comparison
- **RBAC Query:** Optimized with proper indexes

### Recommended Indexes

```sql
CREATE INDEX idx_user_username ON [USER](Username);
CREATE INDEX idx_user_email ON [USER](Email);
CREATE INDEX idx_user_role_user ON [USER_ROLE](UserID);
CREATE INDEX idx_refresh_token ON [RefreshToken](Token);
```

---

## 🔄 Migration from Old System

### Step 1: Run new database script
```bash
sqlcmd -S localhost\SQLEXPRESS -d PERMISSION -i database/rbac_system.sql
```

### Step 2: Update app.py
```python
from src.routes.enhanced_auth_route import enhanced_auth_bp
app.register_blueprint(enhanced_auth_bp, url_prefix="/api/v2/auth")
```

### Step 3: Update frontend
```javascript
// Old: /api/v1/auth/login
// New: /api/v2/auth/login

// Add refresh token handling
const refreshAccessToken = async (refreshToken) => {
  const response = await fetch('/api/v2/auth/refresh-token', {
    method: 'POST',
    body: JSON.stringify({ refresh_token: refreshToken })
  });
  return response.json();
};
```

---

## 📝 TODO / Roadmap

- [ ] Rate limiting
- [ ] Account lockout after failed attempts
- [ ] Two-factor authentication (2FA)
- [ ] OAuth integration (Google, Facebook)
- [ ] Password strength meter
- [ ] Session management
- [ ] Audit logs
- [ ] Admin dashboard UI
- [ ] API documentation with Swagger
- [ ] Unit tests
- [ ] Integration tests

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is for educational purposes.

---

## 👨‍💻 Author

Senior Backend Developer

---

## 📞 Support

- 📖 Documentation: `docs/`
- 🐛 Issues: Create an issue
- 💬 Questions: Contact support

---

## 🙏 Acknowledgments

- Flask Framework
- SQLAlchemy
- PyJWT
- Bcrypt
- Python Community

---

**⭐ If you find this project helpful, please give it a star!**
