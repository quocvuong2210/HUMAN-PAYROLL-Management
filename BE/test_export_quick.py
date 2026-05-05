"""
Quick Test Script for Export Functionality
Run this to verify export libraries are installed and working
"""

def test_imports():
    """Test if required libraries can be imported"""
    print("=" * 60)
    print("TESTING EXPORT LIBRARIES")
    print("=" * 60)
    
    try:
        import openpyxl
        print("✅ openpyxl imported successfully")
        print(f"   Version: {openpyxl.__version__}")
    except ImportError as e:
        print(f"❌ openpyxl import failed: {e}")
        print("   Install with: pip install openpyxl")
        return False
    
    try:
        import reportlab
        print("✅ reportlab imported successfully")
        print(f"   Version: {reportlab.Version}")
    except ImportError as e:
        print(f"❌ reportlab import failed: {e}")
        print("   Install with: pip install reportlab")
        return False
    
    print("\n" + "=" * 60)
    print("TESTING EXPORT SERVICE")
    print("=" * 60)
    
    try:
        from src.services.export_service import ExportService
        print("✅ ExportService imported successfully")
        
        # Test creating an instance
        service = ExportService()
        print("✅ ExportService instance created")
        
        # Test with sample data
        sample_employees = [
            {
                'EmployeeID': 1,
                'FullName': 'Nguyen Van A',
                'Email': 'a@example.com',
                'PhoneNumber': '0123456789',
                'DepartmentName': 'IT',
                'PositionName': 'Developer',
                'Status': 'Đang làm việc',
                'Gender': 'Nam',
                'DateOfBirth': '1990-01-01',
                'HireDate': '2020-01-01'
            }
        ]
        
        print("\n📝 Testing Excel export...")
        excel_file = service.export_employees_to_excel(sample_employees)
        print(f"✅ Excel file created: {excel_file.name}")
        
        print("\n📝 Testing PDF export...")
        pdf_file = service.export_employees_to_pdf(sample_employees)
        print(f"✅ PDF file created: {pdf_file.name}")
        
        print("\n📝 Testing Report Excel export...")
        report_data = {
            'headers': ['Name', 'Salary', 'Bonus'],
            'data': [
                ['Nguyen Van A', 10000000, 1000000],
                ['Tran Thi B', 12000000, 1500000]
            ]
        }
        report_excel = service.export_report_to_excel(report_data, 'salary')
        print(f"✅ Report Excel file created: {report_excel.name}")
        
        print("\n📝 Testing Report PDF export...")
        report_pdf = service.export_report_to_pdf(report_data, 'salary')
        print(f"✅ Report PDF file created: {report_pdf.name}")
        
    except Exception as e:
        print(f"❌ Export service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nExport functionality is ready to use.")
    print("You can now test the API endpoints with the frontend.")
    return True

if __name__ == "__main__":
    success = test_imports()
    if not success:
        print("\n⚠️  Please install missing libraries and try again.")
        exit(1)
    else:
        print("\n🚀 Ready to test export APIs!")
        exit(0)
