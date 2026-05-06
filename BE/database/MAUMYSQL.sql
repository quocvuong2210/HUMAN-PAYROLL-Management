/*
 Navicat Premium Data Transfer

 Source Server         : mySQL
 Source Server Type    : MySQL
 Source Server Version : 80041 (8.0.41)
 Source Host           : localhost:3306
 Source Schema         : payroll_2026

 Target Server Type    : MySQL
 Target Server Version : 80041 (8.0.41)
 File Encoding         : 65001

 Date: 14/01/2026 19:02:44
*/
drop database payroll_2026;
create database payroll_2026;
use payroll_2026;
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for attendance
-- ----------------------------
DROP TABLE IF EXISTS `attendance`;
CREATE TABLE `attendance`  (
  `AttendanceID` int NOT NULL AUTO_INCREMENT,
  `EmployeeID` int NULL DEFAULT NULL,
  `WorkDays` int NOT NULL,
  `AbsentDays` int NULL DEFAULT 0,
  `LeaveDays` int NULL DEFAULT 0,
  `AttendanceMonth` date NOT NULL,
  `CreatedAt` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`AttendanceID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of attendance
-- ----------------------------
-- ----------------------------
-- Table structure for departments_payroll
-- ----------------------------
DROP TABLE IF EXISTS `departments_payroll`;
CREATE TABLE `departments_payroll`  (
  `DepartmentID` int NOT NULL,
  `DepartmentName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SyncedAt` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`DepartmentID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of departments_payroll
-- ----------------------------

-- ----------------------------
-- Table structure for employees_payroll
-- ----------------------------
DROP TABLE IF EXISTS `employees_payroll`;
CREATE TABLE `employees_payroll`  (
  `EmployeeID` int NOT NULL,
  `FullName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DepartmentID` int NULL DEFAULT NULL,
  `PositionID` int NULL DEFAULT NULL,
  `Status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `SyncedAt` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`EmployeeID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of employees_payroll
-- ----------------------------


-- ----------------------------
-- Table structure for positions_payroll
-- ----------------------------
DROP TABLE IF EXISTS `positions_payroll`;
CREATE TABLE `positions_payroll`  (
  `PositionID` int NOT NULL,
  `PositionName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SyncedAt` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`PositionID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for salaries
-- ----------------------------
DROP TABLE IF EXISTS `salaries`;
CREATE TABLE `salaries`  (
  `SalaryID` int NOT NULL AUTO_INCREMENT,
  `EmployeeID` int NULL DEFAULT NULL,
  `SalaryMonth` date NOT NULL,
  `BaseSalary` decimal(12, 2) NOT NULL,
  `Bonus` decimal(12, 2) NULL DEFAULT 0.00,
  `Deductions` decimal(12, 2) NULL DEFAULT 0.00,
  `NetSalary` decimal(12, 2) NOT NULL,
  `CreatedAt` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`SalaryID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of salaries
-- ----------------------------

INSERT INTO `departments_payroll` VALUES (1, 'Phòng Nhân sự', '2025-10-20 19:13:03');
INSERT INTO `departments_payroll` VALUES (2, 'Phòng Kế toán', '2025-10-20 19:13:03');
INSERT INTO `departments_payroll` VALUES (3, 'Phòng Kỹ thuật', '2025-10-20 19:13:03');
INSERT INTO `departments_payroll` VALUES (4, 'Phòng Kinh doanh', '2025-10-20 19:13:03');
INSERT INTO `departments_payroll` VALUES (5, 'Phòng Hành chính', '2025-10-20 19:13:03');
INSERT INTO `departments_payroll` VALUES (6, 'Phòng Marketing', '2025-10-20 19:13:03');
INSERT INTO `departments_payroll` VALUES (7, 'Phòng Sản xuất', '2025-10-20 19:13:03');
INSERT INTO `departments_payroll` VALUES (8, 'Phòng Bảo trì', '2025-10-20 19:13:03');
INSERT INTO `departments_payroll` VALUES (9, 'Phòng Nghiên cứu & Phát triển', '2025-10-20 19:13:03');
INSERT INTO `departments_payroll` VALUES (10, 'Phòng Dịch vụ khách hàng', '2025-10-20 19:13:03');
INSERT INTO `positions_payroll` VALUES (1, 'Nhân viên', '2025-10-20 19:13:03');
INSERT INTO `positions_payroll` VALUES (2, 'Trưởng nhóm', '2025-10-20 19:13:03');
INSERT INTO `positions_payroll` VALUES (3, 'Phó phòng', '2025-10-20 19:13:03');
INSERT INTO `positions_payroll` VALUES (4, 'Trưởng phòng', '2025-10-20 19:13:03');
INSERT INTO `positions_payroll` VALUES (5, 'Giám đốc', '2025-10-20 19:13:03');
INSERT INTO `positions_payroll` VALUES (6, 'Thư ký', '2025-10-20 19:13:03');
INSERT INTO `positions_payroll` VALUES (7, 'Kỹ sư', '2025-10-20 19:13:03');
INSERT INTO `positions_payroll` VALUES (8, 'Nhân viên thử việc', '2025-10-20 19:13:03');
INSERT INTO `positions_payroll` VALUES (9, 'Thực tập sinh', '2025-10-20 19:13:03');
INSERT INTO `positions_payroll` VALUES (10, 'Cố vấn kỹ thuật', '2025-10-20 19:13:03');
  
  
INSERT IGNORE INTO `employees_payroll` (`EmployeeID`, `FullName`, `DepartmentID`, `PositionID`, `Status`) VALUES
(11, 'Trần Văn A', 1, 1, 'Đang làm việc'), (12, 'Lê Thị B', 2, 2, 'Đang làm việc'),
(13, 'Phạm Văn C', 3, 3, 'Đang làm việc'), (14, 'Hoàng Thị D', 4, 1, 'Đang làm việc'),
(15, 'Nguyễn Văn E', 5, 4, 'Đang làm việc'), (16, 'Vũ Thị F', 6, 1, 'Đang làm việc'),
(17, 'Đỗ Văn G', 7, 7, 'Đang làm việc'), (18, 'Phan Thị H', 8, 8, 'Thử việc'),
(19, 'Bùi Văn I', 9, 9, 'Thực tập'), (20, 'Lý Thị K', 10, 6, 'Đang làm việc'),
(21, 'Lê Văn Nam', 1, 1, 'Đang làm việc'), (22, 'Nguyễn Thị Hoa', 2, 3, 'Đang làm việc'),
(23, 'Trần Minh Tuấn', 3, 7, 'Đang làm việc'), (24, 'Phạm Anh Thư', 4, 2, 'Đang làm việc'),
(25, 'Võ Hoàng Yên', 5, 4, 'Đang làm việc'), (26, 'Đặng Thu Thảo', 6, 1, 'Đang làm việc'),
(27, 'Lưu Văn Tài', 7, 5, 'Đang làm việc'), (28, 'Ngô Thị Bích', 8, 8, 'Thử việc'),
(29, 'Bùi Tiến Dũng', 9, 9, 'Thực tập'), (30, 'Hoàng Văn Mạnh', 10, 6, 'Đang làm việc'),
(31, 'Nguyễn Thị Mai', 1, 1, 'Đang làm việc'), (32, 'Lê Văn Phúc', 2, 3, 'Đang làm việc'),
(33, 'Trần Thu Hà', 3, 7, 'Đang làm việc'), (34, 'Phạm Văn Hùng', 4, 2, 'Đang làm việc'),
(35, 'Võ Thị Lệ', 5, 4, 'Đang làm việc'), (36, 'Đặng Văn Khoa', 6, 1, 'Đang làm việc'),
(37, 'Lưu Thị Lan', 7, 5, 'Đang làm việc'), (38, 'Ngô Văn Tùng', 8, 8, 'Thử việc'),
(39, 'Bùi Thị Nga', 9, 9, 'Thực tập'), (40, 'Hoàng Thị Xuân', 10, 6, 'Đang làm việc'); 

INSERT INTO `salaries` VALUES (1, 1, '2024-09-01', 12000000.00, 500000.00, 200000.00, 12300000.00, '2025-10-20 19:13:03');
INSERT INTO `salaries` VALUES (2, 2, '2024-09-01', 10000000.00, 800000.00, 100000.00, 10700000.00, '2025-10-20 19:13:03');
INSERT INTO `salaries` VALUES (3, 3, '2024-09-01', 15000000.00, 600000.00, 0.00, 15600000.00, '2025-10-20 19:13:03');
INSERT INTO `salaries` VALUES (4, 4, '2024-09-01', 11000000.00, 400000.00, 100000.00, 11300000.00, '2025-10-20 19:13:03');
INSERT INTO `salaries` VALUES (5, 5, '2024-09-01', 9000000.00, 0.00, 300000.00, 8700000.00, '2025-10-20 19:13:03');
INSERT INTO `salaries` VALUES (6, 6, '2024-09-01', 9500000.00, 500000.00, 0.00, 10000000.00, '2025-10-20 19:13:03');
INSERT INTO `salaries` VALUES (7, 7, '2024-09-01', 18000000.00, 1000000.00, 0.00, 19000000.00, '2025-10-20 19:13:03');
INSERT INTO `salaries` VALUES (8, 8, '2024-09-01', 7000000.00, 200000.00, 0.00, 7200000.00, '2025-10-20 19:13:03');
INSERT INTO `salaries` VALUES (9, 9, '2024-09-01', 5000000.00, 0.00, 0.00, 5000000.00, '2025-10-20 19:13:03');
INSERT INTO `salaries` VALUES (10, 10, '2024-09-01', 8500000.00, 300000.00, 100000.00, 8700000.00, '2025-10-20 19:13:03');
INSERT INTO `salaries` VALUES (11, 1, '2024-09-01', 12000000.00, 500000.00, 200000.00, 12300000.00, '2025-10-20 19:15:00');
INSERT INTO `salaries` VALUES (12, 2, '2024-09-01', 10000000.00, 800000.00, 100000.00, 10700000.00, '2025-10-20 19:15:00');
INSERT INTO `salaries` VALUES (13, 3, '2024-09-01', 15000000.00, 600000.00, 0.00, 15600000.00, '2025-10-20 19:15:00');
INSERT INTO `salaries` VALUES (14, 4, '2024-09-01', 11000000.00, 400000.00, 100000.00, 11300000.00, '2025-10-20 19:15:00');
INSERT INTO `salaries` VALUES (15, 5, '2024-09-01', 9000000.00, 0.00, 300000.00, 8700000.00, '2025-10-20 19:15:00');
INSERT INTO `salaries` VALUES (16, 6, '2024-09-01', 9500000.00, 500000.00, 0.00, 10000000.00, '2025-10-20 19:15:00');
INSERT INTO `salaries` VALUES (17, 7, '2024-09-01', 18000000.00, 1000000.00, 0.00, 19000000.00, '2025-10-20 19:15:00');
INSERT INTO `salaries` VALUES (18, 8, '2024-09-01', 7000000.00, 200000.00, 0.00, 7200000.00, '2025-10-20 19:15:00');
INSERT INTO `salaries` VALUES (19, 9, '2024-09-01', 5000000.00, 0.00, 0.00, 5000000.00, '2025-10-20 19:15:00');
INSERT INTO `salaries` VALUES (20, 10, '2024-09-01', 8500000.00, 300000.00, 100000.00, 8700000.00, '2025-10-20 19:15:00');

INSERT INTO `attendance` VALUES (1, 1, 22, 1, 0, '2024-09-01', '2025-10-20 19:13:03');
INSERT INTO `attendance` VALUES (2, 2, 21, 0, 1, '2024-09-01', '2025-10-20 19:13:03');
INSERT INTO `attendance` VALUES (3, 3, 23, 0, 0, '2024-09-01', '2025-10-20 19:13:03');
INSERT INTO `attendance` VALUES (4, 4, 22, 2, 0, '2024-09-01', '2025-10-20 19:13:03');
INSERT INTO `attendance` VALUES (5, 5, 18, 3, 2, '2024-09-01', '2025-10-20 19:13:03');
INSERT INTO `attendance` VALUES (6, 6, 24, 0, 0, '2024-09-01', '2025-10-20 19:13:03');
INSERT INTO `attendance` VALUES (7, 7, 20, 1, 1, '2024-09-01', '2025-10-20 19:13:03');
INSERT INTO `attendance` VALUES (8, 8, 19, 2, 0, '2024-09-01', '2025-10-20 19:13:03');
INSERT INTO `attendance` VALUES (9, 9, 16, 0, 2, '2024-09-01', '2025-10-20 19:13:03');
INSERT INTO `attendance` VALUES (10, 10, 22, 1, 0, '2024-09-01', '2025-10-20 19:13:03');
INSERT INTO `attendance` VALUES (11, 1, 22, 1, 0, '2024-09-01', '2025-10-20 19:14:40');
INSERT INTO `attendance` VALUES (12, 2, 21, 0, 1, '2024-09-01', '2025-10-20 19:14:40');
INSERT INTO `attendance` VALUES (13, 3, 23, 0, 0, '2024-09-01', '2025-10-20 19:14:40');
INSERT INTO `attendance` VALUES (14, 4, 22, 2, 0, '2024-09-01', '2025-10-20 19:14:40');
INSERT INTO `attendance` VALUES (15, 5, 18, 3, 2, '2024-09-01', '2025-10-20 19:14:40');
INSERT INTO `attendance` VALUES (16, 6, 24, 0, 0, '2024-09-01', '2025-10-20 19:14:40');
INSERT INTO `attendance` VALUES (17, 7, 20, 1, 1, '2024-09-01', '2025-10-20 19:14:40');
INSERT INTO `attendance` VALUES (18, 8, 19, 2, 0, '2024-09-01', '2025-10-20 19:14:40');
INSERT INTO `attendance` VALUES (19, 9, 16, 0, 2, '2024-09-01', '2025-10-20 19:14:40');
INSERT INTO `attendance` VALUES (20, 10, 22, 1, 0, '2024-09-01', '2025-10-20 19:14:40');

-- ----------------------------
-- Records of positions_payroll
-- ----------------------------

-- ============================================
-- CHÈN DỮ LIỆU CHẤM CÔNG (01/2025 - 05/2026)
-- ============================================

-- Nhóm 1: Nhân viên bình thường (ID 1-20)
INSERT INTO `attendance` (`EmployeeID`, `WorkDays`, `AbsentDays`, `LeaveDays`, `AttendanceMonth`, `CreatedAt`)
SELECT sub.EmployeeID, 
       (24 - (sub.ld_val + sub.ad_val)) AS WorkDays, 
       sub.ad_val AS AbsentDays, 
       sub.ld_val AS LeaveDays, 
       sub.m_date, 
       NOW()
FROM (
    SELECT emp.EmployeeID,
           months.m_date,
           FLOOR(RAND() * 2) AS ld_val,
           FLOOR(RAND() * 3) AS ad_val
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
       (24 - (sub.ld_val + sub.ad_val)) AS WorkDays, 
       sub.ad_val AS AbsentDays, 
       sub.ld_val AS LeaveDays, 
       sub.m_date, 
       NOW()
FROM (
    SELECT emp.EmployeeID,
           months.m_date,
           FLOOR(RAND() * 3) AS ld_val,
           FLOOR(5 + RAND() * 4) AS ad_val
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
       (24 - (sub.ld_val + sub.ad_val)) AS WorkDays, 
       sub.ad_val AS AbsentDays, 
       sub.ld_val AS LeaveDays, 
       sub.m_date, 
       NOW()
FROM (
    SELECT emp.EmployeeID,
           months.m_date,
           FLOOR(RAND() * 2) AS ld_val,
           0 AS ad_val
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
       (24 - (sub.ld_val + sub.ad_val)) AS WorkDays, 
       sub.ad_val AS AbsentDays, 
       sub.ld_val AS LeaveDays, 
       sub.m_date, 
       NOW()
FROM (
    SELECT emp.EmployeeID,
           months.m_date,
           FLOOR(RAND() * 2) AS ld_val,
           FLOOR(RAND() * 4) AS ad_val
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
-- CHÈN DỮ LIỆU LƯƠNG (01/2025 - 05/2026)
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
-- THỐNG KÊ
-- ============================================
SELECT '✅ ĐÃ TẠO XONG DỮ LIỆU TEST!' AS Status;
SELECT '📊 40 nhân viên x 17 tháng (01/2025 - 05/2026)' AS Info1;
SELECT COUNT(*) AS TotalAttendance FROM attendance;
SELECT COUNT(*) AS TotalSalaries FROM salaries;
SELECT '⚠️ CẢNH BÁO ĐÃ TẠO:' AS Info2;
SELECT '   - ID 21-25: Nghỉ nhiều (5-8 ngày/tháng) + Lương thấp (5-7 triệu)' AS Alert1;
SELECT '   - ID 26-30: Bonus đột biến tháng 05/2026 (50 triệu VND)' AS Alert2;
SELECT '   - ID 26-30: Chăm chỉ (23-24 ngày làm việc)' AS Alert3;
SELECT '   - ID 31-40: Thử việc/Thực tập (4-6 triệu lương)' AS Alert4;

SET FOREIGN_KEY_CHECKS = 1;
