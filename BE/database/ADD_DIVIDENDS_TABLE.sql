-- ============================================
-- THÊM BẢNG DIVIDENDS (CỔ TỨC/THƯỞNG)
-- ============================================
-- Script này thêm bảng Dividends để quản lý cổ tức/thưởng cho nhân viên
-- ============================================

USE [PermissionDB];
GO

-- Kiểm tra xem bảng Employees đã tồn tại chưa
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Employees')
BEGIN
    PRINT '⚠️ Cảnh báo: Bảng Employees chưa tồn tại!';
    PRINT '   Tạo bảng Employees trước...';
    
    CREATE TABLE [Employees] (
        [EmployeeID] INT PRIMARY KEY IDENTITY(1,1),
        [FullName] NVARCHAR(100) NOT NULL,
        [DateOfBirth] DATE,
        [Gender] NVARCHAR(10),
        [PhoneNumber] NVARCHAR(15),
        [Email] NVARCHAR(100),
        [HireDate] DATE,
        [DepartmentID] INT,
        [PositionID] INT,
        [Status] NVARCHAR(50) DEFAULT 'ACTIVE',
        [CreatedAt] DATETIME DEFAULT GETDATE(),
        [UpdatedAt] DATETIME DEFAULT GETDATE()
    );
    
    PRINT '✓ Bảng Employees đã được tạo';
END
ELSE
BEGIN
    PRINT '✓ Bảng Employees đã tồn tại';
END
GO

-- Tạo bảng Dividends
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'Dividends')
BEGIN
    PRINT '⚠️ Bảng Dividends đã tồn tại, xóa và tạo lại...';
    DROP TABLE [Dividends];
END
GO

CREATE TABLE [Dividends] (
    [DividendID] INT PRIMARY KEY IDENTITY(1,1),
    [EmployeeID] INT NOT NULL,
    [DividendAmount] DECIMAL(18, 2) NOT NULL,
    [DividendDate] DATE NOT NULL,
    [DividendType] NVARCHAR(50) DEFAULT 'BONUS',  -- BONUS, DIVIDEND, YEAR_END, SPECIAL
    [Description] NVARCHAR(255),
    [Status] NVARCHAR(20) DEFAULT 'PENDING',  -- PENDING, APPROVED, PAID
    [ApprovedBy] INT NULL,
    [ApprovedAt] DATETIME NULL,
    [CreatedAt] DATETIME DEFAULT GETDATE(),
    [UpdatedAt] DATETIME DEFAULT GETDATE(),
    
    -- Foreign Key
    CONSTRAINT FK_Dividends_Employee FOREIGN KEY ([EmployeeID]) 
        REFERENCES [Employees]([EmployeeID]) ON DELETE CASCADE,
    
    -- Check constraint
    CONSTRAINT CHK_DividendAmount CHECK ([DividendAmount] >= 0)
);
GO

-- Tạo indexes
CREATE INDEX idx_dividends_employee ON [Dividends]([EmployeeID]);
CREATE INDEX idx_dividends_date ON [Dividends]([DividendDate] DESC);
CREATE INDEX idx_dividends_status ON [Dividends]([Status]);
GO

PRINT '✓ Bảng Dividends đã được tạo thành công';
GO

-- ============================================
-- THÊM DỮ LIỆU MẪU (OPTIONAL)
-- ============================================

-- Thêm một số dữ liệu mẫu nếu cần
/*
INSERT INTO [Dividends] ([EmployeeID], [DividendAmount], [DividendDate], [DividendType], [Description], [Status])
VALUES 
(1, 5000000, '2026-01-15', 'YEAR_END', 'Thưởng cuối năm 2025', 'PAID'),
(2, 3000000, '2026-01-15', 'YEAR_END', 'Thưởng cuối năm 2025', 'PAID'),
(1, 2000000, '2026-03-01', 'BONUS', 'Thưởng dự án hoàn thành', 'APPROVED');

PRINT '✓ Dữ liệu mẫu đã được thêm';
*/
GO

-- ============================================
-- THỐNG KÊ
-- ============================================

SELECT 
    'Dividends' as TableName,
    COUNT(*) as RecordCount
FROM [Dividends];
GO

PRINT '============================================';
PRINT '✅ HOÀN TẤT: Bảng Dividends đã sẵn sàng sử dụng!';
PRINT '============================================';
GO
