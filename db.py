import sqlite3
import clipboard
from cryptography.fernet import Fernet

class DatabaseManager:
  def __init__(self, db_name='passwords.db') -> None:
    conn = sqlite3.connect(db_name)
    self.conn = conn
    self.cursor = conn.cursor()
    self.create_table()

    
  def create_table(self):
    self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                category TEXT,
                encrypted_password TEXT NOT NULL
            );
        ''')
    self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS master_password (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT NOT NULL,
                encryption_key TEXT NOT NULL
            );
        ''')
    self.conn.commit()
    
  
  def create_master_password(self, password):
    """Creates a master password entry in the database."""
    
    # A secure encryption key for later
    key = (Fernet.generate_key()).decode('utf-8')
    fernet = Fernet(key)
    
    master_password = (fernet.encrypt(password.encode())).decode('utf-8')
    
    self.cursor.execute("INSERT INTO master_password (password, encryption_key) VALUES (?,?)", (master_password, key,))  # Note the comma
    self.conn.commit()

        
  def get_master_password(self):
      self.cursor.execute("SELECT password FROM master_password")
      master_password = ''.join(self.cursor.fetchone())
      return master_password
  
  def add_password(self, url, category, password):
        encrypted_password = self._encrypt_password(password)
        self.cursor.execute("INSERT INTO passwords (url, category, encrypted_password) VALUES (?, ?, ?)", (url, category, encrypted_password))
        self.conn.commit()
  
  def get_password(self, url):
      self.cursor.execute("SELECT encrypted_password FROM passwords WHERE url=?", (url,))
      encrypted_password = self.cursor.fetchone()
      if encrypted_password:
          return self._decrypt_password(encrypted_password[0])
      return None
    
  def _encrypt_password(self, password):
    self.cursor.execute("SELECT encryption_key FROM master_password")
    key = self.cursor.fetchone()
    fernet = Fernet(key)
    encrypted_password = (fernet.encrypt(password.encode())).decode('utf-8')    
    return encrypted_password

  def _decrypt_password(self, encrypted_password):
      self.cursor.execute("SELECT encryption_key FROM master_password")
      key = ''.join(self.cursor.fetchone())
       
      fernet = Fernet(key)
      plain_password = (fernet.decrypt(encrypted_password)).decode('utf-8')
      return plain_password

  def copy_password_to_clipboard(self, url):
      password = self.get_password(url)
      if password:
          clipboard.copy(password)

  def close(self):
      self.conn.close()