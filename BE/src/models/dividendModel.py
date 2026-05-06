"""
Dividend Model - Quản lý cổ tức/thưởng cho nhân viên
Phiên bản đơn giản - chỉ 5 cột
"""
from sqlalchemy import create_engine, text
from config import SQL_SERVER_CONN
from datetime import datetime

class DividendModel:
    def __init__(self):
        self.engine = create_engine(SQL_SERVER_CONN)
    
    def _execute(self, sql, params=None, fetch=False):
        """Hàm thực thi truy vấn nội bộ"""
        with self.engine.connect() as conn:
            with conn.begin():
                query = text(sql)
                result = conn.execute(query, params or {})
                if fetch:
                    return [dict(row._mapping) for row in result.fetchall()]
                return result
    
    # ==================== GET DIVIDENDS ====================
    
    def get_all_dividends(self):
        """Lấy tất cả thưởng"""
        sql = """
            SELECT 
                D.DividendID,
                D.EmployeeID,
                E.FullName as EmployeeName,
                D.DividendAmount,
                CONVERT(VARCHAR, D.DividendDate, 23) as DividendDate,
                CONVERT(VARCHAR, D.CreatedAt, 120) as CreatedAt
            FROM [Dividends] D
            INNER JOIN [Employees] E ON D.EmployeeID = E.EmployeeID
            ORDER BY D.CreatedAt DESC
        """
        try:
            return self._execute(sql, fetch=True)
        except Exception as e:
            print(f"Error getting all dividends: {e}")
            return []
    
    def get_employee_dividends(self, employee_id):
        """Lấy danh sách thưởng của 1 nhân viên"""
        sql = """
            SELECT 
                D.DividendID,
                D.EmployeeID,
                E.FullName as EmployeeName,
                D.DividendAmount,
                CONVERT(VARCHAR, D.DividendDate, 23) as DividendDate,
                CONVERT(VARCHAR, D.CreatedAt, 120) as CreatedAt
            FROM [Dividends] D
            INNER JOIN [Employees] E ON D.EmployeeID = E.EmployeeID
            WHERE D.EmployeeID = :employee_id
            ORDER BY D.CreatedAt DESC
        """
        try:
            return self._execute(sql, {"employee_id": employee_id}, fetch=True)
        except Exception as e:
            print(f"Error getting employee dividends: {e}")
            return []
    
    def get_dividend_by_id(self, dividend_id):
        """Lấy thông tin chi tiết 1 thưởng"""
        sql = """
            SELECT 
                D.*,
                E.FullName as EmployeeName
            FROM [Dividends] D
            INNER JOIN [Employees] E ON D.EmployeeID = E.EmployeeID
            WHERE D.DividendID = :dividend_id
        """
        try:
            result = self._execute(sql, {"dividend_id": dividend_id}, fetch=True)
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting dividend by id: {e}")
            return None
    
    # ==================== CREATE DIVIDEND ====================
    
    def create_dividend(self, employee_id, amount, date):
        """Tạo thưởng mới"""
        # Kiểm tra nhân viên tồn tại
        check_sql = "SELECT COUNT(*) as Count FROM [Employees] WHERE EmployeeID = :emp_id"
        check_result = self._execute(check_sql, {"emp_id": employee_id}, fetch=True)
        
        if check_result[0]['Count'] == 0:
            return False, "Nhân viên không tồn tại", None
        
        # Tạo thưởng
        sql = """
            INSERT INTO [Dividends] 
                ([EmployeeID], [DividendAmount], [DividendDate])
            OUTPUT INSERTED.DividendID
            VALUES (:emp_id, :amount, :date)
        """
        try:
            result = self._execute(sql, {
                "emp_id": employee_id,
                "amount": amount,
                "date": date
            }, fetch=True)
            
            dividend_id = result[0]['DividendID']
            return True, "Tạo thưởng thành công", dividend_id
            
        except Exception as e:
            return False, f"Lỗi tạo thưởng: {str(e)}", None
    
    # ==================== UPDATE DIVIDEND ====================
    
    def update_dividend(self, dividend_id, amount=None, date=None):
        """Cập nhật thông tin thưởng"""
        updates = []
        params = {"dividend_id": dividend_id}
        
        if amount is not None:
            updates.append("[DividendAmount] = :amount")
            params["amount"] = amount
        
        if date is not None:
            updates.append("[DividendDate] = :date")
            params["date"] = date
        
        if not updates:
            return False, "Không có thông tin để cập nhật"
        
        sql = f"""
            UPDATE [Dividends]
            SET {', '.join(updates)}
            WHERE [DividendID] = :dividend_id
        """
        
        try:
            self._execute(sql, params)
            return True, "Cập nhật thưởng thành công"
        except Exception as e:
            return False, f"Lỗi cập nhật thưởng: {str(e)}"
    
    # ==================== DELETE DIVIDEND ====================
    
    def delete_dividend(self, dividend_id):
        """Xóa thưởng"""
        sql = "DELETE FROM [Dividends] WHERE [DividendID] = :dividend_id"
        
        try:
            self._execute(sql, {"dividend_id": dividend_id})
            return True, "Xóa thưởng thành công"
        except Exception as e:
            return False, f"Lỗi xóa thưởng: {str(e)}"
    
    # ==================== STATISTICS ====================
    
    def get_dividend_statistics(self, employee_id=None):
        """Thống kê thưởng"""
        where_clause = "WHERE D.EmployeeID = :emp_id" if employee_id else ""
        params = {"emp_id": employee_id} if employee_id else {}
        
        sql = f"""
            SELECT 
                COUNT(*) as TotalDividends,
                ISNULL(SUM(D.DividendAmount), 0) as TotalAmount,
                ISNULL(AVG(D.DividendAmount), 0) as AverageAmount
            FROM [Dividends] D
            {where_clause}
        """
        
        try:
            result = self._execute(sql, params, fetch=True)
            return result[0] if result else {}
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}
    
    def get_dividends_by_year(self, year):
        """Lấy thưởng theo năm"""
        sql = """
            SELECT 
                D.DividendID,
                D.EmployeeID,
                E.FullName as EmployeeName,
                D.DividendAmount,
                CONVERT(VARCHAR, D.DividendDate, 23) as DividendDate,
                CONVERT(VARCHAR, D.CreatedAt, 120) as CreatedAt
            FROM [Dividends] D
            INNER JOIN [Employees] E ON D.EmployeeID = E.EmployeeID
            WHERE YEAR(D.DividendDate) = :year
            ORDER BY D.CreatedAt DESC
        """
        
        try:
            return self._execute(sql, {"year": year}, fetch=True)
        except Exception as e:
            print(f"Error getting dividends by year: {e}")
            return []
