import sqlitecloud
from flask import current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

def get_db():
    if 'db' not in g:
        conn_str = current_app.config['SQLITECLOUD_CONNECTION_STRING']
        g.db = sqlitecloud.connect(conn_str)
        g.db.execute('PRAGMA foreign_keys = ON;')
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Create tables if they don't exist"""
    db = get_db()
    
    # Users table
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Products table
    db.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Carts table (for users and guests)
    db.execute('''
        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            session_id TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Cart items
    db.execute('''
        CREATE TABLE IF NOT EXISTS cart_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cart_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )
    ''')
    
    # Orders
    db.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            razorpay_order_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Order items
    db.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    db.commit()

class User(UserMixin):
    def __init__(self, id, email, is_admin=False, created_at=None):
        self.id = id
        self.email = email
        self.is_admin = is_admin
        self.created_at = created_at

    @staticmethod
    def get(user_id):
        db = get_db()
        cursor = db.execute('SELECT id, email, is_admin, created_at FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        if row:
            return User(row[0], row[1], bool(row[2]), row[3])
        return None

    @staticmethod
    def get_by_email(email):
        db = get_db()
        cursor = db.execute('SELECT id, email, is_admin FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        if row:
            return User(row[0], row[1], bool(row[2]))
        return None

    @staticmethod
    def create(email, password, is_admin=False):
        db = get_db()
        password_hash = generate_password_hash(password)
        try:
            cursor = db.execute(
                'INSERT INTO users (email, password_hash, is_admin) VALUES (?, ?, ?)',
                (email, password_hash, 1 if is_admin else 0)
            )
            db.commit()
            return cursor.lastrowid
        except sqlitecloud.IntegrityError:
            return None

    def check_password(self, password):
        db = get_db()
        cursor = db.execute('SELECT password_hash FROM users WHERE id = ?', (self.id,))
        row = cursor.fetchone()
        if row:
            return check_password_hash(row[0], password)
        return False

class Product:
    @staticmethod
    def create(name, description, price, stock, image_url):
        db = get_db()
        cursor = db.execute(
            'INSERT INTO products (name, description, price, stock, image_url) VALUES (?, ?, ?, ?, ?)',
            (name, description, price, stock, image_url)
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.execute('SELECT * FROM products ORDER BY created_at DESC')
        rows = cursor.fetchall()
        return [dict(zip([col[0] for col in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_id(product_id):
        db = get_db()
        cursor = db.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        row = cursor.fetchone()
        if row:
            return dict(zip([col[0] for col in cursor.description], row))
        return None

    @staticmethod
    def update_stock(product_id, quantity):
        db = get_db()
        db.execute('UPDATE products SET stock = stock - ? WHERE id = ? AND stock >= ?', 
                  (quantity, product_id, quantity))
        db.commit()
        return db.total_changes > 0

    @staticmethod
    def update(product_id, name, description, price, stock, image_url):
        db = get_db()
        db.execute('''
            UPDATE products
            SET name = ?, description = ?, price = ?, stock = ?, image_url = ?
            WHERE id = ?
        ''', (name, description, price, stock, image_url, product_id))
        db.commit()
        return db.total_changes > 0

    @staticmethod
    def delete(product_id):
        db = get_db()
        db.execute('DELETE FROM products WHERE id = ?', (product_id,))
        db.commit()
        return db.total_changes > 0

class Cart:
    @staticmethod
    def get_or_create_cart(user_id=None, session_id=None):
        db = get_db()
        if user_id:
            cursor = db.execute('SELECT id FROM carts WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            if row:
                cart_id = row[0]
            else:
                cursor = db.execute('INSERT INTO carts (user_id) VALUES (?)', (user_id,))
                cart_id = cursor.lastrowid
                db.commit()
            return cart_id
        elif session_id:
            cursor = db.execute('SELECT id FROM carts WHERE session_id = ?', (session_id,))
            row = cursor.fetchone()
            if row:
                cart_id = row[0]
            else:
                cursor = db.execute('INSERT INTO carts (session_id) VALUES (?)', (session_id,))
                cart_id = cursor.lastrowid
                db.commit()
            return cart_id
        return None

    @staticmethod
    def merge_carts(user_id, session_id):
        db = get_db()
        guest_cart = db.execute('SELECT id FROM carts WHERE session_id = ?', (session_id,)).fetchone()
        if not guest_cart:
            return
        guest_cart_id = guest_cart[0]
        user_cart_id = Cart.get_or_create_cart(user_id=user_id)
        
        guest_items = db.execute('SELECT product_id, quantity FROM cart_items WHERE cart_id = ?', 
                                (guest_cart_id,)).fetchall()
        for product_id, qty in guest_items:
            existing = db.execute('SELECT id, quantity FROM cart_items WHERE cart_id = ? AND product_id = ?',
                                 (user_cart_id, product_id)).fetchone()
            if existing:
                db.execute('UPDATE cart_items SET quantity = quantity + ? WHERE id = ?', (qty, existing[0]))
            else:
                db.execute('INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (?, ?, ?)',
                          (user_cart_id, product_id, qty))
        db.execute('DELETE FROM carts WHERE id = ?', (guest_cart_id,))
        db.commit()

    @staticmethod
    def add_item(cart_id, product_id, quantity=1):
        db = get_db()
        product = Product.get_by_id(product_id)
        if not product or product['stock'] < quantity:
            return False
        
        existing = db.execute('SELECT id, quantity FROM cart_items WHERE cart_id = ? AND product_id = ?',
                            (cart_id, product_id)).fetchone()
        if existing:
            new_qty = existing[1] + quantity
            if product['stock'] < new_qty:
                return False
            db.execute('UPDATE cart_items SET quantity = ? WHERE id = ?', (new_qty, existing[0]))
        else:
            db.execute('INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (?, ?, ?)',
                      (cart_id, product_id, quantity))
        db.commit()
        return True

    @staticmethod
    def remove_item(cart_id, product_id):
        db = get_db()
        db.execute('DELETE FROM cart_items WHERE cart_id = ? AND product_id = ?', (cart_id, product_id))
        db.commit()

    @staticmethod
    def update_item_quantity(cart_id, product_id, quantity):
        if quantity <= 0:
            Cart.remove_item(cart_id, product_id)
            return True
        db = get_db()
        product = Product.get_by_id(product_id)
        if not product or product['stock'] < quantity:
            return False
        db.execute('UPDATE cart_items SET quantity = ? WHERE cart_id = ? AND product_id = ?',
                  (quantity, cart_id, product_id))
        db.commit()
        return True

    @staticmethod
    def get_cart_items(cart_id):
        db = get_db()
        cursor = db.execute('''
            SELECT ci.product_id, ci.quantity, p.name, p.price, p.image_url, p.stock
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.id
            WHERE ci.cart_id = ?
        ''', (cart_id,))
        rows = cursor.fetchall()
        items = []
        total = 0
        for row in rows:
            product_id, qty, name, price, image, stock = row
            subtotal = price * qty
            total += subtotal
            items.append({
                'product_id': product_id,
                'quantity': qty,
                'name': name,
                'price': price,
                'image_url': image,
                'stock': stock,
                'subtotal': subtotal
            })
        return items, total

class Order:
    @staticmethod
    def get_by_user(user_id):
        db = get_db()
        cursor = db.execute('''
            SELECT o.id, o.total_amount, o.status, o.razorpay_order_id, o.created_at,
                   oi.product_id, oi.quantity, oi.price, p.name as product_name
            FROM orders o
            LEFT JOIN order_items oi ON o.id = oi.order_id
            LEFT JOIN products p ON oi.product_id = p.id
            WHERE o.user_id = ?
            ORDER BY o.created_at DESC
        ''', (user_id,))
        rows = cursor.fetchall()
        orders = {}
        for row in rows:
            order_id = row[0]
            if order_id not in orders:
                orders[order_id] = {
                    'id': order_id,
                    'total_amount': row[1],
                    'status': row[2],
                    'razorpay_order_id': row[3],
                    'created_at': row[4],
                    'items': []
                }
            if row[5]:  # product_id exists
                orders[order_id]['items'].append({
                    'product_id': row[5],
                    'quantity': row[6],
                    'price': row[7],
                    'product_name': row[8]
                })
        return list(orders.values())