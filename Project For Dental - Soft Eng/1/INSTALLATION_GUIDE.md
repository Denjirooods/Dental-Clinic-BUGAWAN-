# Installation Guide - Macvil Dental Clinic Inventory System

## 🐍 Python Installation

### Windows Users

1. **Download Python**
   - Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Click "Download Python 3.x.x" (latest version)
   - Download the Windows installer (64-bit recommended)

2. **Install Python**
   - Run the downloaded installer
   - **IMPORTANT**: Check "Add Python to PATH" checkbox
   - Choose "Install Now" (recommended)
   - Wait for installation to complete

3. **Verify Installation**
   - Open Command Prompt or PowerShell
   - Type: `python --version`
   - You should see: `Python 3.x.x`

### macOS Users

1. **Using Homebrew (Recommended)**
   ```bash
   brew install python3
   ```

2. **Using Official Installer**
   - Download from [python.org](https://www.python.org/downloads/)
   - Run the macOS installer
   - Follow installation prompts

3. **Verify Installation**
   ```bash
   python3 --version
   ```

### Linux Users

1. **Ubuntu/Debian**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **CentOS/RHEL/Fedora**
   ```bash
   sudo yum install python3 python3-pip
   # or for newer versions:
   sudo dnf install python3 python3-pip
   ```

3. **Verify Installation**
   ```bash
   python3 --version
   ```

## 🚀 System Setup

### Step 1: Download/Extract Project
- Download the project files
- Extract to a folder (e.g., `C:\DentalClinic\` or `/home/user/dental-clinic/`)

### Step 2: Open Terminal/Command Prompt
- **Windows**: Press `Win + R`, type `cmd`, press Enter
- **macOS**: Open Terminal app
- **Linux**: Open terminal application

### Step 3: Navigate to Project Directory
```bash
# Windows
cd C:\DentalClinic

# macOS/Linux
cd /path/to/dental-clinic
```

### Step 4: Install Dependencies
```bash
# Windows
pip install -r requirements.txt

# macOS/Linux
pip3 install -r requirements.txt
```

### Step 5: Run the System
```bash
# Windows
python app.py

# macOS/Linux
python3 app.py
```

### Step 6: Access the System
- Open web browser
- Go to: `http://localhost:5000`
- Login with:
  - Username: `admin`
  - Password: `admin123`

## 🎯 Quick Start Scripts

### Windows Users
1. Double-click `run_system.bat`
2. The system will start automatically
3. Open browser to `http://localhost:5000`

### macOS/Linux Users
1. Make script executable: `chmod +x run_system.sh`
2. Run script: `./run_system.sh`
3. Open browser to `http://localhost:5000`

## 🔧 Troubleshooting

### Python Not Found
**Problem**: `'python' is not recognized as an internal or external command`

**Solution**:
1. Reinstall Python with "Add to PATH" checked
2. Restart Command Prompt/PowerShell
3. Try `python3` instead of `python`

### Port Already in Use
**Problem**: `Address already in use`

**Solution**:
1. Close other applications using port 5000
2. Or change port in `app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

### Permission Denied
**Problem**: `Permission denied` when installing packages

**Solution**:
```bash
# Windows: Run as Administrator
# macOS/Linux: Use sudo
sudo pip3 install -r requirements.txt
```

### Database Errors
**Problem**: Database connection issues

**Solution**:
1. Ensure write permissions in project directory
2. Check available disk space
3. Delete `dental_inventory.db` and restart (will recreate)

## 📱 System Requirements

### Minimum Requirements
- **OS**: Windows 7+, macOS 10.12+, Ubuntu 16.04+
- **Python**: 3.7 or higher
- **RAM**: 2GB available
- **Storage**: 100MB free space
- **Browser**: Chrome 60+, Firefox 55+, Edge 79+

### Recommended Requirements
- **OS**: Windows 10/11, macOS 11+, Ubuntu 20.04+
- **Python**: 3.9 or higher
- **RAM**: 4GB or more
- **Storage**: 500MB free space
- **Browser**: Latest Chrome, Firefox, or Edge

## 🔒 Security Notes

1. **Change Default Password**
   - Login as admin
   - Change password immediately
   - Use strong password (8+ characters, mixed case, numbers)

2. **Network Security**
   - System runs on localhost by default
   - For network access, configure firewall rules
   - Use HTTPS in production environments

3. **Data Backup**
   - Regular backup of `dental_inventory.db`
   - Store backups in secure location
   - Test backup restoration

## 📞 Support

### Before Asking for Help
1. Check this installation guide
2. Verify Python version: `python --version`
3. Check error messages in terminal
4. Ensure all dependencies installed

### Getting Help
- Check system logs in terminal
- Review browser console for errors
- Verify database file exists and is writable

## 🎉 Success Indicators

You'll know the system is working when:
- Terminal shows: `Running on http://0.0.0.0:5000`
- Browser loads login page at `http://localhost:5000`
- Can login with admin/admin123
- Dashboard displays with statistics
- No error messages in terminal

---

**Need Help?** Check the troubleshooting section above or review the README.md file for additional information.



