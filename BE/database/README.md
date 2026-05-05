# 🗄️ Database Setup Guide

## 📋 Quick Start

Chỉ cần chạy **1 file duy nhất** để setup toàn bộ database:

```sql
MASTER_DATABASE_SETUP.sql
```

## 🚀 Cách Sử Dụng

### Bước 1: Mở SQL Server Management Studio (SSMS)

### Bước 2: Mở file
- File → Open → File
- Chọn: `MASTER_DATABASE_SETUP.sql`

### Bước 3: Execute
- Nhấn F5 hoặc click Execute
- Đợi script chạy xong (khoảng 5-10 giây)

### Bước 4: Verify
Script sẽ tự động hiển thị thống kê:
- Total Users
- Total Roles
- Total Permissions
- Total Functions
- Assignments

## 📦 Nội Dung File

File `MASTER_DATABASE_SETUP.sql` bao gồm:

### 1. Create Database
- Tạo database `PermissionDB`
- Drop database cũ nếu tồn tại

### 2. Create Tables (13 tables)
- USER, ROLE, USER_ROLE
- PERMISSION, ROLE_PERMISSION
- SYSTEMFUNCTION, PERMISSION_FUNCTION
- ACCESS_LOG
- OTP_VERIFICATION, OTP_RESEND_LOG
- EmailVerification, PasswordReset, RefreshToken

### 3. Create Indexes (9 indexes)
- Tối ưu performance cho queries

### 4. Insert Master Data
- **4 Roles:**
  - SUPER_ADMIN (Toàn quyền)
  - HR_MANAGER (Quản lý nhân sự)
  - PAYROLL_ACCOUNTANT (Kế toán lương)
  - EMPLOYEE (Nhân viên)

- **5 Permissions:**
  - HR_MANAGEMENT
  - TIMEKEEPING
  - PAYROLL_MANAGEMENT
  - REPORTING
  - SELF_SERVICE

- **20 System Functions:**
  - USER_VIEW, USER_CREATE, USER_EDIT, USER_DELETE
  - DEPT_MANAGE, POSITION_MANAGE
  - ATTENDANCE_VIEW, ATTENDANCE_EDIT, ATTENDANCE_EXPORT, ATTENDANCE_CHECKIN
  - SALARY_VIEW_OWN, SALARY_VIEW_ALL, SALARY_CALCULATE, SALARY_LOCK, PAYSLIP_GENERATE
  - REPORT_HR_VIEW, REPORT_PAYROLL_VIEW, REPORT_PERSONAL_VIEW
  - PROFILE_VIEW, PROFILE_EDIT, PASSWORD_CHANGE

### 5. Create Sample Users
| Username | Password | Role | Email |
|----------|----------|------|-------|
| admin | admin123 | SUPER_ADMIN | admin@company.com |
| hr_manager | admin123 | HR_MANAGER | hr@company.com |
| accountant | admin123 | PAYROLL_ACCOUNTANT | accountant@company.com |
| employee | admin123 | EMPLOYEE | employee@company.com |

### 6. Create Stored Procedures (4 procedures)
- `sp_CleanupExpiredOTP` - Xóa OTP hết hạn
- `sp_CheckOTPResendCooldown` - Kiểm tra cooldown gửi lại OTP
- `sp_GetUserDetails` - Lấy thông tin user đầy đủ
- `sp_CheckUserFunction` - Kiểm tra quyền của user

### 7. Insert Sample Access Logs
- 5 sample logs để test

### 8. Verification Queries
- Hiển thị thống kê sau khi setup

## 🔐 Sample Users

Sau khi chạy script, bạn có thể login với:

### Super Admin
```
Username: admin
Password: admin123
Role: SUPER_ADMIN
Permissions: ALL
```

### HR Manager
```
Username: hr_manager
Password: admin123
Role: HR_MANAGER
Permissions: HR_MANAGEMENT, TIMEKEEPING, REPORTING, SELF_SERVICE
```

### Accountant
```
Username: accountant
Password: admin123
Role: PAYROLL_ACCOUNTANT
Permissions: PAYROLL_MANAGEMENT, REPORTING, SELF_SERVICE
```

### Employee
```
Username: employee
Password: admin123
Role: EMPLOYEE
Permissions: SELF_SERVICE
```

## 🛠️ Stored Procedures Usage

### Get User Details
```sql
EXEC sp_GetUserDetails @UserID = 1;
```
Returns:
- User info
- Roles
- Permissions
- Functions

### Check User Function
```sql
EXEC sp_CheckUserFunction @UserID = 1, @FunctionName = 'USER_EDIT';
```
Returns: 1 (có quyền) hoặc 0 (không có quyền)

### Cleanup Expired OTP
```sql
EXEC sp_CleanupExpiredOTP;
```
Xóa tất cả OTP đã hết hạn hoặc đã sử dụng

### Check OTP Resend Cooldown
```sql
EXEC sp_CheckOTPResendCooldown @Email = 'user@example.com', @CooldownSeconds = 60;
```
Returns: CanResend (1/0) và SecondsRemaining

## 📊 Verification Queries

### Check All Users
```sql
SELECT * FROM [USER];
```

### Check User Roles
```sql
SELECT 
    U.Username,
    R.RoleName
FROM [USER] U
INNER JOIN [USER_ROLE] UR ON U.UserID = UR.UserID
INNER JOIN [ROLE] R ON UR.RoleID = R.RoleID;
```

### Check User Permissions
```sql
SELECT 
    U.Username,
    P.PermissionName
FROM [USER] U
INNER JOIN [USER_ROLE] UR ON U.UserID = UR.UserID
INNER JOIN [ROLE_PERMISSION] RP ON UR.RoleID = RP.RoleID
INNER JOIN [PERMISSION] P ON RP.PermissionID = P.PermissionID
WHERE U.Username = 'admin';
```

### Check User Functions
```sql
SELECT 
    U.Username,
    SF.FunctionName
FROM [USER] U
INNER JOIN [USER_ROLE] UR ON U.UserID = UR.UserID
INNER JOIN [ROLE_PERMISSION] RP ON UR.RoleID = RP.RoleID
INNER JOIN [PERMISSION_FUNCTION] PF ON RP.PermissionID = PF.PermissionID
INNER JOIN [SYSTEMFUNCTION] SF ON PF.FunctionID = SF.FunctionID
WHERE U.Username = 'admin';
```

## 🔄 Reset Database

Nếu muốn reset lại database từ đầu:

1. Chạy lại file `MASTER_DATABASE_SETUP.sql`
2. Script sẽ tự động:
   - Drop database cũ
   - Tạo database mới
   - Setup lại tất cả

## ⚠️ Lưu Ý

- **Password mặc định:** Tất cả sample users đều có password `admin123`
- **Bcrypt Hash:** Password đã được hash bằng bcrypt với cost factor 12
- **Email Verified:** Tất cả sample users đã được verify email
- **Status:** Tất cả sample users có status ACTIVE

## 📝 Changelog

### Version 1.0 (Current)
- Tập hợp tất cả SQL scripts vào 1 file
- 13 tables
- 9 indexes
- 4 roles, 5 permissions, 20 functions
- 4 sample users
- 4 stored procedures
- Sample data

---

**File:** `MASTER_DATABASE_SETUP.sql`  
**Last Updated:** 2024-09  
**Status:** ✅ Production Ready
