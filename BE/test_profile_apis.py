"""
Test Profile APIs - Test tất cả APIs liên quan đến profile
"""
import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000/api/v1/auth"
TEST_USER = {
    "username": "admin",
    "password": "admin123"
}

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{'='*80}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{'='*80}\n")

def print_test(text):
    print(f"{Colors.BOLD}🧪 TEST: {text}{Colors.RESET}")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.YELLOW}ℹ️  {text}{Colors.RESET}")

def print_response(response):
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")

# Test 1: Login
def test_login():
    print_test("Login - Đăng nhập để lấy token")
    
    url = f"{BASE_URL}/login"
    payload = TEST_USER
    
    response = requests.post(url, json=payload)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success":
            token = data.get("token")
            print_success(f"Login thành công! Token: {token[:50]}...")
            return token
        else:
            print_error(f"Login thất bại: {data.get('message')}")
            return None
    else:
        print_error(f"Login thất bại với status code: {response.status_code}")
        return None

# Test 2: Get Profile
def test_get_profile(token):
    print_test("Get Profile - Lấy thông tin profile")
    
    url = f"{BASE_URL}/me"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success":
            profile = data.get("data")
            print_success("Lấy profile thành công!")
            print_info(f"Username: {profile.get('username')}")
            print_info(f"Email: {profile.get('email')}")
            print_info(f"Roles: {len(profile.get('roles', []))} roles")
            print_info(f"Permissions: {len(profile.get('permissions', []))} permissions")
            print_info(f"Functions: {len(profile.get('functions', []))} functions")
            return profile
        else:
            print_error(f"Lấy profile thất bại: {data.get('message')}")
            return None
    else:
        print_error(f"Lấy profile thất bại với status code: {response.status_code}")
        return None

