# 🚀 Setup Guide - RBAC Authentication System

## 📋 Prerequisites

- Python 3.8+
- SQL Server 2019+
- ODBC Driver 17 for SQL Server
- pip (Python package manager)

---

## 🔧 Installation Steps

### 1. Clone Repository

```bash
cd BE
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirement.txt
```

### 4. Setup Database

#### 4.1. Tạo Database

```sql
-- Tạo database PERMISSION (nếu chưa có)
CREATE DATABASE PERMISSION;
GO

USE PERMISSION;
GO
```

#### 4.2. Chạy SQL Script

Chạy file `database/rbac_system.sql` để tạo các bảng và dữ liệu mẫu:

```bash
# Sử dụng SQL Server Management Studio (SSMS)
# Hoặc command line:
sqlcmd -S localhost\SQLEXPRESS -d PERMISSION -i database/rbac_system.sql
```

#### 4.3. Kiểm tra Tables

```sql
-- Kiểm tra các bảng đã được tạo
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;

-- Expected tables:
-- EmailVerification
-- PasswordReset
-- RefreshToken
-- ROLE
-- USER_ROLE
-- PERMISSION
-- SYSTEMFUNCTION
-- ROLE_PERMISSION
-- PERMISSION_FUNCTION
-- USER (nếu chưa có)
-- UserAccessLog (nếu chưa có)
```

### 5. Configure Environment Variables

#### 5.1. Copy .env.example

```bash
cp .env.example .env
```

#### 5.2. Update .env file

```env
# Database
SQL_SERVER_PERMISSION_CONN=mssql+pyodbc://YOUR_USERNAME:YOUR_PASSWORD@localhost\\SQLEXPRESS/PERMISSION?driver=ODBC+Driver+17+for+SQL+Server

# JWT Secrets (CHANGE THESE!)
JWT_ACCESS_SECRET=your-super-secret-access-key-change-this
JWT_REFRESH_SECRET=your-super-secret-refresh-key-change-this

# Email (Development)
EMAIL_MOCK_MODE=True
```

**⚠️ IMPORTANT:** Thay đổi JWT secrets trong production!

### 6. Update config.py

Đảm bảo `config.py` sử dụng environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

SQL_SERVER_PERMISSION_CONN = os.getenv(
    'SQL_SERVER_PERMISSION_CONN',
    'mssql+pyodbc://sang:Sang17102005@localhost\\SQLEXPRESS/PERMISSION?driver=ODBC+Driver+17+for+SQL+Server'
)
```

### 7. Run Application

```bash
python app.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### 8. Test Health Check

```bash
curl http://localhost:5000/api/v2/auth/health
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Enhanced Auth API is running",
  "version": "1.0.0"
}
```

---

## 🗄️ Database Schema

### Core Tables

```
USER
├── UserID (PK)
├── Username (UNIQUE)
├── Password (HASHED)
├── Email (UNIQUE)
├── EmailVerified (BIT)
├── Status (ACTIVE/INACTIVE)
└── ...

EmailVerification
├── Id (PK)
├── UserID (FK -> USER)
├── Token (UNIQUE)
└── ExpiredAt

PasswordReset
├── Id (PK)
├── UserID (FK -> USER)
├── Token (UNIQUE)
├── ExpiredAt
└── IsUsed

RefreshToken
├── Id (PK)
├── UserID (FK -> USER)
├── Token (UNIQUE)
├── ExpiredAt
└── IsRevoked

ROLE
├── RoleID (PK)
├── RoleName (UNIQUE)
└── Description

USER_ROLE
├── Id (PK)
├── UserID (FK -> USER)
└── RoleID (FK -> ROLE)

PERMISSION
├── PermissionID (PK)
├── PermissionName (UNIQUE)
└── Description

SYSTEMFUNCTION
├── FunctionID (PK)
├── FunctionName (UNIQUE)
└── Description

ROLE_PERMISSION
├── Id (PK)
├── RoleID (FK -> ROLE)
└── PermissionID (FK -> PERMISSION)

PERMISSION_FUNCTION
├── Id (PK)
├── PermissionID (FK -> PERMISSION)
└── FunctionID (FK -> SYSTEMFUNCTION)

UserAccessLog
├── Id (PK)
├── UserID (FK -> USER)
├── Action
├── IPAddress
├── UserAgent
└── AccessTime
```

---

## 🎭 Sample Data

