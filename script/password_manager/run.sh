#!/bin/bash

# Password Manager Launcher Script

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ -d "../../.venv" ]; then
    echo "Using virtual environment..."
    PYTHON="../../.venv/bin/python3"
else
    echo "Virtual environment not found, using system Python..."
    PYTHON="python3"
fi

# Check if dependencies are installed
$PYTHON -c "import PyQt5; import cryptography" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    $PYTHON -m pip install -r requirements.txt
fi

# Run the password manager
echo "Starting Password Manager..."
$PYTHON password_manager.py

exit 0
