-- ============================================
-- MASTER DATABASE SETUP SCRIPT
-- Hệ Thống Quản Lý Nhân Sự với RBAC
-- ============================================
-- Tập hợp tất cả SQL scripts vào 1 file duy nhất
-- Chạy file này để setup toàn bộ database
-- ============================================

USE [master];
GO

-- ============================================
-- SECTION 1: CREATE DATABASE
-- ============================================

IF EXISTS (SELECT name FROM sys.databases WHERE name = N'PermissionDB')
BEGIN
    ALTER DATABASE [PERMISSION] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE [PERMISSION];
END
GO

CREATE DATABASE [PERMISSION];
GO

USE [PERMISSION];
GO

PRINT '✓ Database created successfully';
GO

-- ============================================
-- SECTION 2: CREATE TABLES
-- ============================================

-- 2.1 USER Table
CREATE TABLE [USER] (
    [UserID] INT PRIMARY KEY IDENTITY(1,1),
    [Username] NVARCHAR(50) NOT NULL UNIQUE,
    [PasswordHash] NVARCHAR(255) NOT NULL,
    [Email] NVARCHAR(100) NOT NULL UNIQUE,
    [PhoneNumber] NVARCHAR(20),
    [DateOfBirth] DATE,
    [Gender] NVARCHAR(10),
    [Status] NVARCHAR(20) DEFAULT 'ACTIVE',
    [EmailVerified] BIT DEFAULT 0,
    [CreatedAt] DATETIME DEFAULT GETDATE(),
    [LastLoginAt] DATETIME NULL,
    [FailedLoginAttempts] INT DEFAULT 0,
    [LockedUntil] DATETIME NULL
);

-- 2.2 ROLE Table
CREATE TABLE [ROLE] (
    [RoleID] INT PRIMARY KEY IDENTITY(1,1),
    [RoleName] NVARCHAR(50) NOT NULL UNIQUE,
    [Description] NVARCHAR(255),
    [CreatedAt] DATETIME DEFAULT GETDATE()
);

-- 2.3 USER_ROLE Table
CREATE TABLE [USER_ROLE] (
    [UserID] INT NOT NULL,
    [RoleID] INT NOT NULL,
    [AssignedAt] DATETIME DEFAULT GETDATE(),
    PRIMARY KEY ([UserID], [RoleID]),
    CONSTRAINT FK_UR_User FOREIGN KEY ([UserID]) REFERENCES [USER]([UserID]) ON DELETE CASCADE,
    CONSTRAINT FK_UR_Role FOREIGN KEY ([RoleID]) REFERENCES [ROLE]([RoleID])
);

-- 2.4 PERMISSION Table
CREATE TABLE [PERMISSION] (
    [PermissionID] INT PRIMARY KEY IDENTITY(1,1),
    [PermissionName] NVARCHAR(100) NOT NULL UNIQUE,
    [Description] NVARCHAR(255),
    [CreatedAt] DATETIME DEFAULT GETDATE()
);

-- 2.5 ROLE_PERMISSION Table
CREATE TABLE [ROLE_PERMISSION] (
    [RoleID] INT NOT NULL,
    [PermissionID] INT NOT NULL,
    [AssignedAt] DATETIME DEFAULT GETDATE(),
    PRIMARY KEY ([RoleID], [PermissionID]),
    CONSTRAINT FK_RP_Role FOREIGN KEY ([RoleID]) REFERENCES [ROLE]([RoleID]),
    CONSTRAINT FK_RP_Permission FOREIGN KEY ([PermissionID]) REFERENCES [PERMISSION]([PermissionID])
);

-- 2.6 SYSTEMFUNCTION Table
CREATE TABLE [SYSTEMFUNCTION] (
    [FunctionID] INT PRIMARY KEY IDENTITY(1,1),
    [FunctionName] NVARCHAR(100) NOT NULL UNIQUE,
    [Description] NVARCHAR(255),
    [CreatedAt] DATETIME DEFAULT GETDATE()
);

