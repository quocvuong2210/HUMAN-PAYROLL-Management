# 📊 Hướng Dẫn Bảng DIVIDENDS (Cổ Tức/Thưởng)

## 📋 Mục Đích

Bảng `Dividends` dùng để quản lý **cổ tức và tiền thưởng** phát cho nhân viên, bao gồm:
- 🎁 Thưởng cuối năm
- 💰 Cổ tức từ lợi nhuận công ty
- 🏆 Thưởng dự án/thành tích
- 🎉 Thưởng đặc biệt

---

## 🗂️ Cấu Trúc Bảng

```sql
CREATE TABLE [Dividends] (
    [DividendID] INT PRIMARY KEY IDENTITY(1,1),
    [EmployeeID] INT NOT NULL,
    [DividendAmount] DECIMAL(18, 2) NOT NULL,
    [DividendDate] DATE NOT NULL,
    [DividendType] NVARCHAR(50) DEFAULT 'BONUS',
    [Description] NVARCHAR(255),
    [Status] NVARCHAR(20) DEFAULT 'PENDING',
    [ApprovedBy] INT NULL,
    [ApprovedAt] DATETIME NULL,
    [CreatedAt] DATETIME DEFAULT GETDATE(),
    [UpdatedAt] DATETIME DEFAULT GETDATE()
);
```

### Các Cột:

| Cột | Kiểu Dữ Liệu | Mô Tả |
|-----|-------------|-------|
| `DividendID` | INT | ID duy nhất (Primary Key) |
| `EmployeeID` | INT | ID nhân viên (Foreign Key → Employees) |
| `DividendAmount` | DECIMAL(18,2) | Số tiền thưởng (VD: 5000000.00) |
| `DividendDate` | DATE | Ngày phát thưởng |
| `DividendType` | NVARCHAR(50) | Loại thưởng (BONUS, DIVIDEND, YEAR_END, SPECIAL) |
| `Description` | NVARCHAR(255) | Mô tả lý do thưởng |
| `Status` | NVARCHAR(20) | Trạng thái (PENDING, APPROVED, PAID) |
| `ApprovedBy` | INT | ID người phê duyệt (nullable) |
| `ApprovedAt` | DATETIME | Thời gian phê duyệt (nullable) |
| `CreatedAt` | DATETIME | Thời gian tạo |
| `UpdatedAt` | DATETIME | Thời gian cập nhật |

---

## 🎯 Các Loại Thưởng (DividendType)

| Giá Trị | Ý Nghĩa | Ví Dụ |
|---------|---------|-------|
| `BONUS` | Thưởng thành tích | Thưởng hoàn thành dự án |
| `DIVIDEND` | Cổ tức | Chia lợi nhuận công ty |
| `YEAR_END` | Thưởng cuối năm | Thưởng Tết |
| `SPECIAL` | Thưởng đặc biệt | Thưởng sinh nhật công ty |

---

## 📊 Trạng Thái (Status)

| Trạng Thái | Ý Nghĩa | Hành Động Tiếp Theo |
|-----------|---------|---------------------|
| `PENDING` | Chờ phê duyệt | HR Manager phê duyệt |
| `APPROVED` | Đã phê duyệt | Kế toán thanh toán |
| `PAID` | Đã thanh toán | Hoàn tất |

---

## 🚀 Cách Sử Dụng

### 1. Chạy Script Tạo Bảng

```bash
# Mở SQL Server Management Studio (SSMS)
# Mở file: BE/database/ADD_DIVIDENDS_TABLE.sql
# Chạy script (F5)
```

Hoặc dùng command line:
```bash
sqlcmd -S localhost -d PermissionDB -i BE/database/ADD_DIVIDENDS_TABLE.sql
```

### 2. Thêm Dữ Liệu Mẫu

```sql
INSERT INTO [Dividends] 
    ([EmployeeID], [DividendAmount], [DividendDate], [DividendType], [Description], [Status])
VALUES 
    (1, 5000000, '2026-01-15', 'YEAR_END', 'Thưởng cuối năm 2025', 'PAID'),
    (2, 3000000, '2026-01-15', 'YEAR_END', 'Thưởng cuối năm 2025', 'PAID'),
    (1, 2000000, '2026-03-01', 'BONUS', 'Thưởng dự án hoàn thành', 'APPROVED');
```

### 3. Truy Vấn Dữ Liệu

#### Xem tất cả thưởng của 1 nhân viên:
```sql
SELECT * FROM [Dividends]
WHERE [EmployeeID] = 1
ORDER BY [DividendDate] DESC;
```

