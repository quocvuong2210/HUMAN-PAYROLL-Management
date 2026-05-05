"""
Script test tất cả APIs
Kiểm tra xem tất cả endpoints có hoạt động không
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_api(method, endpoint, data=None, headers=None, description=""):
    """Test một API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    print(f"\n{'='*80}")
    print(f"🧪 TEST: {description}")
    print(f"{'='*80}")
    print(f"Method: {method}")
    print(f"URL: {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=5)
        else:
            print(f"❌ Method {method} not supported")
            return False
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200 or response.status_code == 201:
            try:
                json_data = response.json()
                print(f"✅ SUCCESS")
                print(f"Response: {json.dumps(json_data, indent=2, ensure_ascii=False)[:500]}...")
                return True
            except:
                print(f"✅ SUCCESS (No JSON)")
                print(f"Response: {response.text[:200]}")
                return True
        else:
            print(f"❌ FAILED")
            print(f"Response: {response.text[:500]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION ERROR - Server không chạy!")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ TIMEOUT - Server không phản hồi!")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    """Test tất cả APIs"""
    print("\n" + "="*80)
    print("🚀 BẮT ĐẦU TEST TẤT CẢ APIs")
    print("="*80)
    
    results = []
    
    # Test 1: Health Check
    results.append(("Health Check", test_api(
        "GET", "/", 
        description="Health Check - Server có chạy không?"
    )))
    
    # Test 2: Login
    token = None
    login_success = test_api(
        "POST", "/api/v1/auth/login",
        data={"username": "admin", "password": "admin123"},
        description="Login - Đăng nhập với admin"
    )
    results.append(("Login", login_success))
    
    if login_success:
        # Get token from last response (simplified)
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/auth/login",
                json={"username": "admin", "password": "admin123"}
            )
            token = response.json().get("token")
            print(f"\n🔑 Token: {token[:50]}...")
        except:
            print("\n⚠️  Không lấy được token")
    
    headers = {"Authorization": f"Bearer {token}"} if token else None
    
    # Test 3: Departments
    results.append(("Departments", test_api(
        "GET", "/api/v1/departments/",
        headers=headers,
        description="Departments - Lấy danh sách phòng ban"
    )))
    
    # Test 4: Positions
    results.append(("Positions", test_api(
        "GET", "/api/v1/positions/",
        headers=headers,
        description="Positions - Lấy danh sách chức vụ"
    )))
    
    # Test 5: Employees
    results.append(("Employees", test_api(
        "GET", "/api/v1/employees/",
        headers=headers,
        description="Employees - Lấy danh sách nhân viên"
    )))
    
    # Test 6: Users with Roles (Admin only)
    results.append(("Users with Roles", test_api(
        "GET", "/api/v1/admin/users-with-roles",
        headers=headers,
        description="Users - Lấy danh sách users với roles (SUPER_ADMIN only)"
    )))
    
    # Test 7: Access Logs (Admin only)
    results.append(("Access Logs", test_api(
        "GET", "/api/v1/admin/access-logs",
        headers=headers,
        description="Access Logs - Lấy lịch sử truy cập (SUPER_ADMIN only)"
    )))
    
    # Test 8: Current User
    results.append(("Current User", test_api(
        "GET", "/api/v1/auth/me",
        headers=headers,
        description="Current User - Lấy thông tin user hiện tại"
    )))
    
    # Summary
    print("\n" + "="*80)
    print("📊 TÓM TẮT KẾT QUẢ")
    print("="*80)
    
    total = len(results)
    passed = sum(1 for _, success in results if success)
    failed = total - passed
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status:12} | {name}")
    
    print("="*80)
    print(f"Tổng: {total} tests")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/total*100):.1f}%")
    print("="*80)
    
    if failed > 0:
        print("\n⚠️  CÓ LỖI! Kiểm tra:")
        print("1. Backend có đang chạy không? (python app.py)")
        print("2. Database có data không?")
        print("3. Routes có được register không?")
        print("4. CORS có được enable không?")
    else:
        print("\n🎉 TẤT CẢ APIs HOẠT ĐỘNG HOÀN HẢO!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Đã hủy!")
    except Exception as e:
        print(f"\n\n❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()
