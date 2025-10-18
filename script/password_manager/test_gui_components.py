#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication

def test_gui_imports():
    print("Testing GUI component imports...")
    try:
        from password_manager import PasswordManager, AddEditDialog
        print("✓ PasswordManager class imported")
        print("✓ AddEditDialog class imported")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_gui_initialization():
    print("\nTesting GUI initialization...")
    try:
        app = QApplication(sys.argv)
        from password_manager import PasswordManager
        
        window = PasswordManager()
        print("✓ Main window created")
        
        assert window.windowTitle() == '密码管理器', "Window title incorrect"
        print("✓ Window title is correct")
        
        assert window.table is not None, "Table widget not initialized"
        print("✓ Table widget initialized")
        
        assert window.add_btn is not None, "Add button not initialized"
        print("✓ Add button initialized")
        
        assert window.edit_btn is not None, "Edit button not initialized"
        print("✓ Edit button initialized")
        
        assert window.delete_btn is not None, "Delete button not initialized"
        print("✓ Delete button initialized")
        
        assert window.copy_password_btn is not None, "Copy password button not initialized"
        print("✓ Copy password button initialized")
        
        assert window.search_input is not None, "Search input not initialized"
        print("✓ Search input initialized")
        
        print("✓ All GUI components initialized successfully")
        return True
    except Exception as e:
        print(f"✗ GUI initialization error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dialog_initialization():
    print("\nTesting dialog initialization...")
    try:
        app = QApplication(sys.argv)
        from password_manager import AddEditDialog
        
        dialog = AddEditDialog()
        print("✓ Add dialog created")
        
        assert dialog.windowTitle() == '添加账号', "Dialog title incorrect for add mode"
        print("✓ Add dialog title is correct")
        
        test_account = {
            'website': 'test.com',
            'username': 'testuser',
            'password': 'testpass',
            'notes': 'test notes'
        }
        edit_dialog = AddEditDialog(account_data=test_account)
        print("✓ Edit dialog created")
        
        assert edit_dialog.windowTitle() == '编辑账号', "Dialog title incorrect for edit mode"
        print("✓ Edit dialog title is correct")
        
        assert edit_dialog.website_input.text() == 'test.com', "Website not loaded"
        print("✓ Website field loaded correctly")
        
        print("✓ Dialog initialization successful")
        return True
    except Exception as e:
        print(f"✗ Dialog initialization error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("Password Manager - GUI Component Tests")
    print("=" * 60)
    
    results = []
    results.append(("Import GUI Components", test_gui_imports()))
    results.append(("GUI Initialization", test_gui_initialization()))
    results.append(("Dialog Initialization", test_dialog_initialization()))
    
    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print("=" * 60)
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print("=" * 60)
    if all_passed:
        print("✓ All GUI component tests passed!")
        print("\nNote: These tests verify that GUI components can be")
        print("initialized correctly. The application needs to be run")
        print("with a display to verify visual appearance.")
    else:
        print("✗ Some tests failed!")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
