"""
Test đăng nhập và lấy profile
"""
import requests
import json

BASE_URL = "http://localhost:5000/api/v1/auth"

print("=" * 80)
print("TEST ĐĂNG NHẬP VÀ PROFILE")
print("=" * 80)

# 1. Login
print("\n1️⃣ ĐĂNG NHẬP...")
response = requests.post(f"{BASE_URL}/login", json={
    "username": "admin",
    "password": "admin123"
})

print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"✅ Đăng nhập thành công!")
    
    token = data.get("token")
    print(f"\n🔑 Token (50 ký tự đầu): {token[:50]}...")
    
    # 2. Get Profile
    print("\n2️⃣ LẤY PROFILE...")
    response = requests.get(f"{BASE_URL}/me", headers={
        "Authorization": f"Bearer {token}"
    })
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        profile_data = response.json()
        print(f"✅ Lấy profile thành công!")
        print(f"\n📊 THÔNG TIN PROFILE:")
        print(json.dumps(profile_data, indent=2, ensure_ascii=False))
        
        # Extract data
        profile = profile_data.get("data", {})
        print(f"\n📋 SUMMARY:")
        print(f"  - Username: {profile.get('username')}")
        print(f"  - Email: {profile.get('email')}")
        print(f"  - Phone: {profile.get('phone')}")
        print(f"  - DOB: {profile.get('dob')}")
        print(f"  - Gender: {profile.get('gender')}")
        print(f"  - Status: {profile.get('status')}")
        print(f"  - Roles: {len(profile.get('roles', []))}")
        print(f"  - Permissions: {len(profile.get('permissions', []))}")
        print(f"  - Functions: {len(profile.get('functions', []))}")
        
    else:
        print(f"❌ Lấy profile thất bại!")
        print(f"Response: {response.json()}")
        
    # 3. Get Access Logs
    print("\n3️⃣ LẤY ACCESS LOGS...")
    response = requests.get(f"{BASE_URL}/my-access-logs?limit=5", headers={
        "Authorization": f"Bearer {token}"
    })
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        logs_data = response.json()
        print(f"✅ Lấy access logs thành công!")
        logs = logs_data.get("data", [])
        print(f"  - Số logs: {len(logs)}")
        
        if logs:
            print(f"\n📜 3 LOGS GẦN NHẤT:")
            for i, log in enumerate(logs[:3], 1):
                print(f"  {i}. {log.get('Action')} - {log.get('AccessTime')} - {log.get('IPAddress')}")
    else:
        print(f"❌ Lấy access logs thất bại!")
        print(f"Response: {response.json()}")
        
else:
    print(f"❌ Đăng nhập thất bại!")
    print(f"Response: {response.json()}")

print("\n" + "=" * 80)
print("KẾT THÚC TEST")
print("=" * 80)
