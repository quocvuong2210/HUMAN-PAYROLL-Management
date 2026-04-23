from flask import Flask, jsonify, request
from src.routes.dashboardRoute import dashboard_bp
from src.routes.alertRoute import alert_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Đăng ký blueprint
app.register_blueprint(dashboard_bp, url_prefix="/api/v1/dashboard")
app.register_blueprint(alert_bp, url_prefix="/api/v1/alerts")

# Hiển thị JSON tiếng Việt đúng
app.json.ensure_ascii = False

@app.route("/")
def home():
    return "Hello world"

@app.route("/ip", methods=["GET"])
def get_ip():
    """
    Trả về:
    - IP LAN của client (theo Flask thấy)
    - Nếu có X-Forwarded-For (proxy), lấy IP gốc đầu tiên
    """
    # Lấy IP client nội bộ
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    client_ip_local = x_forwarded_for.split(",")[0].strip() if x_forwarded_for else request.remote_addr

    return jsonify({
        "client_ip_local": client_ip_local
    })

if __name__ == "__main__":
    # host=0.0.0.0 để truy cập từ mạng khác
    app.run(debug=True, host="0.0.0.0", port=8000)