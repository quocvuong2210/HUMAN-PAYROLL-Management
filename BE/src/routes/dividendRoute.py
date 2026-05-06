"""
Dividend Routes - API routes cho quản lý thưởng
"""
from flask import Blueprint
from src.controllers.dividendController import DividendController

# Khởi tạo Blueprint
dividend_bp = Blueprint('dividend', __name__)

# Khởi tạo Controller
dividend_controller = DividendController()

# ==================== DIVIDEND ROUTES ====================

@dividend_bp.route('/dividends', methods=['GET'])
def get_all_dividends():
    """Lấy tất cả thưởng"""
    return dividend_controller.get_all_dividends()

@dividend_bp.route('/dividends/employee/<int:employee_id>', methods=['GET'])
def get_employee_dividends(employee_id):
    """Lấy thưởng của nhân viên"""
    return dividend_controller.get_employee_dividends(employee_id)

@dividend_bp.route('/dividends/<int:dividend_id>', methods=['GET'])
def get_dividend_by_id(dividend_id):
    """Lấy chi tiết 1 thưởng"""
    return dividend_controller.get_dividend_by_id(dividend_id)

@dividend_bp.route('/dividends', methods=['POST'])
def create_dividend():
    """Tạo thưởng mới"""
    return dividend_controller.create_dividend()

@dividend_bp.route('/dividends/<int:dividend_id>', methods=['PUT'])
def update_dividend(dividend_id):
    """Cập nhật thưởng"""
    return dividend_controller.update_dividend(dividend_id)

@dividend_bp.route('/dividends/<int:dividend_id>', methods=['DELETE'])
def delete_dividend(dividend_id):
    """Xóa thưởng"""
    return dividend_controller.delete_dividend(dividend_id)

@dividend_bp.route('/dividends/statistics', methods=['GET'])
def get_statistics():
    """Thống kê thưởng"""
    return dividend_controller.get_statistics()

@dividend_bp.route('/dividends/year/<int:year>', methods=['GET'])
def get_dividends_by_year(year):
    """Lấy thưởng theo năm"""
    return dividend_controller.get_dividends_by_year(year)