#### Tổng thưởng theo nhân viên:
```sql
SELECT 
    E.FullName,
    COUNT(D.DividendID) as TotalDividends,
    SUM(D.DividendAmount) as TotalAmount
FROM [Employees] E
LEFT JOIN [Dividends] D ON E.EmployeeID = D.EmployeeID
GROUP BY E.FullName
ORDER BY TotalAmount DESC;
```

#### Thưởng chờ phê duyệt:
```sql
SELECT 
    E.FullName,
    D.DividendAmount,
    D.DividendDate,
    D.DividendType,
    D.Description
FROM [Dividends] D
INNER JOIN [Employees] E ON D.EmployeeID = E.EmployeeID
WHERE D.Status = 'PENDING'
ORDER BY D.DividendDate DESC;
```

---

## 🔧 Tích Hợp Vào Backend

### 1. Tạo Model (`BE/src/models/dividend_model.py`)

```python
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN

class DividendModel:
    def __init__(self):
        self.engine = create_engine(SQL_SERVER_PERMISSION_CONN)
    
    def get_employee_dividends(self, employee_id):
        """Lấy danh sách thưởng của nhân viên"""
        sql = """
            SELECT * FROM [Dividends]
            WHERE [EmployeeID] = :employee_id
            ORDER BY [DividendDate] DESC
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(sql), {"employee_id": employee_id})
            return [dict(row._mapping) for row in result.fetchall()]
    
    def create_dividend(self, employee_id, amount, date, type, description):
        """Tạo thưởng mới"""
        sql = """
            INSERT INTO [Dividends] 
                ([EmployeeID], [DividendAmount], [DividendDate], 
                 [DividendType], [Description], [Status])
            VALUES (:emp_id, :amount, :date, :type, :desc, 'PENDING')
        """
        with self.engine.connect() as conn:
            with conn.begin():
                conn.execute(text(sql), {
                    "emp_id": employee_id,
                    "amount": amount,
                    "date": date,
                    "type": type,
                    "desc": description
                })
        return True
```

### 2. Tạo Service (`BE/src/services/dividend_service.py`)

```python
from src.models.dividend_model import DividendModel

class DividendService:
    def __init__(self):
        self.model = DividendModel()
    
    def get_employee_dividends(self, employee_id):
        return self.model.get_employee_dividends(employee_id)
    
    def create_dividend(self, data):
        return self.model.create_dividend(
            employee_id=data['employee_id'],
            amount=data['amount'],
            date=data['date'],
            type=data['type'],
            description=data.get('description', '')
        )
```

### 3. Tạo Controller & Route

```python
# BE/src/controllers/dividend_controller.py
from flask import jsonify, request
from src.services.dividend_service import DividendService

class DividendController:
    def __init__(self):
        self.service = DividendService()
    
    def get_employee_dividends(self, employee_id):
        dividends = self.service.get_employee_dividends(employee_id)
        return jsonify({"status": "success", "data": dividends}), 200

# BE/src/routes/dividend_route.py
from flask import Blueprint
from src.controllers.dividend_controller import DividendController

dividend_bp = Blueprint('dividend', __name__)
controller = DividendController()

@dividend_bp.route('/employees/<int:employee_id>/dividends', methods=['GET'])
def get_dividends(employee_id):
    return controller.get_employee_dividends(employee_id)
```

---

## 📍 Vị Trí Trong Database

Bảng `Dividends` nên được đặt trong **cùng database với bảng Employees**:

```
Database: PermissionDB (hoặc HRPayrollDB)
├── USER
├── ROLE
├── PERMISSION
├── Employees          ← Bảng nhân viên
├── Departments        ← Bảng phòng ban
├── Positions          ← Bảng chức vụ
├── Salaries           ← Bảng lương
└── Dividends          ← Bảng thưởng (MỚI)
```

---

## ⚠️ Lưu Ý

1. **Foreign Key**: Bảng `Dividends` phụ thuộc vào bảng `Employees`
   - Phải tạo bảng `Employees` trước
   - Khi xóa nhân viên, các thưởng liên quan cũng bị xóa (CASCADE)

2. **Quyền Truy Cập**:
   - Nhân viên: Chỉ xem thưởng của mình
   - HR Manager: Tạo và phê duyệt thưởng
   - Kế toán: Cập nhật trạng thái thanh toán

3. **Validation**:
   - `DividendAmount` phải >= 0
   - `DividendDate` không được là tương lai (tùy chọn)
   - `Status` chỉ nhận: PENDING, APPROVED, PAID

---

## 📞 Hỗ Trợ

Nếu có vấn đề khi tạo bảng, kiểm tra:
1. ✅ Bảng `Employees` đã tồn tại chưa?
2. ✅ Database connection string đúng chưa?
3. ✅ User có quyền CREATE TABLE không?

---

**Tài liệu được tạo**: 2026-05-06  
**Phiên bản**: 1.0