-- 2.7 PERMISSION_FUNCTION Table
CREATE TABLE [PERMISSION_FUNCTION] (
    [PermissionID] INT NOT NULL,
    [FunctionID] INT NOT NULL,
    [AssignedAt] DATETIME DEFAULT GETDATE(),
    PRIMARY KEY ([PermissionID], [FunctionID]),
    CONSTRAINT FK_PF_Permission FOREIGN KEY ([PermissionID]) REFERENCES [PERMISSION]([PermissionID]),
    CONSTRAINT FK_PF_Function FOREIGN KEY ([FunctionID]) REFERENCES [SYSTEMFUNCTION]([FunctionID])
);

-- 2.8 ACCESS_LOG Table
CREATE TABLE [ACCESS_LOG] (
    [LogID] INT PRIMARY KEY IDENTITY(1,1),
    [UserID] INT NOT NULL,
    [Action] NVARCHAR(50) NOT NULL,
    [IPAddress] NVARCHAR(50),
    [UserAgent] NVARCHAR(500),
    [AccessTime] DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_AccessLog_User FOREIGN KEY ([UserID]) REFERENCES [USER]([UserID]) ON DELETE CASCADE
);

-- 2.9 OTP_VERIFICATION Table
CREATE TABLE [OTP_VERIFICATION] (
    [Id] INT PRIMARY KEY IDENTITY(1,1),
    [Email] NVARCHAR(255) NOT NULL,
    [OTPCode] NVARCHAR(10) NOT NULL,
    [ExpiredAt] DATETIME NOT NULL,
    [IsUsed] BIT DEFAULT 0,
    [CreatedAt] DATETIME DEFAULT GETDATE(),
    [UsedAt] DATETIME NULL
);

-- 2.10 OTP_RESEND_LOG Table
CREATE TABLE [OTP_RESEND_LOG] (
    [Id] INT PRIMARY KEY IDENTITY(1,1),
    [Email] NVARCHAR(255) NOT NULL,
    [RequestedAt] DATETIME DEFAULT GETDATE(),
    [IPAddress] NVARCHAR(50)
);

-- 2.11 EmailVerification Table
CREATE TABLE [EmailVerification] (
    [Id] INT PRIMARY KEY IDENTITY(1,1),
    [UserID] INT NOT NULL,
    [Token] NVARCHAR(255) NOT NULL UNIQUE,
    [ExpiredAt] DATETIME NOT NULL,
    [CreatedAt] DATETIME DEFAULT GETDATE(),
    FOREIGN KEY ([UserID]) REFERENCES [USER]([UserID]) ON DELETE CASCADE
);

-- 2.12 PasswordReset Table
CREATE TABLE [PasswordReset] (
    [Id] INT PRIMARY KEY IDENTITY(1,1),
    [UserID] INT NOT NULL,
    [Token] NVARCHAR(255) NOT NULL UNIQUE,
    [ExpiredAt] DATETIME NOT NULL,
    [CreatedAt] DATETIME DEFAULT GETDATE(),
    [IsUsed] BIT DEFAULT 0,
    FOREIGN KEY ([UserID]) REFERENCES [USER]([UserID]) ON DELETE CASCADE
);

-- 2.13 RefreshToken Table
CREATE TABLE [RefreshToken] (
    [Id] INT PRIMARY KEY IDENTITY(1,1),
    [UserID] INT NOT NULL,
    [Token] NVARCHAR(500) NOT NULL UNIQUE,
    [ExpiredAt] DATETIME NOT NULL,
    [CreatedAt] DATETIME DEFAULT GETDATE(),
    [IsRevoked] BIT DEFAULT 0,
    FOREIGN KEY ([UserID]) REFERENCES [USER]([UserID]) ON DELETE CASCADE
);

PRINT '✓ All tables created successfully';
GO

-- ============================================
-- SECTION 3: CREATE INDEXES
-- ============================================

