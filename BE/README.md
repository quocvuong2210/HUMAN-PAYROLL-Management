# Backend - HR & Payroll Dashboard System

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update with your credentials:

```bash
cp .env.example .env
```

Edit `.env` file:

```env
# Database Configuration - Connection Strings
SQL_SERVER_CONN=mssql+pyodbc://your_username:your_password@localhost\SQLEXPRESS/HUMAN_2025?driver=ODBC+Driver+17+for+SQL+Server
MYSQL_CONN=mysql+mysqlconnector://root:your_mysql_password@localhost/payroll_2026
SQL_SERVER_PERMISSION_CONN=mssql+pyodbc://your_username:your_password@localhost\SQLEXPRESS/PERMISSION?driver=ODBC+Driver+17+for+SQL+Server

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# CORS Configuration
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 3. Setup Database

Run the SQL script to create database tables:

```bash
# Execute database/MASTER_DATABASE_SETUP.sql in SQL Server Management Studio
```

### 4. Run Application

```bash
python app.py
```

The API will be available at: `http://localhost:5000`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SQL_SERVER_CONN` | SQL Server connection string | `mssql+pyodbc://sang:password@localhost\SQLEXPRESS/HUMAN_2025?driver=ODBC+Driver+17+for+SQL+Server` |
| `MYSQL_CONN` | MySQL connection string | `mysql+mysqlconnector://root:password@localhost/payroll_2026` |
| `SQL_SERVER_PERMISSION_CONN` | Permission database connection string | `mssql+pyodbc://sang:password@localhost\SQLEXPRESS/PERMISSION?driver=ODBC+Driver+17+for+SQL+Server` |
| `JWT_SECRET_KEY` | Secret key for JWT | - |
| `JWT_ACCESS_TOKEN_EXPIRES` | Access token expiration (seconds) | `3600` |
| `JWT_REFRESH_TOKEN_EXPIRES` | Refresh token expiration (seconds) | `2592000` |
| `FLASK_ENV` | Flask environment | `development` |
| `FLASK_DEBUG` | Enable debug mode | `True` |
| `FLASK_HOST` | Flask host | `0.0.0.0` |
| `FLASK_PORT` | Flask port | `5000` |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `http://localhost:5173` |

## API Documentation

See `Security-Authorization-Design-Document.docx.md` for complete API documentation.

## Project Structure

```
BE/
├── app.py                  # Main application entry point
├── config.py               # Configuration (loads from .env)
├── .env                    # Environment variables (DO NOT COMMIT)
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
├── database/               # Database scripts
│   └── MASTER_DATABASE_SETUP.sql
├── src/
│   ├── controllers/        # API controllers
│   ├── models/             # Database models
│   ├── routes/             # API routes
│   ├── services/           # Business logic
│   ├── middleware/         # Authentication & authorization
│   └── utils/              # Utility functions
└── https/                  # HTTP test files
```

## Security Notes

⚠️ **IMPORTANT:**
- Never commit `.env` file to version control
- Change `JWT_SECRET_KEY` in production
- Use strong passwords for database
- Enable HTTPS in production
- Restrict CORS origins in production

## Testing

Use HTTP files in `https/` directory with VS Code REST Client extension:

```bash
# Example: Test login
# Open https/test_login_fixed.http
# Click "Send Request"
```

## Troubleshooting

### Database Connection Error

```
Error: Unable to connect to database
```

**Solution:**
1. Check SQL Server is running
2. Verify credentials in `.env`
3. Ensure ODBC Driver 17 is installed
4. Check firewall settings

### Module Not Found Error

```
ModuleNotFoundError: No module named 'dotenv'
```

**Solution:**
```bash
pip install python-dotenv
```

### CORS Error

```
Access to fetch at 'http://localhost:5000' from origin 'http://localhost:5173' has been blocked by CORS policy
```

**Solution:**
Add your frontend URL to `CORS_ORIGINS` in `.env`:
```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

## License

Internal use only - Company X
