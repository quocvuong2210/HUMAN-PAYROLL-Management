USE [HUMAN_2025];
GO

-- 1. Mở khóa IDENTITY_INSERT để có thể tự nhập EmployeeID từ 11 đến 40
SET IDENTITY_INSERT [dbo].[Employees] ON;
GO

-- 2. Chèn dữ liệu đầy đủ 30 nhân viên (11-40)
INSERT INTO [dbo].[Employees] 
(EmployeeID, FullName, DateOfBirth, Gender, PhoneNumber, Email, HireDate, DepartmentID, PositionID, Status)
VALUES 
(11, N'Trần Văn A', '1998-01-01', N'Nam', '0901000011', 'tran.vana.11@hr.com', '2025-05-01', 1, 1, N'Đang làm việc'),
(12, N'Lê Thị B', '1997-02-02', N'Nữ', '0901000012', 'le.thib.12@hr.com', '2025-05-01', 2, 2, N'Đang làm việc'),
(13, N'Phạm Văn C', '1996-03-03', N'Nam', '0901000013', 'pham.vanc.13@hr.com', '2025-05-01', 3, 3, N'Đang làm việc'),
(14, N'Hoàng Thị D', '1999-04-04', N'Nữ', '0901000014', 'hoang.thid.14@hr.com', '2025-05-01', 4, 1, N'Đang làm việc'),
(15, N'Nguyễn Văn E', '1995-05-05', N'Nam', '0901000015', 'nguyen.vane.15@hr.com', '2025-05-01', 5, 4, N'Đang làm việc'),
(16, N'Vũ Thị F', '1994-06-06', N'Nữ', '0901000016', 'vu.thif.16@hr.com', '2025-05-01', 6, 1, N'Đang làm việc'),
(17, N'Đỗ Văn G', '1993-07-07', N'Nam', '0901000017', 'do.vang.17@hr.com', '2025-05-01', 7, 7, N'Đang làm việc'),
(18, N'Phan Thị H', '1992-08-08', N'Nữ', '0901000018', 'phan.thih.18@hr.com', '2025-05-01', 8, 8, N'Thử việc'),
(19, N'Bùi Văn I', '2000-09-09', N'Nam', '0901000019', 'bui.vani.19@hr.com', '2025-05-01', 9, 9, N'Thực tập'),
(20, N'Lý Thị K', '1991-10-10', N'Nữ', '0901000020', 'ly.thik.20@hr.com', '2025-05-01', 10, 6, N'Đang làm việc'),
(21, N'Lê Văn Nam', '1995-01-10', N'Nam', '0901000021', 'le.vannam.21@hr.com', '2026-01-05', 1, 1, N'Đang làm việc'),
(22, N'Nguyễn Thị Hoa', '1996-02-15', N'Nữ', '0901000022', 'nguyen.thihoa.22@hr.com', '2026-01-05', 2, 3, N'Đang làm việc'),
(23, N'Trần Minh Tuấn', '1994-03-20', N'Nam', '0901000023', 'tran.minhtuan.23@hr.com', '2026-01-05', 3, 7, N'Đang làm việc'),
(24, N'Phạm Anh Thư', '1997-04-25', N'Nữ', '0901000024', 'pham.anhthu.24@hr.com', '2026-01-05', 4, 2, N'Đang làm việc'),
(25, N'Võ Hoàng Yên', '1993-05-30', N'Nam', '0901000025', 'vo.hoangyen.25@hr.com', '2026-01-05', 5, 4, N'Đang làm việc'),
(26, N'Đặng Thu Thảo', '1998-06-05', N'Nữ', '0901000026', 'dang.thuthao.26@hr.com', '2026-01-05', 6, 1, N'Đang làm việc'),
(27, N'Lưu Văn Tài', '1992-07-10', N'Nam', '0901000027', 'luu.vantai.27@hr.com', '2026-01-05', 7, 5, N'Đang làm việc'),
(28, N'Ngô Thị Bích', '1999-08-15', N'Nữ', '0901000028', 'ngo.thibich.28@hr.com', '2026-01-05', 8, 8, N'Thử việc'),
(29, N'Bùi Tiến Dũng', '2000-09-20', N'Nam', '0901000029', 'bui.tiendung.29@hr.com', '2026-01-05', 9, 9, N'Thực tập'),
(30, N'Hoàng Văn Mạnh', '1991-10-25', N'Nam', '0901000030', 'hoang.vanmanh.30@hr.com', '2026-01-05', 10, 6, N'Đang làm việc'),
(31, N'Nguyễn Thị Mai', '1996-11-01', N'Nữ', '0901000031', 'nguyen.thimai.31@hr.com', '2026-01-05', 1, 1, N'Đang làm việc'),
(32, N'Lê Văn Phúc', '1995-12-05', N'Nam', '0901000032', 'le.vanphuc.32@hr.com', '2026-01-05', 2, 3, N'Đang làm việc'),
(33, N'Trần Thu Hà', '1994-01-10', N'Nữ', '0901000033', 'tran.thuha.33@hr.com', '2026-01-05', 3, 7, N'Đang làm việc'),
(34, N'Phạm Văn Hùng', '1997-02-15', N'Nam', '0901000034', 'pham.vanhung.34@hr.com', '2026-01-05', 4, 2, N'Đang làm việc'),
(35, N'Võ Thị Lệ', '1993-03-20', N'Nữ', '0901000035', 'vo.thile.35@hr.com', '2026-01-05', 5, 4, N'Đang làm việc'),
(36, N'Đặng Văn Khoa', '1998-04-25', N'Nam', '0901000036', 'dang.vankhoa.36@hr.com', '2026-01-05', 6, 1, N'Đang làm việc'),
(37, N'Lưu Thị Lan', '1992-05-30', N'Nữ', '0901000037', 'luu.thilan.37@hr.com', '2026-01-05', 7, 5, N'Đang làm việc'),
(38, N'Ngô Văn Tùng', '1999-06-05', N'Nam', '0901000038', 'ngo.vantung.38@hr.com', '2026-01-05', 8, 8, N'Thử việc'),
(39, N'Bùi Thị Nga', '2000-07-10', N'Nữ', '0901000039', 'bui.thinga.39@hr.com', '2026-01-05', 9, 9, N'Thực tập'),
(40, N'Hoàng Thị Xuân', '1991-08-15', N'Nữ', '0901000040', 'hoang.thixuan.40@hr.com', '2026-01-05', 10, 6, N'Đang làm việc');
GO

-- 3. Tắt IDENTITY_INSERT sau khi chèn xong
SET IDENTITY_INSERT [dbo].[Employees] OFF;
GO