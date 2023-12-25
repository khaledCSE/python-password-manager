from password_manager import PasswordManager
from ui import UI
from db import DatabaseManager

if __name__ == "__main__":
    database = DatabaseManager()
    manager = PasswordManager(database)
    ui = UI(manager)
    
    ui.greet_user()
    ui.check_master_password()