CREATE INDEX idx_user_email ON [USER](Email);
CREATE INDEX idx_user_username ON [USER](Username);
CREATE INDEX idx_user_status ON [USER](Status);
CREATE INDEX IX_AccessLog_UserID ON [ACCESS_LOG](UserID);
CREATE INDEX IX_AccessLog_AccessTime ON [ACCESS_LOG](AccessTime DESC);
CREATE INDEX idx_otp_email ON [OTP_VERIFICATION](Email);
CREATE INDEX idx_otp_code ON [OTP_VERIFICATION](OTPCode);
CREATE INDEX idx_otp_expired ON [OTP_VERIFICATION](ExpiredAt);
CREATE INDEX idx_email_time ON [OTP_RESEND_LOG](Email, RequestedAt);

PRINT '✓ Indexes created successfully';
GO

-- ============================================
-- SECTION 4: INSERT MASTER DATA
-- ============================================

-- 4.1 ROLES
INSERT INTO [ROLE] ([RoleName], [Description]) VALUES 
('SUPER_ADMIN', 'Quản trị viên hệ thống - Toàn quyền'),
('HR_MANAGER', 'Quản lý nhân sự - Quản lý nhân viên, chấm công'),
('PAYROLL_ACCOUNTANT', 'Kế toán lương - Tính lương, báo cáo'),
('EMPLOYEE', 'Nhân viên - Xem thông tin cá nhân');

-- 4.2 PERMISSIONS
INSERT INTO [PERMISSION] ([PermissionName], [Description]) VALUES 
('HR_MANAGEMENT', 'Quản trị nhân sự - Quản lý user, phòng ban, chức vụ'),
('TIMEKEEPING', 'Chấm công - Quản lý chấm công'),
('PAYROLL_MANAGEMENT', 'Tính lương - Quản lý lương, phiếu lương'),
('REPORTING', 'Báo cáo - Xem và tạo báo cáo'),
('SELF_SERVICE', 'Tự phục vụ - Xem thông tin cá nhân, chấm công, lương của bản thân');

-- 4.3 SYSTEM FUNCTIONS
INSERT INTO [SYSTEMFUNCTION] ([FunctionName], [Description]) VALUES 
-- User Management
('USER_VIEW', 'Xem danh sách người dùng'),
('USER_CREATE', 'Tạo người dùng mới'),
('USER_EDIT', 'Chỉnh sửa người dùng'),
('USER_DELETE', 'Xóa người dùng'),

-- Department & Position
('DEPT_MANAGE', 'Quản lý phòng ban'),
('POSITION_MANAGE', 'Quản lý chức vụ'),

-- Attendance
('ATTENDANCE_VIEW', 'Xem chấm công'),
('ATTENDANCE_EDIT', 'Chỉnh sửa chấm công'),
('ATTENDANCE_EXPORT', 'Xuất dữ liệu chấm công'),
('ATTENDANCE_CHECKIN', 'Chấm công (check in/out)'),

-- Salary
('SALARY_VIEW_OWN', 'Xem lương của bản thân'),
('SALARY_VIEW_ALL', 'Xem lương tất cả nhân viên'),
('SALARY_CALCULATE', 'Tính lương'),
('SALARY_LOCK', 'Khóa bảng lương'),
('PAYSLIP_GENERATE', 'Tạo phiếu lương'),

-- Reports
('REPORT_HR_VIEW', 'Xem báo cáo nhân sự'),
('REPORT_PAYROLL_VIEW', 'Xem báo cáo lương'),
('REPORT_PERSONAL_VIEW', 'Xem báo cáo cá nhân'),

-- Profile
('PROFILE_VIEW', 'Xem thông tin cá nhân'),
('PROFILE_EDIT', 'Chỉnh sửa thông tin cá nhân'),
('PASSWORD_CHANGE', 'Đổi mật khẩu');

