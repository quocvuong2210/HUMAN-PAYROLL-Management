"""
Quick test - Kiểm tra nhanh API profile
"""
import requests

BASE_URL = "http://localhost:5000/api/v1/auth"

# 1. Login
print("1. Testing Login...")
response = requests.post(f"{BASE_URL}/login", json={
    "username": "admin",
    "password": "admin123"
})

if response.status_code == 200:
    data = response.json()
    token = data.get("token")
    print(f"✅ Login OK - Token: {token[:50]}...")
    
    # 2. Get Profile
    print("\n2. Testing Get Profile...")
    response = requests.get(f"{BASE_URL}/me", headers={
        "Authorization": f"Bearer {token}"
    })
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        profile = response.json().get("data", {})
        print(f"\n✅ Profile Data:")
        print(f"  - Username: {profile.get('username')}")
        print(f"  - Email: {profile.get('email')}")
        print(f"  - Phone: {profile.get('phone')}")
        print(f"  - DOB: {profile.get('dob')}")
        print(f"  - Gender: {profile.get('gender')}")
        print(f"  - Roles: {len(profile.get('roles', []))}")
    else:
        print(f"❌ Get Profile Failed!")
        
else:
    print(f"❌ Login Failed: {response.status_code}")
    print(response.json())