### Roles
- **ADMIN**: Quản trị viên hệ thống (Full access)
- **HR_MANAGER**: Quản lý nhân sự
- **EMPLOYEE**: Nhân viên thông thường
- **VIEWER**: Chỉ xem thông tin

### Permissions
- **USER_MANAGEMENT**: Quản lý người dùng
- **HR_MANAGEMENT**: Quản lý nhân sự
- **REPORT_VIEW**: Xem báo cáo
- **SALARY_MANAGEMENT**: Quản lý lương
- **ATTENDANCE_MANAGEMENT**: Quản lý chấm công

### Functions
- USER_CREATE, USER_EDIT, USER_DELETE, USER_VIEW
- EMPLOYEE_CREATE, EMPLOYEE_EDIT, EMPLOYEE_DELETE, EMPLOYEE_VIEW
- REPORT_GENERATE, REPORT_EXPORT
- SALARY_VIEW, SALARY_EDIT
- ATTENDANCE_VIEW, ATTENDANCE_EDIT

---

## 🧪 Testing

### 1. Create Test User

```bash
curl -X POST http://localhost:5000/api/v2/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test123456"
  }'
```

### 2. Check Console for Verification Token

```
📧 EMAIL MOCK MODE
To: test@example.com
Subject: Xác nhận đăng ký tài khoản
...
http://localhost:5000/api/v2/auth/verify-email?token=ABC123XYZ...
```

### 3. Verify Email

```bash
curl "http://localhost:5000/api/v2/auth/verify-email?token=ABC123XYZ..."
```

### 4. Login

```bash
curl -X POST http://localhost:5000/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "Test123456"
  }'
```

### 5. Assign ADMIN Role (via SQL)

```sql
-- Get UserID
SELECT UserID FROM [USER] WHERE Username = 'testuser';

-- Assign ADMIN role (RoleID = 1)
INSERT INTO [USER_ROLE] (UserID, RoleID)
VALUES (1, 1);
```

### 6. Test Protected Endpoint

```bash
curl http://localhost:5000/api/v2/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🔐 Security Checklist

### Development
- [x] Email mock mode enabled
- [x] Debug mode enabled
- [x] Simple JWT secrets

### Production
- [ ] Email mock mode **DISABLED**
- [ ] Debug mode **DISABLED**
- [ ] Strong JWT secrets (64+ characters)
- [ ] HTTPS enabled
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] SQL injection protection (using parameterized queries)
- [ ] Input validation
- [ ] Password complexity requirements
- [ ] Token expiration configured
- [ ] Database backups enabled
- [ ] Logging and monitoring

---

## 📧 Email Configuration (Production)

### Gmail Setup

1. **Enable 2-Factor Authentication**
2. **Generate App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other"
   - Copy the generated password

3. **Update .env:**
```env
EMAIL_MOCK_MODE=False
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@yourcompany.com
```

### Other SMTP Providers

**SendGrid:**
```env
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key
```

**Mailgun:**
```env
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=postmaster@your-domain.mailgun.org
SMTP_PASSWORD=your-mailgun-password
```

---

## 🐛 Troubleshooting

### Issue: Cannot connect to SQL Server

**Solution:**
```bash
# Check ODBC Driver
odbcinst -q -d

# Install ODBC Driver 17 (Windows)
# Download from: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

# Test connection
sqlcmd -S localhost\SQLEXPRESS -U your_username -P your_password
```

### Issue: Import errors

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirement.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

### Issue: Token not working

**Solution:**
```python
# Check JWT secret consistency
# Ensure .env is loaded
from dotenv import load_dotenv
load_dotenv()
```

### Issue: Email not sending

**Solution:**
```bash
# Check mock mode
EMAIL_MOCK_MODE=True  # For development

# Check SMTP credentials
# Test with telnet:
telnet smtp.gmail.com 587
```

---

## 📚 Next Steps

1. ✅ Complete setup
2. ✅ Test all endpoints
3. 📖 Read API Documentation
4. 🧪 Run Postman tests
5. 🔐 Configure production security
6. 📧 Setup real email service
7. 🚀 Deploy to production

---

## 🆘 Support

- **Documentation:** `docs/API_DOCUMENTATION.md`
- **Postman Guide:** `docs/POSTMAN_EXAMPLES.md`
- **Database Script:** `database/rbac_system.sql`

---

## 📝 License

This project is for educational purposes.