-- 4.4 PERMISSION_FUNCTION Mapping
INSERT INTO [PERMISSION_FUNCTION] ([PermissionID], [FunctionID])
SELECT P.PermissionID, F.FunctionID
FROM [PERMISSION] P, [SYSTEMFUNCTION] F
WHERE 
    -- HR_MANAGEMENT
    (P.PermissionName = 'HR_MANAGEMENT' AND F.FunctionName IN (
        'USER_VIEW', 'USER_CREATE', 'USER_EDIT', 'USER_DELETE',
        'DEPT_MANAGE', 'POSITION_MANAGE'
    ))
    OR
    -- TIMEKEEPING
    (P.PermissionName = 'TIMEKEEPING' AND F.FunctionName IN (
        'ATTENDANCE_VIEW', 'ATTENDANCE_EDIT', 'ATTENDANCE_EXPORT', 'ATTENDANCE_CHECKIN'
    ))
    OR
    -- PAYROLL_MANAGEMENT
    (P.PermissionName = 'PAYROLL_MANAGEMENT' AND F.FunctionName IN (
        'SALARY_VIEW_ALL', 'SALARY_CALCULATE', 'SALARY_LOCK', 'PAYSLIP_GENERATE'
    ))
    OR
    -- REPORTING
    (P.PermissionName = 'REPORTING' AND F.FunctionName IN (
        'REPORT_HR_VIEW', 'REPORT_PAYROLL_VIEW'
    ))
    OR
    -- SELF_SERVICE (for EMPLOYEE)
    (P.PermissionName = 'SELF_SERVICE' AND F.FunctionName IN (
        'PROFILE_VIEW', 'PROFILE_EDIT', 'PASSWORD_CHANGE',
        'SALARY_VIEW_OWN', 'ATTENDANCE_CHECKIN', 'ATTENDANCE_VIEW',
        'REPORT_PERSONAL_VIEW'
    ));

-- 4.5 ROLE_PERMISSION Mapping
INSERT INTO [ROLE_PERMISSION] ([RoleID], [PermissionID])
SELECT R.RoleID, P.PermissionID
FROM [ROLE] R, [PERMISSION] P
WHERE 
    -- SUPER_ADMIN: Tất cả quyền
    (R.RoleName = 'SUPER_ADMIN')
    OR
    -- HR_MANAGER: HR, Timekeeping, Reporting, Self Service
    (R.RoleName = 'HR_MANAGER' AND P.PermissionName IN (
        'HR_MANAGEMENT', 'TIMEKEEPING', 'REPORTING', 'SELF_SERVICE'
    ))
    OR
    -- PAYROLL_ACCOUNTANT: Payroll, Reporting, Self Service
    (R.RoleName = 'PAYROLL_ACCOUNTANT' AND P.PermissionName IN (
        'PAYROLL_MANAGEMENT', 'REPORTING', 'SELF_SERVICE'
    ))
    OR
    -- EMPLOYEE: Chỉ Self Service
    (R.RoleName = 'EMPLOYEE' AND P.PermissionName = 'SELF_SERVICE');

PRINT '✓ Master data inserted successfully';
GO

-- ============================================
-- SECTION 5: CREATE SAMPLE USERS
-- ============================================

-- Password: admin123 (bcrypt hashed)
INSERT INTO [USER] ([Username], [PasswordHash], [Email], [Status], [EmailVerified]) VALUES
('admin', '$2b$12$W3mD38T06UqLNOHQkavvReypqMe/FqNeHnnN5Q0SvJdvlKmM6lSkS', 'admin@company.com', 'ACTIVE', 1),
('hr_manager', '$2b$12$W3mD38T06UqLNOHQkavvReypqMe/FqNeHnnN5Q0SvJdvlKmM6lSkS', 'hr@company.com', 'ACTIVE', 1),
('accountant', '$2b$12$W3mD38T06UqLNOHQkavvReypqMe/FqNeHnnN5Q0SvJdvlKmM6lSkS', 'accountant@company.com', 'ACTIVE', 1),
('employee', '$2b$12$W3mD38T06UqLNOHQkavvReypqMe/FqNeHnnN5Q0SvJdvlKmM6lSkS', 'employee@company.com', 'ACTIVE', 1);

