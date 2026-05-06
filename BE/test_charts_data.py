"""
Test Charts Data Structure
"""
import requests
import json

BASE_URL = "http://localhost:5000/api/v1/dashboard"

print("=" * 60)
print("🔍 KIỂM TRA DỮ LIỆU CHARTS")
print("=" * 60)

# Test Charts endpoint
print("\n📊 Test /charts...")
try:
    response = requests.get(f"{BASE_URL}/charts?month=5&year=2026&view_mode=month")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        print("\n✅ Response structure:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # Kiểm tra chi tiết
        charts = data.get('charts', {})
        
        print("\n📈 Bar Chart (Chi phí bộ phận):")
        bar_chart = charts.get('bar_chart', [])
        print(f"   - Số lượng: {len(bar_chart)}")
        if bar_chart:
            print(f"   - Mẫu: {bar_chart[0]}")
        else:
            print("   ⚠️ RỖNG!")
        
        print("\n📉 Line Chart (Chi tiết năm):")
        line_chart = charts.get('line_chart', [])
        print(f"   - Số lượng: {len(line_chart)}")
        if line_chart:
            print(f"   - Mẫu: {line_chart[0]}")
        else:
            print("   ⚠️ RỖNG!")
        
        print("\n🥧 Pie Chart (Phân bổ nhân sự):")
        pie_chart = charts.get('pie_chart', [])
        print(f"   - Số lượng: {len(pie_chart)}")
        if pie_chart:
            print(f"   - Mẫu: {pie_chart[0]}")
        else:
            print("   ⚠️ RỖNG!")
            
    else:
        print(f"❌ Error: {response.text}")
        
except Exception as e:
    print(f"❌ Exception: {e}")

print("\n" + "=" * 60)
