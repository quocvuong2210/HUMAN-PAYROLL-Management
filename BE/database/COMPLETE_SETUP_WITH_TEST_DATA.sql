/*
Navicat Premium Data Transfer
Complete Setup: Database + Tables + Test Data
Source: MySQL 8.0.41
Date: 07/05/2026
*/

DROP DATABASE IF EXISTS payroll_2026;
CREATE DATABASE payroll_2026;
USE payroll_2026;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- CREATE TABLES
-- ============================================

DROP TABLE IF EXISTS `attendance`;
CREATE TABLE `attendance` (
  `AttendanceID` int NOT NULL AUTO_INCREMENT,
  `EmployeeID` int NULL DEFAULT NULL,
  `WorkDays` int NOT NULL,
  `AbsentDays` int NULL DEFAULT 0,
  `LeaveDays` int NULL DEFAULT 0,
  `AttendanceMonth` date NOT NULL,
  `CreatedAt` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`AttendanceID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

DROP TABLE IF EXISTS `departments_payroll`;
CREATE TABLE `departments_payroll` (
  `DepartmentID` int NOT NULL,
  `DepartmentName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SyncedAt` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`DepartmentID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

DROP TABLE IF EXISTS `employees_payroll`;
CREATE TABLE `employees_payroll` (
  `EmployeeID` int NOT NULL,
  `FullName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DepartmentID` int NULL DEFAULT NULL,
  `PositionID` int NULL DEFAULT NULL,
  `Status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `SyncedAt` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`EmployeeID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

DROP TABLE IF EXISTS `positions_payroll`;
CREATE TABLE `positions_payroll` (
  `PositionID` int NOT NULL,
  `PositionName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SyncedAt` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`PositionID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

DROP TABLE IF EXISTS `salaries`;
CREATE TABLE `salaries` (
  `SalaryID` int NOT NULL AUTO_INCREMENT,
  `EmployeeID` int NULL DEFAULT NULL,
  `SalaryMonth` date NOT NULL,
  `BaseSalary` decimal(12, 2) NOT NULL,
  `Bonus` decimal(12, 2) NULL DEFAULT 0.00,
  `Deductions` decimal(12, 2) NULL DEFAULT 0.00,
  `NetSalary` decimal(12, 2) NOT NULL,
  `CreatedAt` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`SalaryID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ============================================
-- INSERT MASTER DATA
-- ============================================

INSERT INTO `departments_payroll` VALUES 
(1, 'Phòng Nhân sự', NOW()),
(2, 'Phòng Kế toán', NOW()),
(3, 'Phòng Kỹ thuật', NOW()),
(4, 'Phòng Kinh doanh', NOW()),
(5, 'Phòng Hành chính', NOW()),
(6, 'Phòng Marketing', NOW()),
(7, 'Phòng Sản xuất', NOW()),
(8, 'Phòng Bảo trì', NOW()),
(9, 'Phòng Nghiên cứu & Phát triển', NOW()),
(10, 'Phòng Dịch vụ khách hàng', NOW());

INSERT INTO `positions_payroll` VALUES 
(1, 'Nhân viên', NOW()),
(2, 'Trưởng nhóm', NOW()),
(3, 'Phó phòng', NOW()),
(4, 'Trưởng phòng', NOW()),
(5, 'Giám đốc', NOW()),
(6, 'Thư ký', NOW()),
(7, 'Kỹ sư', NOW()),
(8, 'Nhân viên thử việc', NOW()),
(9, 'Thực tập sinh', NOW()),
(10, 'Cố vấn kỹ thuật', NOW());

INSERT INTO `employees_payroll` VALUES 
(1, 'Nguyễn Văn An', 1, 1, 'Đang làm việc', NOW()),
(2, 'Lê Thị Bình', 2, 3, 'Đang làm việc', NOW()),
(3, 'Trần Quốc Cường', 3, 7, 'Đang làm việc', NOW()),
(4, 'Phạm Hồng Dung', 4, 2, 'Đang làm việc', NOW()),
(5, 'Võ Thành Đạt', 5, 4, 'Nghỉ phép', NOW()),
(6, 'Đặng Minh Hạnh', 6, 1, 'Đang làm việc', NOW()),
(7, 'Lưu Trung Hiếu', 7, 5, 'Đang làm việc', NOW()),
(8, 'Ngô Thu Lan', 8, 8, 'Thử việc', NOW()),
(9, 'Bùi Văn Minh', 9, 9, 'Thực tập', NOW()),
(10, 'Hoàng Thị Oanh', 10, 6, 'Đang làm việc', NOW()),
(11, 'Trần Văn A', 1, 1, 'Đang làm việc', NOW()),
(12, 'Lê Thị B', 2, 2, 'Đang làm việc', NOW()),
(13, 'Phạm Văn C', 3, 3, 'Đang làm việc', NOW()),
(14, 'Hoàng Thị D', 4, 1, 'Đang làm việc', NOW()),
(15, 'Nguyễn Văn E', 5, 4, 'Đang làm việc', NOW()),
(16, 'Vũ Thị F', 6, 1, 'Đang làm việc', NOW()),
(17, 'Đỗ Văn G', 7, 7, 'Đang làm việc', NOW()),
(18, 'Phan Thị H', 8, 8, 'Thử việc', NOW()),
(19, 'Bùi Văn I', 9, 9, 'Thực tập', NOW()),
(20, 'Lý Thị K', 10, 6, 'Đang làm việc', NOW()),
(21, 'Lê Văn Nam', 1, 1, 'Đang làm việc', NOW()),
(22, 'Nguyễn Thị Hoa', 2, 3, 'Đang làm việc', NOW()),
(23, 'Trần Minh Tuấn', 3, 7, 'Đang làm việc', NOW()),
(24, 'Phạm Anh Thư', 4, 2, 'Đang làm việc', NOW()),
(25, 'Võ Hoàng Yên', 5, 4, 'Đang làm việc', NOW()),
(26, 'Đặng Thu Thảo', 6, 1, 'Đang làm việc', NOW()),
(27, 'Lưu Văn Tài', 7, 5, 'Đang làm việc', NOW()),
(28, 'Ngô Thị Bích', 8, 8, 'Thử việc', NOW()),
(29, 'Bùi Tiến Dũng', 9, 9, 'Thực tập', NOW()),
(30, 'Hoàng Văn Mạnh', 10, 6, 'Đang làm việc', NOW()),
(31, 'Nguyễn Thị Mai', 1, 1, 'Đang làm việc', NOW()),
(32, 'Lê Văn Phúc', 2, 3, 'Đang làm việc', NOW()),
(33, 'Trần Thu Hà', 3, 7, 'Đang làm việc', NOW()),
(34, 'Phạm Văn Hùng', 4, 2, 'Đang làm việc', NOW()),
(35, 'Võ Thị Lệ', 5, 4, 'Đang làm việc', NOW()),
(36, 'Đặng Văn Khoa', 6, 1, 'Đang làm việc', NOW()),
(37, 'Lưu Thị Lan', 7, 5, 'Đang làm việc', NOW()),
(38, 'Ngô Văn Tùng', 8, 8, 'Thử việc', NOW()),
(39, 'Bùi Thị Nga', 9, 9, 'Thực tập', NOW()),
(40, 'Hoàng Thị Xuân', 10, 6, 'Đang làm việc', NOW());

-- ============================================
-- INSERT TEST DATA: ATTENDANCE (01/2025 - 05/2026)
-- WorkDays random từ 20-24
-- ============================================

-- Nhóm 1: Nhân viên bình thường (ID 1-20)
INSERT INTO `attendance` (`EmployeeID`, `WorkDays`, `AbsentDays`, `LeaveDays`, `AttendanceMonth`, `CreatedAt`)
SELECT sub.EmployeeID, 
       sub.work_val AS WorkDays,
       sub.ad_val AS AbsentDays, 
       sub.ld_val AS LeaveDays, 
       sub.m_date, 
       NOW()
FROM (
    SELECT emp.EmployeeID,
           months.m_date,
           FLOOR(20 + RAND() * 4) AS work_val,
           FLOOR(RAND() * 3) AS ad_val,
           FLOOR(RAND() * 2) AS ld_val
    FROM (SELECT 1 AS EmployeeID UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 
          UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
          UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15
          UNION SELECT 16 UNION SELECT 17 UNION SELECT 18 UNION SELECT 19 UNION SELECT 20) AS emp
    CROSS JOIN (
        SELECT DATE_FORMAT(ADDDATE('2025-01-01', INTERVAL t.i MONTH), '%Y-%m-01') AS m_date
        FROM (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
              UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 
              UNION SELECT 10 UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 
              UNION SELECT 15 UNION SELECT 16) AS t
    ) AS months
) AS sub
WHERE sub.m_date <= '2026-05-01';

-- Nhóm 2: Nhân viên nghỉ nhiều (ID 21-25) ⚠️
INSERT INTO `attendance` (`EmployeeID`, `WorkDays`, `AbsentDays`, `LeaveDays`, `AttendanceMonth`, `CreatedAt`)
SELECT sub.EmployeeID, 
       sub.work_val AS WorkDays,
       sub.ad_val AS AbsentDays, 
       sub.ld_val AS LeaveDays, 
       sub.m_date, 
       NOW()
FROM (
    SELECT emp.EmployeeID,
           months.m_date,
           FLOOR(15 + RAND() * 4) AS work_val,
           FLOOR(5 + RAND() * 4) AS ad_val,
           FLOOR(RAND() * 3) AS ld_val
    FROM (SELECT 21 AS EmployeeID UNION SELECT 22 UNION SELECT 23 UNION SELECT 24 UNION SELECT 25) AS emp
    CROSS JOIN (
        SELECT DATE_FORMAT(ADDDATE('2025-01-01', INTERVAL t.i MONTH), '%Y-%m-01') AS m_date
        FROM (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
              UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 
              UNION SELECT 10 UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 
              UNION SELECT 15 UNION SELECT 16) AS t
    ) AS months
) AS sub
WHERE sub.m_date <= '2026-05-01';

-- Nhóm 3: Nhân viên chăm chỉ (ID 26-30) ✅
INSERT INTO `attendance` (`EmployeeID`, `WorkDays`, `AbsentDays`, `LeaveDays`, `AttendanceMonth`, `CreatedAt`)
SELECT sub.EmployeeID, 
       sub.work_val AS WorkDays,
       sub.ad_val AS AbsentDays, 
       sub.ld_val AS LeaveDays, 
       sub.m_date, 
       NOW()
FROM (
    SELECT emp.EmployeeID,
           months.m_date,
           FLOOR(23 + RAND() * 2) AS work_val,
           0 AS ad_val,
           FLOOR(RAND() * 2) AS ld_val
    FROM (SELECT 26 AS EmployeeID UNION SELECT 27 UNION SELECT 28 UNION SELECT 29 UNION SELECT 30) AS emp
    CROSS JOIN (
        SELECT DATE_FORMAT(ADDDATE('2025-01-01', INTERVAL t.i MONTH), '%Y-%m-01') AS m_date
        FROM (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
              UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 
              UNION SELECT 10 UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 
              UNION SELECT 15 UNION SELECT 16) AS t
    ) AS months
) AS sub
WHERE sub.m_date <= '2026-05-01';

-- Nhóm 4: Thử việc/Thực tập (ID 31-40)
INSERT INTO `attendance` (`EmployeeID`, `WorkDays`, `AbsentDays`, `LeaveDays`, `AttendanceMonth`, `CreatedAt`)
SELECT sub.EmployeeID, 
       sub.work_val AS WorkDays,
       sub.ad_val AS AbsentDays, 
       sub.ld_val AS LeaveDays, 
       sub.m_date, 
       NOW()
FROM (
    SELECT emp.EmployeeID,
           months.m_date,
           FLOOR(18 + RAND() * 5) AS work_val,
           FLOOR(RAND() * 4) AS ad_val,
           FLOOR(RAND() * 2) AS ld_val
    FROM (SELECT 31 AS EmployeeID UNION SELECT 32 UNION SELECT 33 UNION SELECT 34 UNION SELECT 35
          UNION SELECT 36 UNION SELECT 37 UNION SELECT 38 UNION SELECT 39 UNION SELECT 40) AS emp
    CROSS JOIN (
        SELECT DATE_FORMAT(ADDDATE('2025-01-01', INTERVAL t.i MONTH), '%Y-%m-01') AS m_date
        FROM (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
              UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 
              UNION SELECT 10 UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 
              UNION SELECT 15 UNION SELECT 16) AS t
    ) AS months
) AS sub
WHERE sub.m_date <= '2026-05-01';

-- ============================================
-- INSERT TEST DATA: SALARIES (01/2025 - 05/2026)
-- ============================================

-- Nhóm 1: Lương bình thường (ID 1-15)
INSERT INTO `salaries` (`EmployeeID`, `SalaryMonth`, `BaseSalary`, `Bonus`, `Deductions`, `NetSalary`, `CreatedAt`)
SELECT sub.EmployeeID, 
       sub.m_date,
       sub.base_val,
       sub.bonus_val,
       sub.deduct_val,
       (sub.base_val + sub.bonus_val - sub.deduct_val) AS NetSalary,
       NOW()
FROM (
    SELECT emp.EmployeeID,
           months.m_date,
           FLOOR(8000000 + RAND() * 7000000) AS base_val,
           FLOOR(300000 + RAND() * 700000) AS bonus_val,
           FLOOR(100000 + RAND() * 200000) AS deduct_val
    FROM (SELECT 1 AS EmployeeID UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 
          UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
          UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15) AS emp
    CROSS JOIN (
        SELECT DATE_FORMAT(ADDDATE('2025-01-01', INTERVAL t.i MONTH), '%Y-%m-01') AS m_date
        FROM (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
              UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 
              UNION SELECT 10 UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 
              UNION SELECT 15 UNION SELECT 16) AS t
    ) AS months
) AS sub
WHERE sub.m_date <= '2026-05-01';

-- Nhóm 2: Lương cao (ID 16-20)
INSERT INTO `salaries` (`EmployeeID`, `SalaryMonth`, `BaseSalary`, `Bonus`, `Deductions`, `NetSalary`, `CreatedAt`)
SELECT sub.EmployeeID, 
       sub.m_date,
       sub.base_val,
       sub.bonus_val,
       sub.deduct_val,
       (sub.base_val + sub.bonus_val - sub.deduct_val) AS NetSalary,
       NOW()
FROM (
    SELECT emp.EmployeeID,
           months.m_date,
           FLOOR(15000000 + RAND() * 10000000) AS base_val,
           FLOOR(500000 + RAND() * 1500000) AS bonus_val,
           FLOOR(200000 + RAND() * 300000) AS deduct_val
    FROM (SELECT 16 AS EmployeeID UNION SELECT 17 UNION SELECT 18 UNION SELECT 19 UNION SELECT 20) AS emp
    CROSS JOIN (
        SELECT DATE_FORMAT(ADDDATE('2025-01-01', INTERVAL t.i MONTH), '%Y-%m-01') AS m_date
        FROM (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
              UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 
              UNION SELECT 10 UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 
              UNION SELECT 15 UNION SELECT 16) AS t
    ) AS months
) AS sub
WHERE sub.m_date <= '2026-05-01';

-- Nhóm 3: Lương thấp (ID 21-25) ⚠️
INSERT INTO `salaries` (`EmployeeID`, `SalaryMonth`, `BaseSalary`, `Bonus`, `Deductions`, `NetSalary`, `CreatedAt`)
SELECT sub.EmployeeID, 
       sub.m_date,
       sub.base_val,
       sub.bonus_val,
       sub.deduct_val,
       (sub.base_val + sub.bonus_val - sub.deduct_val) AS NetSalary,
       NOW()
FROM (
    SELECT emp.EmployeeID,
           months.m_date,
           FLOOR(5000000 + RAND() * 2000000) AS base_val,
           FLOOR(100000 + RAND() * 200000) AS bonus_val,
           FLOOR(50000 + RAND() * 100000) AS deduct_val
    FROM (SELECT 21 AS EmployeeID UNION SELECT 22 UNION SELECT 23 UNION SELECT 24 UNION SELECT 25) AS emp
    CROSS JOIN (
        SELECT DATE_FORMAT(ADDDATE('2025-01-01', INTERVAL t.i MONTH), '%Y-%m-01') AS m_date
        FROM (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
              UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 
              UNION SELECT 10 UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 
              UNION SELECT 15 UNION SELECT 16) AS t
    ) AS months
) AS sub
WHERE sub.m_date <= '2026-05-01';

-- Nhóm 4: Bonus đột biến (ID 26-30) ⚠️
INSERT INTO `salaries` (`EmployeeID`, `SalaryMonth`, `BaseSalary`, `Bonus`, `Deductions`, `NetSalary`, `CreatedAt`)
SELECT sub.EmployeeID, 
       sub.m_date,
       sub.base_val,
       sub.bonus_val,
       sub.deduct_val,
       (sub.base_val + sub.bonus_val - sub.deduct_val) AS NetSalary,
       NOW()
FROM (
    SELECT emp.EmployeeID,
           months.m_date,
           FLOOR(10000000 + RAND() * 5000000) AS base_val,
           CASE 
               WHEN months.m_date = '2026-05-01' THEN 50000000.00
               ELSE FLOOR(300000 + RAND() * 700000)
           END AS bonus_val,
           FLOOR(100000 + RAND() * 200000) AS deduct_val
    FROM (SELECT 26 AS EmployeeID UNION SELECT 27 UNION SELECT 28 UNION SELECT 29 UNION SELECT 30) AS emp
    CROSS JOIN (
        SELECT DATE_FORMAT(ADDDATE('2025-01-01', INTERVAL t.i MONTH), '%Y-%m-01') AS m_date
        FROM (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
              UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 
              UNION SELECT 10 UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 
              UNION SELECT 15 UNION SELECT 16) AS t
    ) AS months
) AS sub
WHERE sub.m_date <= '2026-05-01';

-- Nhóm 5: Thử việc/Thực tập (ID 31-40)
INSERT INTO `salaries` (`EmployeeID`, `SalaryMonth`, `BaseSalary`, `Bonus`, `Deductions`, `NetSalary`, `CreatedAt`)
SELECT sub.EmployeeID, 
       sub.m_date,
       sub.base_val,
       sub.bonus_val,
       sub.deduct_val,
       (sub.base_val + sub.bonus_val - sub.deduct_val) AS NetSalary,
       NOW()
FROM (
    SELECT emp.EmployeeID,
           months.m_date,
           FLOOR(4000000 + RAND() * 2000000) AS base_val,
           FLOOR(100000 + RAND() * 300000) AS bonus_val,
           FLOOR(50000 + RAND() * 100000) AS deduct_val
    FROM (SELECT 31 AS EmployeeID UNION SELECT 32 UNION SELECT 33 UNION SELECT 34 UNION SELECT 35
          UNION SELECT 36 UNION SELECT 37 UNION SELECT 38 UNION SELECT 39 UNION SELECT 40) AS emp
    CROSS JOIN (
        SELECT DATE_FORMAT(ADDDATE('2025-01-01', INTERVAL t.i MONTH), '%Y-%m-01') AS m_date
        FROM (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
              UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 
              UNION SELECT 10 UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 
              UNION SELECT 15 UNION SELECT 16) AS t
    ) AS months
) AS sub
WHERE sub.m_date <= '2026-05-01';

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- VERIFICATION
-- ============================================
SELECT '✅ SETUP HOÀN TẤT!' AS Status;
SELECT '📊 40 nhân viên x 17 tháng (01/2025 - 05/2026)' AS Info;
SELECT COUNT(*) AS TotalAttendance FROM attendance;
SELECT COUNT(*) AS TotalSalaries FROM salaries;
SELECT '⚠️ CẢNH BÁO:' AS Alerts;
SELECT '   - ID 21-25: Nghỉ nhiều + Lương thấp' AS Alert1;
SELECT '   - ID 26-30: Bonus đột biến tháng 05/2026 (50 triệu)' AS Alert2;
