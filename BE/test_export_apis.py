"""
Test Export APIs - Script để test các API xuất dữ liệu
"""
import requests
import json

BASE_URL = "http://localhost:5000"

# Test credentials
USERNAME = "admin"
PASSWORD = "admin123"

def login():
    """Login và lấy token"""
    print("🔐 Đang đăng nhập...")
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        json={"username": USERNAME, "password": PASSWORD}
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('data', {}).get('access_token')
        print(f"✅ Đăng nhập thành công! Token: {token[:20]}...")
        return token
    else:
        print(f"❌ Đăng nhập thất bại: {response.status_code}")
        print(response.text)
        return None

def test_export_employees_excel(token):
    """Test xuất danh sách nhân viên ra Excel"""
    print("\n📊 Test: Export Employees to Excel")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test với filters
    params = {
        "name": "",
        "dept_id": "",
        "status": "Đang làm việc"
    }
    
    response = requests.get(
        f"{BASE_URL}/api/v1/export/employees/excel",
        headers=headers,
        params=params
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    
    if response.status_code == 200:
        # Save file
        filename = "test_employees_export.xlsx"
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"✅ File saved: {filename}")
        print(f"File size: {len(response.content)} bytes")
    else:
        print(f"❌ Error: {response.text}")

def test_export_employees_pdf(token):
    """Test xuất danh sách nhân viên ra PDF"""
    print("\n📄 Test: Export Employees to PDF")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(
        f"{BASE_URL}/api/v1/export/employees/pdf",
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    
    if response.status_code == 200:
        # Save file
        filename = "test_employees_export.pdf"
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"✅ File saved: {filename}")
        print(f"File size: {len(response.content)} bytes")
    else:
        print(f"❌ Error: {response.text}")

def test_export_report_excel(token):
    """Test xuất báo cáo ra Excel"""
    print("\n📊 Test: Export Report to Excel")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Sample report data
    report_data = {
        "report_type": "salary",
        "headers": ["Họ tên", "Lương cơ bản", "Thưởng", "Khấu trừ", "Thực nhận"],
        "data": [
            ["Nguyễn Văn A", 15000000, 2000000, 500000, 16500000],
            ["Trần Thị B", 12000000, 1500000, 300000, 13200000],
            ["Lê Văn C", 18000000, 3000000, 800000, 20200000]
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/export/report/excel",
        headers=headers,
        json=report_data
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    
    if response.status_code == 200:
        # Save file
        filename = "test_report_export.xlsx"
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"✅ File saved: {filename}")
        print(f"File size: {len(response.content)} bytes")
    else:
        print(f"❌ Error: {response.text}")

def test_export_report_pdf(token):
    """Test xuất báo cáo ra PDF"""
    print("\n📄 Test: Export Report to PDF")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Sample report data
    report_data = {
        "report_type": "attendance",
        "headers": ["Họ tên", "Ngày công", "Ngày nghỉ", "Ngày phép"],
        "data": [
            ["Nguyễn Văn A", 22, 1, 0],
            ["Trần Thị B", 20, 2, 1],
            ["Lê Văn C", 23, 0, 0]
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/export/report/pdf",
        headers=headers,
        json=report_data
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    
    if response.status_code == 200:
        # Save file
        filename = "test_report_export.pdf"
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"✅ File saved: {filename}")
        print(f"File size: {len(response.content)} bytes")
    else:
        print(f"❌ Error: {response.text}")

def main():
    """Main test function"""
    print("=" * 60)
    print("🚀 EXPORT API TESTING")
    print("=" * 60)
    
    # Login
    token = login()
    if not token:
        print("❌ Cannot proceed without token")
        return
    
    # Test all export endpoints
    test_export_employees_excel(token)
    test_export_employees_pdf(token)
    test_export_report_excel(token)
    test_export_report_pdf(token)
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main()
