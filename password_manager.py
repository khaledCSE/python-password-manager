import string
import random
import clipboard
from db import DatabaseManager

class PasswordManager:
    def __init__(self, database: DatabaseManager):
        self.db_manager = database
        
    def generate_strong_password(self, length=16):
        """Generates a strong password with a specified length.

        Args:
            length (int, optional): The desired length of the password. Defaults to 16.

        Returns:
            str: The generated strong password.
        """
        # Character sets for password complexity
        uppercase_letters = string.ascii_uppercase
        lowercase_letters = string.ascii_lowercase
        digits = string.digits
        symbols = string.punctuation

        # Combine all character sets
        all_chars = list(uppercase_letters + lowercase_letters + digits + symbols)

        # Shuffle the characters randomly
        random.shuffle(all_chars)

        # Generate the password by selecting random characters
        password = "".join(random.sample(all_chars, length))
        return password

    def compare_passwords(self, plain_text, encrypted):
        decrypted = self.db_manager._decrypt_password(''.join(encrypted))
        return decrypted == plain_text
    
    def add_password(self, url, category, password):
        password_to_save = password
        if password.strip() == '':
            password_to_save = self.generate_strong_password()
            
        self.db_manager.add_password(url, category, password_to_save)

    def get_password(self, url):
        return self.db_manager._decrypt_password(self.db_manager.get_password(url))
    
    def list_passwords(self):
        return self.db_manager.get_password()
    
    def get_master_password(self):
        master_password = self.db_manager.get_master_password()
        return master_password
    
    def set_master_password(self, password):
        self.db_manager.create_master_password(password)

    def copy_password_to_clipboard(self, password):
        clipboard.copy(password)

    def delete_password(self, url):
        self.db_manager.delete_password(url)
    
    def close(self):
        self.db_manager.close()
