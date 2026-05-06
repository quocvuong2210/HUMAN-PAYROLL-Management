"""
Dividend Controller - API endpoints cho quản lý thưởng
"""
from flask import jsonify, request
from src.services.dividendService import DividendService

class DividendController:
    def __init__(self):
        self.service = DividendService()
    
    def get_all_dividends(self):
        """
        GET /api/v1/dividends
        Lấy tất cả thưởng (Admin/HR)
        """
        try:
            result = self.service.get_all_dividends()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    def get_employee_dividends(self, employee_id):
        """
        GET /api/v1/dividends/employee/<employee_id>
        Lấy thưởng của nhân viên
        """
        try:
            result = self.service.get_employee_dividends(employee_id)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    def get_dividend_by_id(self, dividend_id):
        """
        GET /api/v1/dividends/<dividend_id>
        Lấy chi tiết 1 thưởng
        """
        try:
            result = self.service.get_dividend_by_id(dividend_id)
            status_code = 200 if result["status"] == "success" else 404
            return jsonify(result), status_code
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    def create_dividend(self):
        """
        POST /api/v1/dividends
        Tạo thưởng mới
        
        Body:
        {
            "employee_id": 1,
            "amount": 5000000,
            "date": "2026-01-15",
            "type": "YEAR_END",
            "description": "Thưởng cuối năm 2025",
            "status": "PENDING"
        }
        """
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    "status": "error",
                    "message": "Thiếu dữ liệu"
                }), 400
            
            result = self.service.create_dividend(data)
            status_code = 201 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    def update_dividend(self, dividend_id):
        """
        PUT /api/v1/dividends/<dividend_id>
        Cập nhật thưởng
        
        Body:
        {
            "amount": 6000000,
            "status": "APPROVED"
        }
        """
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    "status": "error",
                    "message": "Thiếu dữ liệu"
                }), 400
            
            result = self.service.update_dividend(dividend_id, data)
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    def delete_dividend(self, dividend_id):
        """
        DELETE /api/v1/dividends/<dividend_id>
        Xóa thưởng
        """
        try:
            result = self.service.delete_dividend(dividend_id)
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    def get_statistics(self):
        """
        GET /api/v1/dividends/statistics
        Thống kê thưởng
        
        Query params:
        - employee_id (optional): ID nhân viên
        """
        try:
            employee_id = request.args.get('employee_id', type=int)
            result = self.service.get_statistics(employee_id)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    def get_dividends_by_year(self, year):
        """
        GET /api/v1/dividends/year/<year>
        Lấy thưởng theo năm
        """
        try:
            result = self.service.get_dividends_by_year(year)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
