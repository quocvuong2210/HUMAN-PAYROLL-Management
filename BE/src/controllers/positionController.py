from flask import jsonify, request
from src.services.positionService import PositionService

class PositionController:
    def __init__(self):
        # Khởi tạo service điều phối cho Position
        self.service = PositionService()

    def get_all_positions(self):
        """
        Lấy danh sách chức vụ kèm số nhân viên (TotalEmployees).
        Query params: ?search=...
        """
        try:
            search_query = request.args.get('search', default=None, type=str)
            
            # Service trả về list các dict có kèm TotalEmployees
            data = self.service.list_all_positions(search_query)
            
            return jsonify({
                "status": "success",
                "message": "Lấy danh sách chức vụ thành công",
                "count": len(data),
                "data": data
            }), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    def get_position_by_id(self, pos_id):
        """Lấy chi tiết một chức vụ theo ID"""
        try:
            result = self.service.get_details(pos_id)
            
            # Kiểm tra nếu service trả về thông báo lỗi logic
            if result.get("status") == "error":
                return jsonify(result), 404
            
            return jsonify(result), 200 # result đã là dict {status: success, data: ...}
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    def create_position(self):
        """
        Thêm mới chức vụ đồng bộ 2 DB
        Payload: { "PositionName": "Tên chức vụ" }
        """
        try:
            body = request.get_json()
            if not body:
                return jsonify({"status": "error", "message": "Dữ liệu yêu cầu không hợp lệ"}), 400
                
            name = body.get('PositionName')

            if not name or not name.strip():
                return jsonify({"status": "error", "message": "Tên chức vụ là bắt buộc"}), 400

            # Gọi Service xử lý đồng bộ: MSSQL Master -> MySQL Slave
            result = self.service.create_position_sync(name)
            
            status_code = 201 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    def update_position(self, pos_id):
        """Cập nhật tên chức vụ đồng bộ cả 2 bên"""
        try:
            body = request.get_json()
            if not body:
                return jsonify({"status": "error", "message": "Dữ liệu yêu cầu không hợp lệ"}), 400
                
            new_name = body.get('PositionName')

            if not new_name or not new_name.strip():
                return jsonify({"status": "error", "message": "Tên chức vụ mới không được để trống"}), 400

            result = self.service.update_info(pos_id, new_name)
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    def delete_position(self, pos_id):
        """
        Xóa chức vụ đồng bộ.
        Service đã check ràng buộc: nếu có nhân viên sẽ không cho xóa.
        """
        try:
            result = self.service.remove_position(pos_id)
            
            # Nếu status là error (do vướng nhân viên hoặc lỗi khác) trả về 400
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    def sync_all_positions(self):
        """Ép buộc đồng bộ lại toàn bộ Positions từ MSSQL sang MySQL"""
        try:
            result = self.service.force_sync_from_master()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500