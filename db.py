import sqlite3 as db
from datetime import datetime
import hashlib
from contextlib import contextmanager

# Register datetime adapters and converters
db.register_adapter(datetime, lambda d: d.isoformat())
db.register_converter('DATETIME', lambda s: datetime.fromisoformat(s.decode('utf-8')))

@contextmanager
def db_connection():
    conn = None
    try:
        conn = db.connect('safety.db', detect_types=db.PARSE_DECLTYPES)
        conn.row_factory = db.Row  # Return rows as dictionaries
        yield conn
    except db.DatabaseError as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def create_tables():
    try:
        with db_connection() as conn:
            cursor = conn.cursor()

            # Users Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    is_admin BOOLEAN DEFAULT FALSE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Activities Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    activity TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
                )
            ''')

            # Tips Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Tips (
                    tip_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON Users(username)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_activities_user_id ON Activities(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_tips_title ON Tips(title)')

            conn.commit()
    except db.DatabaseError as e:
        print(f"Error creating tables: {e}")
        raise

def default_admin():
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            hashed_password = hashlib.sha256('#sbm@86140764'.encode()).hexdigest()
            cursor.execute('''
                INSERT OR IGNORE INTO Users 
                (username, password, is_admin) 
                VALUES (?, ?, ?)
            ''', ('ADMIN', hashed_password, True))
            conn.commit()
    except db.DatabaseError as e:
        print(f"Error creating admin user: {e}")

def authenticate_user(username, password):
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, username, password, is_admin 
                FROM Users 
                WHERE username = ?
            ''', (username,))
            user = cursor.fetchone()
            
            if user and hashlib.sha256(password.encode()).hexdigest() == user['password']:
                return dict(user)  # Convert to regular dictionary
            return None
    except db.DatabaseError as e:
        print(f"Authentication error: {e}")
        return None

def add_tip(title, content):
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Tips (title, content) 
                VALUES (?, ?)
            ''', (title, content))
            conn.commit()
            return True
    except db.DatabaseError as e:
        print(f"Error adding tip: {e}")
        return False

def update_tip(tip_id, title, content):
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Tips 
                SET title = ?, content = ? 
                WHERE tip_id = ?
            ''', (title, content, tip_id))
            conn.commit()
            return cursor.rowcount > 0
    except db.DatabaseError as e:
        print(f"Error updating tip: {e}")
        return False

def remove_tip(tip_id):
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Tips WHERE tip_id = ?', (tip_id,))
            conn.commit()
            return cursor.rowcount > 0
    except db.DatabaseError as e:
        print(f"Error deleting tip: {e}")
        return False

def get_tips(search_query=None):
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            if search_query:
                cursor.execute('''
                    SELECT tip_id, title, content, created_at 
                    FROM Tips 
                    WHERE title LIKE ?
                    ORDER BY created_at DESC
                ''', (f'%{search_query}%',))
            else:
                cursor.execute('''
                    SELECT tip_id, title, content, created_at 
                    FROM Tips 
                    ORDER BY created_at DESC
                ''')
            
            # Convert to list of dictionaries with consistent keys
            columns = [column[0] for column in cursor.description]
            tips = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return tips
    except db.DatabaseError as e:
        print(f"Error fetching tips: {e}")
        return []

def add_user(username, password, is_admin=False):
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute('''
                INSERT INTO Users 
                (username, password, is_admin) 
                VALUES (?, ?, ?)
            ''', (username, hashed_password, is_admin))
            conn.commit()
            return True
    except db.IntegrityError:
        print(f'Username {username} already exists')
        return False
    except db.DatabaseError as e:
        print(f"Error adding user: {e}")
        return False

def update_user(user_id, new_username=None, new_password=None):
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if new_username:
                updates.append("username = ?")
                params.append(new_username)
            
            if new_password:
                hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                updates.append("password = ?")
                params.append(hashed_password)
            
            if not updates:
                return False
                
            params.append(user_id)
            
            query = f"UPDATE Users SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
            
            return cursor.rowcount > 0
    except db.DatabaseError as e:
        print(f"Error updating user: {e}")
        return False

def remove_user(user_id):
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Users WHERE id = ?', (user_id,))
            conn.commit()
            return cursor.rowcount > 0
    except db.DatabaseError as e:
        print(f"Error deleting user: {e}")
        return False

def view_users():
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, username, is_admin, created_at 
                FROM Users 
                ORDER BY created_at DESC
            ''')
            
            columns = [column[0] for column in cursor.description]
            users = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return users
    except db.DatabaseError as e:
        print(f"Error fetching users: {e}")
        return []

def log_activity(user_id, activity):
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Activities (user_id, activity) 
                VALUES (?, ?)
            ''', (user_id, activity))
            conn.commit()
            return True
    except db.DatabaseError as e:
        print(f"Error logging activity: {e}")
        return False

def view_activities():
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    a.id, 
                    u.username as user_id, 
                    a.activity, 
                    a.timestamp 
                FROM Activities a
                JOIN Users u ON a.user_id = u.id
                ORDER BY a.timestamp DESC
            ''')
            
            columns = [column[0] for column in cursor.description]
            activities = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return activities
    except db.DatabaseError as e:
        print(f"Error fetching activities: {e}")
        return []

# Initialize database
create_tables()
default_admin()
print('db connected')
