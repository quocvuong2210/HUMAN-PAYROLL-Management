"""
Test Login Endpoint - Standalone Flask app để test login
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN

app = Flask(__name__)
CORS(app)

@app.route('/test/login', methods=['POST'])
def test_login():
    """Test login endpoint với debug chi tiết"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    debug_info = {
        "step": "",
        "details": []
    }
    
    try:
        engine = create_engine(SQL_SERVER_PERMISSION_CONN)
        
        # Step 1: Check user exists
        debug_info["step"] = "1. Checking user exists"
        with engine.connect() as conn:
            sql = text("SELECT UserID, Username, PasswordHash, Status FROM [USER] WHERE Username = :username")
            result = conn.execute(sql, {"username": username}).fetchone()
            
            if not result:
                debug_info["details"].append(f"❌ User '{username}' not found")
                return jsonify({
                    "status": "error",
                    "message": "Tài khoản không tồn tại",
                    "debug": debug_info
                }), 401
            
            user_id = result[0]
            db_username = result[1]
            password_hash = result[2]
            status = result[3]
            
            debug_info["details"].append(f"✅ User found: UserID={user_id}, Username={db_username}")
            debug_info["details"].append(f"   Status: {status}")
            debug_info["details"].append(f"   Hash length: {len(password_hash)} chars")
            debug_info["details"].append(f"   Hash prefix: {password_hash[:30]}...")
            
            # Step 2: Check status
            debug_info["step"] = "2. Checking status"
            if status != 'ACTIVE':
                debug_info["details"].append(f"❌ Status is '{status}', not ACTIVE")
                return jsonify({
                    "status": "error",
                    "message": "Tài khoản đã bị khóa",
                    "debug": debug_info
                }), 401
            
            debug_info["details"].append("✅ Status is ACTIVE")
            
            # Step 3: Verify password
            debug_info["step"] = "3. Verifying password"
            debug_info["details"].append(f"   Input password: '{password}'")
            debug_info["details"].append(f"   Password length: {len(password)} chars")
            
            try:
                # Encode
                password_bytes = password.encode('utf-8')
                hash_bytes = password_hash.encode('utf-8')
                
                debug_info["details"].append(f"   Password bytes: {len(password_bytes)} bytes")
                debug_info["details"].append(f"   Hash bytes: {len(hash_bytes)} bytes")
                
                # Check
                is_valid = bcrypt.checkpw(password_bytes, hash_bytes)
                
                if is_valid:
                    debug_info["details"].append("✅ Password CORRECT!")
                    debug_info["step"] = "4. Login SUCCESS"
                    
                    return jsonify({
                        "status": "success",
                        "message": "Đăng nhập thành công",
                        "user": {
                            "userId": user_id,
                            "username": db_username
                        },
                        "debug": debug_info
                    }), 200
                else:
                    debug_info["details"].append("❌ Password INCORRECT!")
                    
                    # Generate correct hash for comparison
                    correct_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
                    debug_info["details"].append(f"   Correct hash would be: {correct_hash[:50]}...")
                    
                    return jsonify({
                        "status": "error",
                        "message": "Mật khẩu không đúng",
                        "debug": debug_info
                    }), 401
                    
            except ValueError as e:
                debug_info["details"].append(f"❌ ValueError: {str(e)}")
                debug_info["details"].append("   Hash format is invalid (not bcrypt)")
                
                return jsonify({
                    "status": "error",
                    "message": "Lỗi xác thực mật khẩu - Hash không hợp lệ",
                    "debug": debug_info
                }), 500
                
            except Exception as e:
                debug_info["details"].append(f"❌ Exception: {str(e)}")
                
                return jsonify({
                    "status": "error",
                    "message": f"Lỗi xác thực mật khẩu: {str(e)}",
                    "debug": debug_info
                }), 500
    
    except Exception as e:
        debug_info["details"].append(f"❌ Database error: {str(e)}")
        
        return jsonify({
            "status": "error",
            "message": f"Lỗi database: {str(e)}",
            "debug": debug_info
        }), 500

@app.route('/test/fix-password', methods=['POST'])
def fix_password():
    """Fix password hash cho user"""
    data = request.get_json()
    username = data.get('username', 'admin')
    new_password = data.get('password', 'admin123')
    
    try:
        engine = create_engine(SQL_SERVER_PERMISSION_CONN)
        
        # Generate new hash
        new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        with engine.connect() as conn:
            with conn.begin():
                # Update password
                sql = text("UPDATE [USER] SET PasswordHash = :password WHERE Username = :username")
                result = conn.execute(sql, {"password": new_hash, "username": username})
                
                if result.rowcount == 0:
                    return jsonify({
                        "status": "error",
                        "message": f"User '{username}' not found"
                    }), 404
                
                return jsonify({
                    "status": "success",
                    "message": f"Password updated for user '{username}'",
                    "new_hash": new_hash,
                    "password": new_password
                }), 200
                
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/test/check-hash', methods=['POST'])
def check_hash():
    """Kiểm tra hash có hợp lệ không"""
    data = request.get_json()
    password = data.get('password')
    hash_str = data.get('hash')
    
    try:
        is_valid = bcrypt.checkpw(password.encode('utf-8'), hash_str.encode('utf-8'))
        
        return jsonify({
            "status": "success",
            "is_valid": is_valid,
            "password": password,
            "hash": hash_str[:50] + "..."
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}",
            "password": password,
            "hash": hash_str[:50] + "..."
        }), 500

@app.route('/test/info', methods=['GET'])
def info():
    """Thông tin test server"""
    return jsonify({
        "status": "success",
        "message": "Test Login Server is running",
        "endpoints": {
            "POST /test/login": "Test login với debug chi tiết",
            "POST /test/fix-password": "Fix password hash cho user",
            "POST /test/check-hash": "Kiểm tra password hash",
            "GET /test/info": "Thông tin server"
        }
    }), 200

if __name__ == '__main__':
    print("="*70)
    print("🧪 TEST LOGIN SERVER")
    print("="*70)
    print("\nEndpoints:")
    print("  POST http://localhost:5001/test/login")
    print("       Body: {\"username\": \"admin\", \"password\": \"admin123\"}")
    print("")
    print("  POST http://localhost:5001/test/fix-password")
    print("       Body: {\"username\": \"admin\", \"password\": \"admin123\"}")
    print("")
    print("  POST http://localhost:5001/test/check-hash")
    print("       Body: {\"password\": \"admin123\", \"hash\": \"$2b$12$...\"}")
    print("")
    print("  GET  http://localhost:5001/test/info")
    print("="*70)
    print("\n🚀 Server starting on http://localhost:5001")
    print("="*70)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