-- Assign roles to sample users
INSERT INTO [USER_ROLE] ([UserID], [RoleID])
SELECT U.UserID, R.RoleID
FROM [USER] U, [ROLE] R
WHERE 
    (U.Username = 'admin' AND R.RoleName = 'SUPER_ADMIN')
    OR (U.Username = 'hr_manager' AND R.RoleName = 'HR_MANAGER')
    OR (U.Username = 'accountant' AND R.RoleName = 'PAYROLL_ACCOUNTANT')
    OR (U.Username = 'employee' AND R.RoleName = 'EMPLOYEE');

PRINT '✓ Sample users created successfully';
GO

-- ============================================
-- SECTION 6: CREATE STORED PROCEDURES
-- ============================================

-- 6.1 Cleanup expired OTP
CREATE OR ALTER PROCEDURE sp_CleanupExpiredOTP
AS
BEGIN
    DELETE FROM [OTP_VERIFICATION]
    WHERE ExpiredAt < GETDATE() OR IsUsed = 1;
    
    -- Cleanup old resend logs (older than 24 hours)
    DELETE FROM [OTP_RESEND_LOG]
    WHERE RequestedAt < DATEADD(HOUR, -24, GETDATE());
    
    PRINT 'Expired OTP cleaned up';
END;
GO

-- 6.2 Check OTP resend cooldown
CREATE OR ALTER PROCEDURE sp_CheckOTPResendCooldown
    @Email NVARCHAR(255),
    @CooldownSeconds INT = 60
AS
BEGIN
    DECLARE @LastRequestTime DATETIME;
    DECLARE @CanResend BIT = 0;
    
    SELECT TOP 1 @LastRequestTime = RequestedAt
    FROM [OTP_RESEND_LOG]
    WHERE Email = @Email
    ORDER BY RequestedAt DESC;
    
    IF @LastRequestTime IS NULL OR DATEDIFF(SECOND, @LastRequestTime, GETDATE()) >= @CooldownSeconds
    BEGIN
        SET @CanResend = 1;
    END
    
    SELECT @CanResend AS CanResend, 
           CASE 
               WHEN @LastRequestTime IS NULL THEN 0
               ELSE @CooldownSeconds - DATEDIFF(SECOND, @LastRequestTime, GETDATE())
           END AS SecondsRemaining;
END;
GO

-- 6.3 Get user with roles, permissions, and functions
CREATE OR ALTER PROCEDURE sp_GetUserDetails
    @UserID INT
AS
BEGIN
    -- User info
    SELECT 
        U.UserID,
        U.Username,
        U.Email,
        U.PhoneNumber,
        U.DateOfBirth,
        U.Gender,
        U.Status,
        U.EmailVerified,
        U.CreatedAt,
        U.LastLoginAt
    FROM [USER] U
    WHERE U.UserID = @UserID;
    
    -- Roles
    SELECT 
        R.RoleID,
        R.RoleName,
        R.Description
    FROM [USER_ROLE] UR
    INNER JOIN [ROLE] R ON UR.RoleID = R.RoleID
    WHERE UR.UserID = @UserID;
    
    -- Permissions
    SELECT DISTINCT 
        P.PermissionID,
        P.PermissionName,
        P.Description
    FROM [USER_ROLE] UR
    INNER JOIN [ROLE_PERMISSION] RP ON UR.RoleID = RP.RoleID
    INNER JOIN [PERMISSION] P ON RP.PermissionID = P.PermissionID
    WHERE UR.UserID = @UserID;
    
    -- Functions
    SELECT DISTINCT 
        SF.FunctionID,
        SF.FunctionName,
        SF.Description
    FROM [USER_ROLE] UR
    INNER JOIN [ROLE_PERMISSION] RP ON UR.RoleID = RP.RoleID
    INNER JOIN [PERMISSION_FUNCTION] PF ON RP.PermissionID = PF.PermissionID
    INNER JOIN [SYSTEMFUNCTION] SF ON PF.FunctionID = SF.FunctionID
    WHERE UR.UserID = @UserID;