# Test 3: Update Profile
def test_update_profile(token):
    print_test("Update Profile - Cập nhật thông tin profile")
    
    url = f"{BASE_URL}/profile"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "email": "admin@company.com",
        "phone": "0901234567",
        "dob": "1990-01-15",
        "gender": "Nam"
    }
    
    response = requests.put(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success":
            print_success("Cập nhật profile thành công!")
            profile = data.get("data")
            print_info(f"Email: {profile.get('email')}")
            print_info(f"Phone: {profile.get('phone')}")
            print_info(f"DOB: {profile.get('dob')}")
            print_info(f"Gender: {profile.get('gender')}")
            return True
        else:
            print_error(f"Cập nhật profile thất bại: {data.get('message')}")
            return False
    else:
        print_error(f"Cập nhật profile thất bại với status code: {response.status_code}")
        return False

# Test 4: Change Password (same password)
def test_change_password(token):
    print_test("Change Password - Đổi mật khẩu (giữ nguyên)")
    
    url = f"{BASE_URL}/change-password"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "oldPassword": "admin123",
        "newPassword": "admin123"  # Giữ nguyên để không ảnh hưởng test
    }
    
    response = requests.post(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success":
            print_success("Đổi mật khẩu thành công!")
            return True
        else:
            print_error(f"Đổi mật khẩu thất bại: {data.get('message')}")
            return False
    else:
        print_error(f"Đổi mật khẩu thất bại với status code: {response.status_code}")
        return False

# Test 5: Change Password - Wrong Old Password
def test_change_password_wrong(token):
    print_test("Change Password - Đổi mật khẩu với mật khẩu cũ SAI")
    
    url = f"{BASE_URL}/change-password"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "oldPassword": "wrongpassword",
        "newPassword": "newpass123"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 400:
        data = response.json()
        if data.get("status") == "error":
            print_success("Validation đúng! Từ chối mật khẩu cũ sai")
            return True
        else:
            print_error("Validation sai! Không từ chối mật khẩu cũ sai")
            return False
    else:
        print_error(f"Kết quả không mong đợi với status code: {response.status_code}")
        return False

# Test 6: Get Access Logs
def test_get_access_logs(token):
    print_test("Get Access Logs - Lấy lịch sử truy cập")
    
    url = f"{BASE_URL}/my-access-logs?limit=10"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success":
            logs = data.get("data", [])
            count = data.get("count", 0)
            print_success(f"Lấy access logs thành công! Có {count} logs")
            
            if logs:
                print_info("3 logs gần nhất:")
                for i, log in enumerate(logs[:3], 1):
                    print(f"  {i}. {log.get('Action')} - {log.get('AccessTime')} - {log.get('IPAddress')}")
            else:
                print_info("Chưa có logs")
            
            return True
        else:
            print_error(f"Lấy access logs thất bại: {data.get('message')}")
            return False
    else:
        print_error(f"Lấy access logs thất bại với status code: {response.status_code}")
        return False

# Test 7: Get Access Logs with different limit
def test_get_access_logs_limit(token):
    print_test("Get Access Logs - Lấy lịch sử với limit=5")
    
    url = f"{BASE_URL}/my-access-logs?limit=5"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success":
            count = data.get("count", 0)
            print_success(f"Lấy access logs thành công! Có {count} logs (limit=5)")
            
            if count <= 5:
                print_success("Limit hoạt động đúng!")
                return True
            else:
                print_error(f"Limit không hoạt động! Trả về {count} logs thay vì ≤5")
                return False
        else:
            print_error(f"Lấy access logs thất bại: {data.get('message')}")
            return False
    else:
        print_error(f"Lấy access logs thất bại với status code: {response.status_code}")
        return False

# Test 8: Unauthorized Access
def test_unauthorized_access():
    print_test("Unauthorized Access - Truy cập không có token")
    
    url = f"{BASE_URL}/me"
    
    response = requests.get(url)
    
    if response.status_code == 401:
        print_success("Authorization hoạt động đúng! Từ chối truy cập không có token")
        return True
    else:
        print_error(f"Authorization sai! Status code: {response.status_code}")
        return False

# Main test runner
def run_all_tests():
    print_header("🚀 BẮT ĐẦU TEST PROFILE APIs")
    
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0
    }
    
    # Test 1: Login
    print_header("TEST 1: Login")
    token = test_login()
    results["total"] += 1
    if token:
        results["passed"] += 1
    else:
        results["failed"] += 1
        print_error("Không thể tiếp tục test vì login thất bại!")
        return
    
    # Test 2: Get Profile
    print_header("TEST 2: Get Profile")
    profile = test_get_profile(token)
    results["total"] += 1
    if profile:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 3: Update Profile
    print_header("TEST 3: Update Profile")
    success = test_update_profile(token)
    results["total"] += 1
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 4: Change Password
    print_header("TEST 4: Change Password (Same Password)")
    success = test_change_password(token)
    results["total"] += 1
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 5: Change Password - Wrong Old Password
    print_header("TEST 5: Change Password (Wrong Old Password)")
    success = test_change_password_wrong(token)
    results["total"] += 1
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 6: Get Access Logs
    print_header("TEST 6: Get Access Logs")
    success = test_get_access_logs(token)
    results["total"] += 1
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 7: Get Access Logs with Limit
    print_header("TEST 7: Get Access Logs (Limit=5)")
    success = test_get_access_logs_limit(token)
    results["total"] += 1
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 8: Unauthorized Access
    print_header("TEST 8: Unauthorized Access")
    success = test_unauthorized_access()
    results["total"] += 1
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Summary
    print_header("📊 TÓM TẮT KẾT QUẢ")
    print(f"Tổng: {results['total']} tests")
    print_success(f"Passed: {results['passed']}")
    print_error(f"Failed: {results['failed']}")
    
    success_rate = (results['passed'] / results['total']) * 100
    print(f"\n{Colors.BOLD}📈 Success Rate: {success_rate:.1f}%{Colors.RESET}\n")
    
    if results['failed'] == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 TẤT CẢ PROFILE APIs HOẠT ĐỘNG HOÀN HẢO!{Colors.RESET}\n")
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  CÓ {results['failed']} TEST THẤT BẠI!{Colors.RESET}\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Test bị dừng bởi user{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Lỗi: {str(e)}{Colors.RESET}")
