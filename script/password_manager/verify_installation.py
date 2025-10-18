#!/usr/bin/env python3
import sys
import os

def check_python_version():
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} detected")
        print("  Python 3.7 or higher is required!")
        return False

def check_dependencies():
    print("\nChecking dependencies...")
    missing = []
    
    try:
        import PyQt5
        print("✓ PyQt5 is installed")
    except ImportError:
        print("✗ PyQt5 is not installed")
        missing.append("PyQt5")
    
    try:
        import cryptography
        print("✓ cryptography is installed")
    except ImportError:
        print("✗ cryptography is not installed")
        missing.append("cryptography")
    
    return missing

def check_files():
    print("\nChecking required files...")
    required_files = [
        'password_manager.py',
        'database.py',
        'crypto_utils.py',
        'requirements.txt',
        'README.md'
    ]
    
    all_present = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} found")
        else:
            print(f"✗ {file} not found")
            all_present = False
    
    return all_present

def main():
    print("=" * 60)
    print("Password Manager - Installation Verification")
    print("=" * 60)
    
    results = []
    
    results.append(check_python_version())
    
    missing_deps = check_dependencies()
    results.append(len(missing_deps) == 0)
    
    results.append(check_files())
    
    print("\n" + "=" * 60)
    print("Verification Summary:")
    print("=" * 60)
    
    if all(results):
        print("✓ All checks passed!")
        print("\nYou can now run the Password Manager:")
        if os.name == 'nt':
            print("  - Double-click run.bat")
            print("  - Or run: python password_manager.py")
        else:
            print("  - Run: ./run.sh")
            print("  - Or run: python3 password_manager.py")
    else:
        print("✗ Some checks failed!")
        if missing_deps:
            print(f"\nMissing dependencies: {', '.join(missing_deps)}")
            print("Please install them by running:")
            print("  pip install -r requirements.txt")
    
    print("=" * 60)
    
    return 0 if all(results) else 1

if __name__ == '__main__':
    sys.exit(main())
