"""
Dividend Service - Business logic cho quản lý thưởng
Phiên bản đơn giản
"""
from src.models.dividendModel import DividendModel

class DividendService:
    def __init__(self):
        self.model = DividendModel()
    
    def get_all_dividends(self):
        """Lấy tất cả thưởng"""
        dividends = self.model.get_all_dividends()
        return {
            "status": "success",
            "data": dividends,
            "count": len(dividends)
        }
    
    def get_employee_dividends(self, employee_id):
        """Lấy thưởng của nhân viên"""
        dividends = self.model.get_employee_dividends(employee_id)
        stats = self.model.get_dividend_statistics(employee_id)
        
        return {
            "status": "success",
            "data": dividends,
            "statistics": stats,
            "count": len(dividends)
        }
    
    def get_dividend_by_id(self, dividend_id):
        """Lấy chi tiết 1 thưởng"""
        dividend = self.model.get_dividend_by_id(dividend_id)
        
        if not dividend:
            return {
                "status": "error",
                "message": "Không tìm thấy thưởng"
            }
        
        return {
            "status": "success",
            "data": dividend
        }
    
    def create_dividend(self, data):
        """Tạo thưởng mới"""
        # Validate
        required_fields = ['employee_id', 'amount', 'date']
        for field in required_fields:
            if field not in data:
                return {
                    "status": "error",
                    "message": f"Thiếu trường {field}"
                }
        
        # Validate amount
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return {
                    "status": "error",
                    "message": "Số tiền thưởng phải lớn hơn 0"
                }
        except ValueError:
            return {
                "status": "error",
                "message": "Số tiền thưởng không hợp lệ"
            }
        
        # Create
        success, message, dividend_id = self.model.create_dividend(
            employee_id=data['employee_id'],
            amount=amount,
            date=data['date']
        )
        
        if success:
            return {
                "status": "success",
                "message": message,
                "dividend_id": dividend_id
            }
        
        return {
            "status": "error",
            "message": message
        }
    
    def update_dividend(self, dividend_id, data):
        """Cập nhật thưởng"""
        # Validate amount if provided
        if 'amount' in data:
            try:
                amount = float(data['amount'])
                if amount <= 0:
                    return {
                        "status": "error",
                        "message": "Số tiền thưởng phải lớn hơn 0"
                    }
                data['amount'] = amount
            except ValueError:
                return {
                    "status": "error",
                    "message": "Số tiền thưởng không hợp lệ"
                }
        
        # Update
        success, message = self.model.update_dividend(
            dividend_id=dividend_id,
            amount=data.get('amount'),
            date=data.get('date')
        )
        
        if success:
            return {
                "status": "success",
                "message": message
            }
        
        return {
            "status": "error",
            "message": message
        }
    
    def delete_dividend(self, dividend_id):
        """Xóa thưởng"""
        success, message = self.model.delete_dividend(dividend_id)
        
        if success:
            return {
                "status": "success",
                "message": message
            }
        
        return {
            "status": "error",
            "message": message
        }
    
    def get_statistics(self, employee_id=None):
        """Thống kê thưởng"""
        stats = self.model.get_dividend_statistics(employee_id)
        
        return {
            "status": "success",
            "data": stats
        }
    
    def get_dividends_by_year(self, year):
        """Lấy thưởng theo năm"""
        try:
            year = int(year)
        except ValueError:
            return {
                "status": "error",
                "message": "Năm không hợp lệ"
            }
        
        dividends = self.model.get_dividends_by_year(year)
        
        return {
            "status": "success",
            "data": dividends,
            "count": len(dividends)
        }
