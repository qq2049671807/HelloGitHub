import sqlite3
from datetime import datetime
from crypto_utils import CryptoManager


class DatabaseManager:
    def __init__(self, db_file='passwords.db'):
        self.db_file = db_file
        self.crypto = CryptoManager()
        self._init_database()
    
    def _init_database(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_account(self, website, username, password, notes=''):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        encrypted_password = self.crypto.encrypt(password)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO accounts (website, username, password, notes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (website, username, encrypted_password, notes, timestamp, timestamp))
        
        conn.commit()
        account_id = cursor.lastrowid
        conn.close()
        return account_id
    
    def get_all_accounts(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT id, website, username, password, notes, created_at, updated_at FROM accounts')
        rows = cursor.fetchall()
        conn.close()
        
        accounts = []
        for row in rows:
            account = {
                'id': row[0],
                'website': row[1],
                'username': row[2],
                'password': self.crypto.decrypt(row[3]),
                'notes': row[4],
                'created_at': row[5],
                'updated_at': row[6]
            }
            accounts.append(account)
        
        return accounts
    
    def get_account_by_id(self, account_id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT id, website, username, password, notes, created_at, updated_at FROM accounts WHERE id = ?', (account_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'website': row[1],
                'username': row[2],
                'password': self.crypto.decrypt(row[3]),
                'notes': row[4],
                'created_at': row[5],
                'updated_at': row[6]
            }
        return None
    
    def update_account(self, account_id, website, username, password, notes=''):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        encrypted_password = self.crypto.encrypt(password)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            UPDATE accounts
            SET website = ?, username = ?, password = ?, notes = ?, updated_at = ?
            WHERE id = ?
        ''', (website, username, encrypted_password, notes, timestamp, account_id))
        
        conn.commit()
        conn.close()
    
    def delete_account(self, account_id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM accounts WHERE id = ?', (account_id,))
        conn.commit()
        conn.close()
    
    def search_accounts(self, keyword):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, website, username, password, notes, created_at, updated_at
            FROM accounts
            WHERE website LIKE ? OR username LIKE ?
        ''', (f'%{keyword}%', f'%{keyword}%'))
        rows = cursor.fetchall()
        conn.close()
        
        accounts = []
        for row in rows:
            account = {
                'id': row[0],
                'website': row[1],
                'username': row[2],
                'password': self.crypto.decrypt(row[3]),
                'notes': row[4],
                'created_at': row[5],
                'updated_at': row[6]
            }
            accounts.append(account)
        
        return accounts
