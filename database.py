import sqlite3

class Database:
    def __init__(self, db_name='library.db'):
        self.connection = sqlite3.connect(db_name,check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                address TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                dob TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                available INTEGER DEFAULT 1,
                total_copies INTEGER NOT NULL,
                issued_copies INTEGER DEFAULT 0
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS issued_books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                issue_date TEXT NOT NULL,
                return_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (book_id) REFERENCES books(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                request_date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (book_id) REFERENCES books(id)
            )
        ''')

        self.connection.commit()

    def insert_user(self, username, password, address, phone, email, dob):
        self.cursor.execute('''
            INSERT INTO users (username, password, address, phone, email, dob)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, password, address, phone, email, dob))
        self.connection.commit()


    def insert_book(self, title, author, total_copies):
        self.cursor.execute('''
            INSERT INTO books (title, author, total_copies)
            VALUES (?, ?, ?)
        ''', (title, author, total_copies))
        self.connection.commit()
    
    def insert_admin(self, username, password):
        self.cursor.execute('''
            INSERT INTO admin (username, password)
            VALUES (?, ?)
        ''', (username, password))
        self.connection.commit()

    def fetch_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()
    
    def fetch_books(self):
        self.cursor.execute('SELECT * FROM books')
        return self.cursor.fetchall()
    
    def fetch_books_by_user(self, user_id):
        self.cursor.execute('''
            SELECT books.* FROM books
            JOIN issued_books ON books.id = issued_books.book_id
            WHERE issued_books.user_id = ?
        ''', (user_id,))
        return self.cursor.fetchall()   

    def get_admin_username(self):
        self.cursor.execute('SELECT username FROM admin LIMIT 1')
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_admin_password(self):
        self.cursor.execute('SELECT password FROM admin LIMIT 1')
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_user_username(self):
        self.cursor.execute('SELECT username FROM users LIMIT 1')
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_user_password(self):
        self.cursor.execute('SELECT password FROM users LIMIT 1')
        result = self.cursor.fetchone()
        return result[0] if result else None

    def close(self):
        self.connection.close()