#!/bin/bash

echo "========================================"
echo "  Macvil Dental Clinic"
echo "  Inventory Management System"
echo "========================================"
echo ""
echo "Starting the system..."
echo ""
echo "Please wait while the system initializes..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo ""
    echo "Please install Python 3.7 or higher:"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "macOS: brew install python3"
    echo ""
    exit 1
fi

# Check if requirements are installed
echo "Checking dependencies..."
pip3 install -r requirements.txt --quiet

# Start the application
echo ""
echo "Starting Flask application..."
echo ""
echo "The system will be available at: http://localhost:5000"
echo ""
echo "Default login credentials:"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "Press Ctrl+C to stop the system"
echo ""
echo "========================================"
echo ""

python3 app.py

echo ""
echo "System stopped."



