from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from datetime import datetime
import hashlib
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Generate secure secret key

def hash_password(password):
    """Hash a password using SHA-256 with salt"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}:{password_hash}"

def verify_password(password, stored_password):
    """Verify a password against its hash"""
    try:
        salt, password_hash = stored_password.split(':')
        return hashlib.sha256((password + salt).encode()).hexdigest() == password_hash
    except:
        return False

def init_db():
    conn = sqlite3.connect('inventory.db', timeout=10)
    c = conn.cursor()
    c.execute('PRAGMA journal_mode=WAL')
    c.execute('PRAGMA busy_timeout=5000')
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS categories
                 (id INTEGER PRIMARY KEY, name TEXT UNIQUE, description TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                 (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER, min_level INTEGER, unit TEXT, 
                  category_id INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (category_id) REFERENCES categories (id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY, item_id INTEGER, transaction_type TEXT, quantity INTEGER, 
                  reason TEXT, user_id INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (item_id) REFERENCES inventory (id),
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS login_attempts
                 (username TEXT PRIMARY KEY, failed_count INTEGER, lock_until INTEGER)''')
    
    # Insert default category if none exists
    c.execute("SELECT COUNT(*) FROM categories")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO categories (name, description) VALUES (?, ?)", 
                 ("General", "General inventory items"))
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and password are required')
            return render_template('login.html')

        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()

        # Check current lockout status
        c.execute("SELECT failed_count, lock_until FROM login_attempts WHERE username=?", (username,))
        attempt = c.fetchone()
        now_ts = int(datetime.now().timestamp())
        if attempt and attempt[1] and attempt[1] > now_ts:
            remaining = attempt[1] - now_ts
            minutes = remaining // 60
            seconds = remaining % 60
            conn.close()
            flash(f'Account locked. Try again in {minutes}m {seconds}s')
            return render_template('login.html')

        # Perform credential check
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        
        if user and verify_password(password, user[2]):
            # Successful login: reset any attempt tracking
            session['logged_in'] = True
            session['username'] = username
            session['user_id'] = user[0]
            c.execute("DELETE FROM login_attempts WHERE username=?", (username,))
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard'))
        else:
            # Failed login: increment attempts, lock if threshold reached
            if attempt is None:
                c.execute("INSERT INTO login_attempts (username, failed_count, lock_until) VALUES (?, ?, ?)", (username, 1, None))
            else:
                failed = (attempt[0] or 0) + 1
                lock_until = attempt[1]
                if failed >= 5:
                    lock_until = now_ts + 5 * 60
                    failed = 0
                c.execute("UPDATE login_attempts SET failed_count=?, lock_until=? WHERE username=?", (failed, lock_until, username))
            conn.commit()
            conn.close()
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('inventory.db', timeout=10)
    c = conn.cursor()
    c.execute('PRAGMA busy_timeout=5000')
    c.execute("SELECT * FROM inventory")
    items = c.fetchall()
    conn.close()
    
    return render_template('dashboard.html', items=items)

@app.route('/inventory')
def inventory():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('inventory.db', timeout=10)
    c = conn.cursor()
    c.execute('PRAGMA busy_timeout=5000')
    c.execute("SELECT * FROM inventory")
    items = c.fetchall()
    conn.close()
    
    return render_template('inventory.html', items=items)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            quantity = int(request.form.get('quantity', 0))
            min_level = int(request.form.get('min_level', 0))
            unit = request.form.get('unit', '').strip()
            category_id = int(request.form.get('category_id', 1))
            
            # Validation
            if not name:
                flash('Item name is required')
                return redirect(url_for('add_item'))
            
            if quantity < 0:
                flash('Quantity cannot be negative')
                return redirect(url_for('add_item'))
            
            if min_level < 0:
                flash('Minimum level cannot be negative')
                return redirect(url_for('add_item'))
            
            if not unit:
                flash('Unit is required')
                return redirect(url_for('add_item'))
            
            conn = sqlite3.connect('inventory.db', timeout=10)
            c = conn.cursor()
            c.execute('PRAGMA busy_timeout=5000')
            c.execute("INSERT INTO inventory (name, quantity, min_level, unit, category_id) VALUES (?, ?, ?, ?, ?)", 
                     (name, quantity, min_level, unit, category_id))
            
            # Log transaction
            item_id = c.lastrowid
            c.execute("INSERT INTO transactions (item_id, transaction_type, quantity, reason, user_id) VALUES (?, ?, ?, ?, ?)",
                     (item_id, 'ADD', quantity, 'Initial stock', session['user_id']))
            
            conn.commit()
            conn.close()
            
            flash('Item added successfully!')
            return redirect(url_for('add_item'))
            
        except ValueError as e:
            flash('Please enter valid numbers for quantity and minimum level')
            return redirect(url_for('add_item'))
        except Exception as e:
            flash('An error occurred while adding the item')
            return redirect(url_for('add_item'))
    
    # Get categories for dropdown
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM categories ORDER BY name")
    categories = c.fetchall()
    conn.close()
    
    return render_template('add_item.html', categories=categories)

@app.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        min_level = int(request.form['min_level'])
        unit = request.form['unit']
        category_id = request.form.get('category_id', 1)
        
        # Get old quantity for transaction logging
        c.execute("SELECT quantity FROM inventory WHERE id=?", (item_id,))
        old_quantity = c.fetchone()[0]
        
        c.execute("UPDATE inventory SET name=?, quantity=?, min_level=?, unit=?, category_id=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", 
                 (name, quantity, min_level, unit, category_id, item_id))
        
        # Log quantity change if different
        if quantity != old_quantity:
            change_type = 'INCREASE' if quantity > old_quantity else 'DECREASE'
            change_amount = abs(quantity - old_quantity)
            c.execute("INSERT INTO transactions (item_id, transaction_type, quantity, reason, user_id) VALUES (?, ?, ?, ?, ?)",
                     (item_id, change_type, change_amount, 'Manual adjustment', session['user_id']))
        
        conn.commit()
        conn.close()
        
        flash('Item updated successfully!')
        return redirect(url_for('dashboard'))
    
    c.execute("SELECT * FROM inventory WHERE id=?", (item_id,))
    item = c.fetchone()
    
    # Get categories for dropdown
    c.execute("SELECT * FROM categories ORDER BY name")
    categories = c.fetchall()
    
    conn.close()
    
    if item is None:
        flash('Item not found')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_item.html', item=item, categories=categories)

@app.route('/decrement_item/<int:item_id>', methods=['POST'])
def decrement_item(item_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    try:
        amount = int(request.form.get('decrement', '1'))
    except ValueError:
        amount = 0

    if amount <= 0:
        flash('Enter a valid amount to deduct')
        return redirect(url_for('edit_item', item_id=item_id))

    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    # Fetch current quantity
    c.execute("SELECT quantity FROM inventory WHERE id=?", (item_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        flash('Item not found')
        return redirect(url_for('inventory'))

    current_qty = int(row[0])
    new_qty = max(current_qty - amount, 0)
    c.execute("UPDATE inventory SET quantity=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", (new_qty, item_id))
    
    # Log transaction
    c.execute("INSERT INTO transactions (item_id, transaction_type, quantity, reason, user_id) VALUES (?, ?, ?, ?, ?)",
             (item_id, 'DECREASE', amount, 'Stock usage', session['user_id']))
    
    conn.commit()
    conn.close()

    flash(f'Quantity reduced by {amount}. New quantity: {new_qty}')
    return redirect(url_for('edit_item', item_id=item_id))

@app.route('/delete_item/<int:item_id>')
def delete_item(item_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("DELETE FROM inventory WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    
    flash('Item deleted successfully!')
    return redirect(url_for('inventory'))

@app.route('/api/low_stock')
def api_low_stock():
    if 'logged_in' not in session:
        return {'error': 'Not authenticated'}, 401
    
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory WHERE quantity <= min_level")
    low_stock_items = c.fetchall()
    conn.close()
    
    return {'items': low_stock_items}

@app.route('/api/export')
def api_export():
    if 'logged_in' not in session:
        return {'error': 'Not authenticated'}, 401
    
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    items = c.fetchall()
    conn.close()
    
    csv_data = "Item Name,Quantity,Min Level,Unit,Status\n"
    for item in items:
        status = "Low Stock" if item[2] <= item[3] else "Good"
        csv_data += f'"{item[1]}",{item[2]},{item[3]},"{item[4]}","{status}"\n'
    
    return csv_data, 200, {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=inventory_report.csv'}

# Analytics route removed per request; charts moved to dashboard

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not password:
            flash('Username and password are required')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match')
            return render_template('register.html')

        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        try:
            hashed_password = hash_password(password)
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            flash('Username already exists')
            return render_template('register.html')
        conn.close()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/categories')
def categories():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM categories ORDER BY name")
    categories = c.fetchall()
    conn.close()
    
    return render_template('categories.html', categories=categories)

@app.route('/add_category', methods=['POST'])
def add_category():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    
    if not name:
        flash('Category name is required')
        return redirect(url_for('categories'))
    
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO categories (name, description) VALUES (?, ?)", (name, description))
        conn.commit()
        flash('Category added successfully!')
    except sqlite3.IntegrityError:
        flash('Category name already exists')
    conn.close()
    
    return redirect(url_for('categories'))

@app.route('/delete_category/<int:category_id>')
def delete_category(category_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    # Check if category is in use
    c.execute("SELECT COUNT(*) FROM inventory WHERE category_id=?", (category_id,))
    if c.fetchone()[0] > 0:
        flash('Cannot delete category that is in use')
        conn.close()
        return redirect(url_for('categories'))
    
    c.execute("DELETE FROM categories WHERE id=?", (category_id,))
    conn.commit()
    conn.close()
    
    flash('Category deleted successfully!')
    return redirect(url_for('categories'))

@app.route('/transactions')
def transactions():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''SELECT t.*, i.name as item_name, u.username 
                 FROM transactions t 
                 JOIN inventory i ON t.item_id = i.id 
                 JOIN users u ON t.user_id = u.id 
                 ORDER BY t.created_at DESC''')
    transactions = c.fetchall()
    conn.close()
    
    return render_template('transactions.html', transactions=transactions)

@app.route('/reports')
def reports():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    # Get various report data
    c.execute("SELECT COUNT(*) FROM inventory")
    total_items = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM inventory WHERE quantity <= min_level")
    low_stock_count = c.fetchone()[0]
    
    c.execute("SELECT name, quantity FROM inventory ORDER BY quantity DESC LIMIT 10")
    top_items = c.fetchall()
    
    c.execute('''SELECT c.name, COUNT(i.id) as item_count 
                 FROM categories c 
                 LEFT JOIN inventory i ON c.id = i.category_id 
                 GROUP BY c.id, c.name''')
    category_stats = c.fetchall()
    
    conn.close()
    
    return render_template('reports.html', 
                         total_items=total_items, 
                         low_stock_count=low_stock_count,
                         top_items=top_items,
                         category_stats=category_stats)

@app.route('/analytics')
def analytics():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT id, name, quantity, min_level FROM inventory ORDER BY quantity DESC")
    items = c.fetchall()
    conn.close()
    
    low_stock_count = sum(1 for _id, _name, qty, min_lvl in items if qty <= min_lvl)
    well_stock_count = max(len(items) - low_stock_count, 0)

    top_items = items[:5]
    quantity_labels = [(_name or '')[:10] for _id, _name, _qty, _min in top_items]
    quantity_values = [int(_qty or 0) for _id, _name, _qty, _min in top_items]

    return render_template(
        'analytics.html',
        stock_counts={'well': well_stock_count, 'low': low_stock_count},
        quantity_labels=quantity_labels,
        quantity_values=quantity_values,
    )

@app.route('/adjust_stock')
def adjust_stock():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    return render_template('adjust_stock.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
