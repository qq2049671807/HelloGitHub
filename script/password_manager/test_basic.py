import os
import sys

def test_imports():
    print("Testing imports...")
    try:
        from crypto_utils import CryptoManager
        print("✓ crypto_utils imported successfully")
        
        from database import DatabaseManager
        print("✓ database imported successfully")
        
        print("\nAll imports successful!")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_crypto():
    print("\nTesting encryption/decryption...")
    try:
        from crypto_utils import CryptoManager
        
        crypto = CryptoManager('test_secret.key')
        
        test_password = "MySecretP@ssw0rd123"
        encrypted = crypto.encrypt(test_password)
        decrypted = crypto.decrypt(encrypted)
        
        assert decrypted == test_password, "Decryption failed"
        print(f"✓ Original: {test_password}")
        print(f"✓ Encrypted: {encrypted[:30]}...")
        print(f"✓ Decrypted: {decrypted}")
        print("✓ Encryption/decryption working correctly")
        
        if os.path.exists('test_secret.key'):
            os.remove('test_secret.key')
        
        return True
    except Exception as e:
        print(f"✗ Crypto test error: {e}")
        if os.path.exists('test_secret.key'):
            os.remove('test_secret.key')
        return False

def test_database():
    print("\nTesting database operations...")
    try:
        from database import DatabaseManager
        
        db = DatabaseManager('test_passwords.db')
        
        account_id = db.add_account(
            website='example.com',
            username='testuser',
            password='testpass123',
            notes='Test notes'
        )
        print(f"✓ Account added with ID: {account_id}")
        
        accounts = db.get_all_accounts()
        assert len(accounts) > 0, "No accounts found"
        print(f"✓ Retrieved {len(accounts)} account(s)")
        
        account = db.get_account_by_id(account_id)
        assert account is not None, "Account not found"
        assert account['website'] == 'example.com', "Website mismatch"
        assert account['password'] == 'testpass123', "Password decryption failed"
        print(f"✓ Account retrieved: {account['website']}")
        
        db.update_account(
            account_id,
            website='updated.com',
            username='updateduser',
            password='newpass456',
            notes='Updated notes'
        )
        updated = db.get_account_by_id(account_id)
        assert updated['website'] == 'updated.com', "Update failed"
        print(f"✓ Account updated successfully")
        
        search_results = db.search_accounts('updated')
        assert len(search_results) > 0, "Search failed"
        print(f"✓ Search found {len(search_results)} result(s)")
        
        db.delete_account(account_id)
        deleted = db.get_account_by_id(account_id)
        assert deleted is None, "Delete failed"
        print(f"✓ Account deleted successfully")
        
        if os.path.exists('test_passwords.db'):
            os.remove('test_passwords.db')
        if os.path.exists('secret.key'):
            os.remove('secret.key')
        
        print("✓ All database operations working correctly")
        return True
    except Exception as e:
        print(f"✗ Database test error: {e}")
        if os.path.exists('test_passwords.db'):
            os.remove('test_passwords.db')
        if os.path.exists('secret.key'):
            os.remove('secret.key')
        return False

def main():
    print("=" * 50)
    print("Password Manager - Basic Functionality Test")
    print("=" * 50)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Encryption", test_crypto()))
    results.append(("Database", test_database()))
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print("=" * 50)
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print("=" * 50)
    if all_passed:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed!")
    print("=" * 50)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
