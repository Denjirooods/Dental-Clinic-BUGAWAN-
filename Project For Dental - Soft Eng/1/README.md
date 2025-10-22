# Macvil Dental Clinic - Inventory Management System

A professional, standalone inventory and supply management system designed specifically for Macvil Dental Clinic. This system provides a comprehensive solution for tracking dental supplies, monitoring stock levels, and managing inventory efficiently.

## 🏥 System Overview

The Macvil Dental Clinic Inventory Management System is a web-based application built with Python Flask and SQLite database. It features a modern, Google Material Design-inspired interface that's clean, professional, and easy to use.

### Key Features

- **Dashboard Overview**: Real-time statistics and alerts
- **Inventory Management**: Add, edit, delete, and track inventory items
- **Stock Tracking**: Monitor current stock levels and minimum thresholds
- **Expiration Management**: Track expiration dates and receive alerts
- **Category Organization**: Organize items into logical categories
- **Transaction History**: Complete audit trail of all stock movements
- **Reports & Analytics**: Comprehensive reporting capabilities
- **User Authentication**: Secure login system
- **Responsive Design**: Works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Windows 10/11 (or compatible operating system)
- Modern web browser (Chrome, Firefox, Edge)

### Installation

1. **Clone or Download** the project files to your computer
2. **Open Command Prompt** or PowerShell in the project directory
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application**:
   ```bash
   python app.py
   ```
5. **Open Browser** and navigate to: `http://localhost:5000`

### Default Login

- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Important**: Change the default password after first login for security.

## 📱 System Features

### Dashboard
- Overview of total inventory items
- Low stock alerts
- Expiring items warnings
- Recent activity feed
- Category distribution charts

### Inventory Management
- **Add Items**: Comprehensive form for new inventory items
- **Edit Items**: Modify existing item details
- **Delete Items**: Remove items from inventory
- **Search & Filter**: Find items quickly by name or category
- **Stock Adjustment**: Add or remove stock with transaction tracking

### Categories
- Pre-configured dental supply categories
- Add custom categories
- Organize items logically
- Category-based reporting

### Reports
- **Low Stock Report**: Items below minimum levels
- **Expiring Items**: Items nearing expiration
- **Category Summary**: Overview by category
- **Print Support**: Generate printable reports

### Transactions
- Complete history of stock movements
- Search by date range
- Filter by transaction type
- Audit trail for compliance

## 🗄️ Database Structure

The system uses SQLite database with the following tables:

- **users**: User authentication and management
- **categories**: Item categorization
- **inventory**: Main inventory items
- **transactions**: Stock movement history

## 🎨 User Interface

### Design Principles
- **Clean & Professional**: Google Material Design inspired
- **Responsive**: Works on all device sizes
- **Intuitive**: Easy navigation and user experience
- **Accessible**: Clear typography and color contrast

### Color Scheme
- **Primary**: Blue (#1976d2) - Professional medical theme
- **Success**: Green (#4caf50) - Positive actions
- **Warning**: Orange (#ff9800) - Caution alerts
- **Error**: Red (#f44336) - Critical issues
- **Info**: Blue (#2196f3) - Informational content

## 🔧 Configuration

### Environment Variables
The system can be configured through environment variables:

```bash
# Flask configuration
export FLASK_ENV=production
export FLASK_DEBUG=0

# Database configuration
export DATABASE_URL=sqlite:///dental_inventory.db
```

### Customization
- Modify `static/style.css` for visual changes
- Update `templates/` for layout modifications
- Edit `app.py` for functionality changes

## 📊 Usage Examples

### Adding New Inventory Item
1. Navigate to **Inventory** → **Add New Item**
2. Fill in required fields:
   - Item name (e.g., "Disposable Gloves")
   - Category (e.g., "Gloves")
   - Current stock quantity
   - Minimum stock level
   - Unit (e.g., "boxes")
3. Add optional details like supplier, cost, location
4. Click **Add Item**

### Adjusting Stock Levels
1. Go to **Inventory** and find the item
2. Click **Adjust Stock** button
3. Choose **Add Stock** or **Remove Stock**
4. Enter quantity and notes
5. Click **Update Stock**

### Generating Reports
1. Navigate to **Reports** section
2. View automatic reports:
   - Low stock alerts
   - Expiring items
   - Category summaries
3. Use **Print Reports** for hard copies

## 🛡️ Security Features

- **User Authentication**: Login required for all operations
- **Session Management**: Secure session handling
- **Input Validation**: Form validation and sanitization
- **SQL Injection Protection**: Parameterized queries
- **XSS Protection**: Template escaping

## 📱 Mobile Support

The system is fully responsive and works on:
- Desktop computers
- Laptops
- Tablets
- Mobile phones

## 🖨️ Printing Support

All reports and tables support printing:
- Clean, formatted output
- No navigation elements
- Optimized for paper printing
- Professional appearance

## 🔄 Data Backup

### Automatic Backup
- Database file: `dental_inventory.db`
- Store in secure location
- Regular backup recommended

### Manual Backup
```bash
# Copy database file
copy dental_inventory.db backup_dental_inventory.db
```

## 🚨 Troubleshooting

### Common Issues

**Application won't start:**
- Check Python version (3.7+ required)
- Verify all dependencies installed
- Check port 5000 availability

**Database errors:**
- Ensure write permissions in project directory
- Check disk space availability
- Verify SQLite support

**Login issues:**
- Use default credentials: admin/admin123
- Clear browser cache and cookies
- Check session storage

### Support
For technical support or questions:
- Check system logs in console
- Verify database file integrity
- Review error messages in browser console

## 📈 Future Enhancements

Potential future features:
- **Barcode Scanning**: QR code support for items
- **Email Alerts**: Automated low stock notifications
- **Data Export**: CSV/Excel export functionality
- **Backup Automation**: Scheduled database backups
- **Multi-user Support**: Role-based access control

## 📄 License

This system is developed specifically for Macvil Dental Clinic. All rights reserved.

## 👥 Credits

**Developed by:** Angelo A. Bugawan  
**Client:** Macvil Dental Clinic  
**Address:** 33 MH Del Pilar, Tugatog, Malabon City, Malabon, Philippines  
**Contact:** 0976 485 2052

---

**Version:** 1.0.0  
**Last Updated:** December 2025  
**System Requirements:** Windows 10/11, Python 3.7+, Modern Web Browser
