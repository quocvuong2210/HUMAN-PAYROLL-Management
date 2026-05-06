"""
Test Access Logs API
"""
import requests

API_BASE = "http://localhost:5000"

def test_access_logs_api():
    """Test access logs API"""
    print("="*70)
    print("🧪 TEST ACCESS LOGS API")
    print("="*70)
    
    # 1. Login to get token
    print("\n1️⃣ Login to get token...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        login_response = requests.post(
            f"{API_BASE}/api/v1/auth/login",
            json=login_data
        )
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            token = login_result.get('token')
            print(f"   ✅ Login thành công")
            print(f"   Token: {token[:50]}...")
        else:
            print(f"   ❌ Login thất bại: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            return
    except Exception as e:
        print(f"   ❌ Lỗi login: {e}")
        return
    
    # 2. Get access logs
    print("\n2️⃣ Get access logs...")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        logs_response = requests.get(
            f"{API_BASE}/api/v1/admin/access-logs",
            headers=headers
        )
        
        print(f"   Status Code: {logs_response.status_code}")
        
        if logs_response.status_code == 200:
            logs_result = logs_response.json()
            logs = logs_result.get('data', [])
            
            print(f"   ✅ API hoạt động!")
            print(f"   Số lượng logs: {len(logs)}")
            
            if logs:
                print(f"\n   📋 3 logs mới nhất:")
                for i, log in enumerate(logs[:3], 1):
                    print(f"\n   {i}. {log.get('Username')} - {log.get('Action')}")
                    print(f"      Time: {log.get('AccessTime')}")
                    print(f"      IP: {log.get('IPAddress')}")
            else:
                print(f"   ⚠️  Không có logs nào!")
        else:
            print(f"   ❌ API lỗi: {logs_response.status_code}")
            print(f"   Response: {logs_response.text}")
            
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")
    
    # 3. Get users with roles
    print("\n3️⃣ Get users with roles...")
    
    try:
        users_response = requests.get(
            f"{API_BASE}/api/v1/admin/users-with-roles",
            headers=headers
        )
        
        print(f"   Status Code: {users_response.status_code}")
        
        if users_response.status_code == 200:
            users_result = users_response.json()
            users = users_result.get('data', [])
            
            print(f"   ✅ API hoạt động!")
            print(f"   Số lượng users: {len(users)}")
            
            if users:
                print(f"\n   👥 Danh sách users:")
                for user in users:
                    roles = user.get('UserRoles', [])
                    print(f"   • {user.get('Username')} - {', '.join(roles)}")
        else:
            print(f"   ❌ API lỗi: {users_response.status_code}")
            print(f"   Response: {users_response.text}")
            
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        test_access_logs_api()
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
