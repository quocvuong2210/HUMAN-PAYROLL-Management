from flask import Flask, jsonify, request
from flask_cors import CORS
import config

# Import routes
from src.routes.dashboardRoute import dashboard_bp
from src.routes.alertRoute import alert_bp
# from src.routes.authRoute import auth_bp  # OLD - Commented out
from src.routes.auth_rbac_route import auth_rbac_bp  # NEW - Auth with RBAC (PRODUCTION)
from src.routes.employee_route import employee_bp
from src.routes.departmentRoute import department_bp
from src.routes.positionRoute import position_bp
from src.routes.salaryRoute import salary_bp
from src.routes.attendenceRoute import attendance_bp
from src.routes.reportRoute import report_bp
from src.routes.rbac_management_route import rbac_management_bp
from src.routes.roleRoute import role_bp
from src.routes.user_route_v2 import user_v2_bp
from src.routes.user_admin_route import user_admin_bp
from src.routes.export_route import export_bp
from src.routes.dividendRoute import dividend_bp

app = Flask(__name__)

# Load configuration from config.py (which reads from .env)
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRES

# CORS Configuration - Use origins from config
CORS(app, 
     resources={r"/api/*": {"origins": config.CORS_ORIGINS}},
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=True)

# Đăng ký blueprint
app.register_blueprint(dashboard_bp, url_prefix="/api/v1/dashboard")
app.register_blueprint(alert_bp, url_prefix="/api/v1/alerts")

# ==================== AUTH ROUTES (PRODUCTION) ====================
# app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")  # OLD - Commented out
app.register_blueprint(auth_rbac_bp)  # NEW - Auth with RBAC (url_prefix already in blueprint)

# ==================== RBAC ROUTES ====================
app.register_blueprint(role_bp, url_prefix="/api/v1/auth")  # Role Management
app.register_blueprint(user_v2_bp, url_prefix="/api/v1/auth")  # User V2 - Production RBAC
app.register_blueprint(user_admin_bp, url_prefix="/api/v1/admin")  # Admin - Users & Logs with RBAC

# ==================== ALTERNATIVE AUTH ROUTES (V2) ====================
app.register_blueprint(rbac_management_bp, url_prefix="/api/v2/rbac")  # RBAC Management

# ==================== BUSINESS ROUTES ====================
app.register_blueprint(employee_bp, url_prefix="/api/v1/employees")
app.register_blueprint(department_bp, url_prefix="/api/v1/departments")
app.register_blueprint(position_bp, url_prefix="/api/v1/positions")
app.register_blueprint(salary_bp, url_prefix="/api/v1/salary")
app.register_blueprint(attendance_bp, url_prefix="/api/v1/attendance")
app.register_blueprint(report_bp, url_prefix="/api/v1/reports")

# ==================== EXPORT ROUTES ====================
app.register_blueprint(export_bp, url_prefix="/api/v1/export")

# ==================== DIVIDEND ROUTES ====================
app.register_blueprint(dividend_bp, url_prefix="/api/v1")


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
    # Use configuration from config.py
    app.run(
        debug=config.FLASK_DEBUG,
        host=config.FLASK_HOST,
        port=config.FLASK_PORT
    )