END;
GO

-- 6.4 Check if user has specific function
CREATE OR ALTER PROCEDURE sp_CheckUserFunction
    @UserID INT,
    @FunctionName NVARCHAR(100)
AS
BEGIN
    SELECT 
        CASE 
            WHEN EXISTS (
                SELECT 1 
                FROM [USER_ROLE] UR
                INNER JOIN [ROLE_PERMISSION] RP ON UR.RoleID = RP.RoleID
                INNER JOIN [PERMISSION_FUNCTION] PF ON RP.PermissionID = PF.PermissionID
                INNER JOIN [SYSTEMFUNCTION] SF ON PF.FunctionID = SF.FunctionID
                WHERE UR.UserID = @UserID AND SF.FunctionName = @FunctionName
            ) THEN 1
            ELSE 0
        END AS HasFunction;
END;
GO

PRINT '✓ Stored procedures created successfully';
GO

-- ============================================
-- SECTION 7: INSERT SAMPLE ACCESS LOGS
-- ============================================

INSERT INTO [ACCESS_LOG] (UserID, Action, IPAddress, UserAgent, AccessTime)
VALUES 
    (1, 'LOGIN_SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', DATEADD(MINUTE, -30, GETDATE())),
    (1, 'PROFILE_UPDATED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', DATEADD(MINUTE, -20, GETDATE())),
    (1, 'LOGIN_SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', DATEADD(MINUTE, -10, GETDATE())),
    (2, 'LOGIN_SUCCESS', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', DATEADD(MINUTE, -5, GETDATE())),
    (2, 'LOGIN_FAILED', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', DATEADD(MINUTE, -3, GETDATE()));

PRINT '✓ Sample access logs inserted';
GO

-- ============================================
-- SECTION 8: VERIFICATION QUERIES
-- ============================================

PRINT '';
PRINT '========================================';
PRINT 'DATABASE SETUP COMPLETED SUCCESSFULLY!';
PRINT '========================================';
PRINT '';
PRINT 'Sample Users Created:';
PRINT '  - admin / admin123 (SUPER_ADMIN)';
PRINT '  - hr_manager / admin123 (HR_MANAGER)';
PRINT '  - accountant / admin123 (PAYROLL_ACCOUNTANT)';
PRINT '  - employee / admin123 (EMPLOYEE)';
PRINT '';
PRINT 'Statistics:';

SELECT 
    (SELECT COUNT(*) FROM [USER]) AS TotalUsers,
    (SELECT COUNT(*) FROM [ROLE]) AS TotalRoles,
    (SELECT COUNT(*) FROM [PERMISSION]) AS TotalPermissions,
    (SELECT COUNT(*) FROM [SYSTEMFUNCTION]) AS TotalFunctions,
    (SELECT COUNT(*) FROM [USER_ROLE]) AS UserRoleAssignments,
    (SELECT COUNT(*) FROM [ROLE_PERMISSION]) AS RolePermissionAssignments,
    (SELECT COUNT(*) FROM [PERMISSION_FUNCTION]) AS PermissionFunctionAssignments;

PRINT '';
PRINT 'Useful Stored Procedures:';
PRINT '  - EXEC sp_GetUserDetails @UserID = 1';
PRINT '  - EXEC sp_CheckUserFunction @UserID = 1, @FunctionName = ''USER_EDIT''';
PRINT '  - EXEC sp_CleanupExpiredOTP';
PRINT '  - EXEC sp_CheckOTPResendCooldown @Email = ''user@example.com''';
PRINT '';
PRINT '========================================';
GO
