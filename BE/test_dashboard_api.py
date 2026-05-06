"""
Test Dashboard API
"""
import requests

BASE_URL = "http://localhost:5000/api/v1/dashboard"

print("=" * 60)
print("🧪 TEST DASHBOARD API")
print("=" * 60)

# Test 1: Summary
print("\n1️⃣ Test /summary...")
try:
    response = requests.get(f"{BASE_URL}/summary")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Response: {data}")
    else:
        print(f"   ❌ Error: {response.text}")
except Exception as e:
    print(f"   ❌ Exception: {e}")

# Test 2: Charts
print("\n2️⃣ Test /charts...")
try:
    response = requests.get(f"{BASE_URL}/charts?month=5&year=2026&view_mode=month")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Has bar_chart: {'bar_chart' in data.get('charts', {})}")
        print(f"   ✅ Has line_chart: {'line_chart' in data.get('charts', {})}")
        print(f"   ✅ Has pie_chart: {'pie_chart' in data.get('charts', {})}")
    else:
        print(f"   ❌ Error: {response.text}")
except Exception as e:
    print(f"   ❌ Exception: {e}")

# Test 3: Alerts
print("\n3️⃣ Test /alerts...")
try:
    response = requests.get(f"{BASE_URL}/alerts?month=5&year=2026")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Response: {data}")
    else:
        print(f"   ❌ Error: {response.text}")
except Exception as e:
    print(f"   ❌ Exception: {e}")

print("\n" + "=" * 60)
print("✅ TEST HOÀN TẤT")
print("=" * 60)
