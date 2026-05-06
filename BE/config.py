"""
Configuration Module - Loads settings from environment variables
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==================== DATABASE CONFIGURATION ====================

# Load connection strings from environment variables
SQL_SERVER_CONN = os.getenv(
    'SQL_SERVER_CONN',
    'mssql+pyodbc://sang:Sang17102005@localhost\\SQLEXPRESS/HUMAN_2025?driver=ODBC+Driver+17+for+SQL+Server'
)

MYSQL_CONN = os.getenv(
    'MYSQL_CONN',
    'mysql+mysqlconnector://root:123456@localhost/payroll_2026'
)

SQL_SERVER_PERMISSION_CONN = os.getenv(
    'SQL_SERVER_PERMISSION_CONN',
    'mssql+pyodbc://sang:Sang17102005@localhost\\SQLEXPRESS/PERMISSION?driver=ODBC+Driver+17+for+SQL+Server'
)

# ==================== JWT CONFIGURATION ====================

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-super-secret-jwt-key-change-this-in-production')
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # seconds
JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 2592000))  # 30 days

# ==================== FLASK CONFIGURATION ====================

FLASK_ENV = os.getenv('FLASK_ENV', 'development')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))

# ==================== CORS CONFIGURATION ====================

CORS_ORIGINS_STR = os.getenv('CORS_ORIGINS', 'http://localhost:5173')
CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS_STR.split(',')]

# ==================== DEBUG OUTPUT ====================

if FLASK_DEBUG:
    print("\n" + "="*60)
    print("CONFIGURATION LOADED FROM ENVIRONMENT")
    print("="*60)
    print(f"SQL Server Connection: {SQL_SERVER_CONN}")
    print(f"MySQL Connection: {MYSQL_CONN}")
    print(f"Permission DB Connection: {SQL_SERVER_PERMISSION_CONN}")
    print(f"Flask Environment: {FLASK_ENV}")
    print(f"Flask Debug: {FLASK_DEBUG}")
    print(f"Flask Host: {FLASK_HOST}")
    print(f"Flask Port: {FLASK_PORT}")
    print(f"CORS Origins: {CORS_ORIGINS}")
    print(f"JWT Token Expires: {JWT_ACCESS_TOKEN_EXPIRES}s")
    print("="*60 + "\n")
