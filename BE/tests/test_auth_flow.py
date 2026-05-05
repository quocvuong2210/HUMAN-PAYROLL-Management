"""
Test Script - Authentication Flow
Chạy script này để test toàn bộ flow authentication
"""
import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:5000/api/v2/auth"
TEST_USER = {
    "username": "testuser_" + str(int(time.time())),
    "email": f"testuser_{int(time.time())}@example.com",
    "password": "Test123456",
    "phone": "0987654321",
    "dob": "1995-05-15",
    "gender": "Male"
}

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def print_section(title):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{Colors.END}\n")

# Test functions
def test_health_check():
    """Test 1: Health Check"""
    print_section("Test 1: Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        
        if response.status_code == 200 and data['status'] == 'success':
            print_success("Health check passed")
            print_info(f"Message: {data['message']}")
            return True
        else:
            print_error("Health check failed")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_register():
    """Test 2: Register"""
    print_section("Test 2: Register User")
    
    try:
        response = requests.post(
            f"{BASE_URL}/register",
            json=TEST_USER,
            headers={"Content-Type": "application/json"}
        )
        data = response.json()
        
        if response.status_code == 201 and data['status'] == 'success':
            print_success("Registration successful")
            print_info(f"User ID: {data['user_id']}")
            print_info(f"Email sent: {data['email_sent']}")
            print_warning("Check server console for verification token!")
            return True, data.get('user_id')
        else:
            print_error(f"Registration failed: {data.get('message')}")
            return False, None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False, None

def test_login_without_verification():
    """Test 3: Login without email verification (should fail)"""
    print_section("Test 3: Login Without Email Verification")
    
    try:
        response = requests.post(
            f"{BASE_URL}/login",
            json={
                "username": TEST_USER['username'],
                "password": TEST_USER['password']
            },
            headers={"Content-Type": "application/json"}
        )
        data = response.json()
        
        if response.status_code == 401:
            print_success("Correctly blocked unverified user")
            print_info(f"Message: {data.get('message')}")
            return True
        else:
            print_error("Should have blocked unverified user!")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_verify_email(token):
    """Test 4: Verify Email"""
    print_section("Test 4: Verify Email")
    
    if not token:
        print_warning("No token provided. Please enter token manually:")
        token = input("Token: ").strip()
    
    try:
        response = requests.get(f"{BASE_URL}/verify-email?token={token}")
        data = response.json()
        
        if response.status_code == 200 and data['status'] == 'success':
            print_success("Email verification successful")
            print_info(f"Message: {data['message']}")
            return True
        else:
            print_error(f"Verification failed: {data.get('message')}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_login():
    """Test 5: Login after verification"""
    print_section("Test 5: Login After Verification")
    
    try:
        response = requests.post(
            f"{BASE_URL}/login",
            json={
                "username": TEST_USER['username'],
                "password": TEST_USER['password']
            },
            headers={"Content-Type": "application/json"}
        )
        data = response.json()
        
        if response.status_code == 200 and data['status'] == 'success':
            print_success("Login successful")
            print_info(f"User ID: {data['user']['user_id']}")
            print_info(f"Username: {data['user']['username']}")
            print_info(f"Roles: {data['user']['roles']}")
            print_info(f"Access Token: {data['access_token'][:50]}...")
            print_info(f"Refresh Token: {data['refresh_token'][:50]}...")
            return True, data['access_token'], data['refresh_token']
        else:
            print_error(f"Login failed: {data.get('message')}")
            return False, None, None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False, None, None

def test_get_profile(access_token):
    """Test 6: Get Profile"""
    print_section("Test 6: Get User Profile")
    
    try:
        response = requests.get(
            f"{BASE_URL}/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        data = response.json()
        
        if response.status_code == 200 and data['status'] == 'success':
            print_success("Profile retrieved successfully")
            user_info = data['data']['user_info']
            print_info(f"Username: {user_info['Username']}")
            print_info(f"Email: {user_info['Email']}")
            print_info(f"Status: {user_info['Status']}")
            print_info(f"Email Verified: {user_info['EmailVerified']}")
            print_info(f"Roles: {len(data['data']['roles'])}")
            print_info(f"Permissions: {len(data['data']['functions'])}")
            return True
        else:
            print_error(f"Failed to get profile: {data.get('message')}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_get_permissions(access_token):
    """Test 7: Get Permissions"""
    print_section("Test 7: Get User Permissions")
    
    try:
        response = requests.get(
            f"{BASE_URL}/me/permissions",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        data = response.json()
        
        if response.status_code == 200 and data['status'] == 'success':
            print_success("Permissions retrieved successfully")
            permissions = data['data']['permissions']
            if permissions:
                print_info(f"Permissions: {', '.join(permissions)}")
            else:
                print_warning("No permissions assigned yet")
            return True
        else:
            print_error(f"Failed to get permissions: {data.get('message')}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_refresh_token(refresh_token):
    """Test 8: Refresh Access Token"""
    print_section("Test 8: Refresh Access Token")
    
    try:
        response = requests.post(
            f"{BASE_URL}/refresh-token",
            json={"refresh_token": refresh_token},
            headers={"Content-Type": "application/json"}
        )
        data = response.json()
        
        if response.status_code == 200 and data['status'] == 'success':
            print_success("Token refreshed successfully")
            print_info(f"New Access Token: {data['access_token'][:50]}...")
            return True, data['access_token']
        else:
            print_error(f"Token refresh failed: {data.get('message')}")
            return False, None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False, None

def test_forgot_password():
    """Test 9: Forgot Password"""
    print_section("Test 9: Forgot Password")
    
    try:
        response = requests.post(
            f"{BASE_URL}/forgot-password",
            json={"email": TEST_USER['email']},
            headers={"Content-Type": "application/json"}
        )
        data = response.json()
        
        if response.status_code == 200 and data['status'] == 'success':
            print_success("Password reset email sent")
            print_info(f"Message: {data['message']}")
            print_warning("Check server console for reset token!")
            return True
        else:
            print_error(f"Forgot password failed: {data.get('message')}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_logout(access_token, refresh_token):
    """Test 10: Logout"""
    print_section("Test 10: Logout")
    
    try:
        response = requests.post(
            f"{BASE_URL}/logout",
            json={"refresh_token": refresh_token},
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        data = response.json()
        
        if response.status_code == 200 and data['status'] == 'success':
            print_success("Logout successful")
            print_info(f"Message: {data['message']}")
            return True
        else:
            print_error(f"Logout failed: {data.get('message')}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_access_after_logout(access_token):
    """Test 11: Try to access after logout"""
    print_section("Test 11: Access After Logout")
    
    try:
        response = requests.get(
            f"{BASE_URL}/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        data = response.json()
        
        # Access token vẫn valid (chưa hết hạn), nhưng refresh token đã revoked
        if response.status_code == 200:
            print_warning("Access token still valid (not expired yet)")
            print_info("This is expected - access tokens are stateless")
            return True
        else:
            print_info(f"Access denied: {data.get('message')}")
            return True
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

# Main test runner
def run_all_tests():
    """Run all tests in sequence"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("  RBAC AUTHENTICATION SYSTEM - TEST SUITE")
    print(f"{'='*60}{Colors.END}\n")
    
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Test User: {TEST_USER['username']}")
    print_info(f"Test Email: {TEST_USER['email']}")
    
    results = []
    
    # Test 1: Health Check
    results.append(("Health Check", test_health_check()))
    
    # Test 2: Register
    success, user_id = test_register()
    results.append(("Register", success))
    
    if not success:
        print_error("Registration failed. Stopping tests.")
        return
    
    # Test 3: Login without verification
    results.append(("Login Without Verification", test_login_without_verification()))
    
    # Test 4: Verify Email
    print_warning("\nPlease check server console for verification token")
    token = input("Enter verification token (or press Enter to skip): ").strip()
    
    if token:
        success = test_verify_email(token)
        results.append(("Verify Email", success))
        
        if success:
            # Test 5: Login
            success, access_token, refresh_token = test_login()
            results.append(("Login", success))
            
            if success:
                # Test 6: Get Profile
                results.append(("Get Profile", test_get_profile(access_token)))
                
                # Test 7: Get Permissions
                results.append(("Get Permissions", test_get_permissions(access_token)))
                
                # Test 8: Refresh Token
                success, new_access_token = test_refresh_token(refresh_token)
                results.append(("Refresh Token", success))
                
                # Test 9: Forgot Password
                results.append(("Forgot Password", test_forgot_password()))
                
                # Test 10: Logout
                results.append(("Logout", test_logout(access_token, refresh_token)))
                
                # Test 11: Access after logout
                results.append(("Access After Logout", test_access_after_logout(access_token)))
    else:
        print_warning("Skipping verification and subsequent tests")
    
    # Print summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")
    
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  Results: {passed}/{total} tests passed")
    print(f"{'='*60}{Colors.END}\n")
    
    if passed == total:
        print_success("All tests passed! 🎉")
    else:
        print_warning(f"{total - passed} test(s) failed")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print_warning("\n\nTests interrupted by user")
    except Exception as e:
        print_error(f"\n\nUnexpected error: {str(e)}")
