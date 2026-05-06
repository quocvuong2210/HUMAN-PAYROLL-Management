"""
Test login trực tiếp với UserModel để debug
"""
import sys
sys.path.insert(0, 'BE')

from src.models.userModel import UserModel

def test_login():
    """Test login trực tiếp"""
    print("🔍 Testing login với UserModel...")
    
    model = UserModel()
    
    # Test login
    username = "admin"
    password = "admin123"
    ip = "127.0.0.1"
    ua = "Test Script"
    
    print(f"\n📝 Đang test login:")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    
    try:
        success, result = model.login(username, password, ip, ua)
        
        if success:
            print(f"\n✅ LOGIN THÀNH CÔNG!")
            print(f"   UserID: {result}")
        else:
            print(f"\n❌ LOGIN THẤT BẠI!")
            print(f"   Lỗi: {result}")
            
    except Exception as e:
        print(f"\n❌ EXCEPTION!")
        print(f"   Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_login()
