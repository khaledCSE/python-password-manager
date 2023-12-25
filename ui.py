from password_manager import PasswordManager
from termcolor import colored
import pyfiglet
from prettytable import PrettyTable

class UI:
  def __init__(self, password_manager: PasswordManager) -> None:
    self.password_manager = password_manager  
    self.master_password_max_retries = 5
    self.master_password_retries = 0

  def check_master_password(self):
    master_password_found = self.password_manager.get_master_password()
    
    if master_password_found:
      master_password = input('Enter master password: ')
      if (self.password_manager.compare_passwords(master_password, master_password_found)):
        self.display_menu()
      else:
        if self.master_password_retries >= self.master_password_max_retries:
          print('Cool Down! ❄️ Maximum retries reached! Comeback again!')
          exit(1)
        print(f'Incorrect master password! {self.master_password_max_retries - self.master_password_retries} tries left!')
        self.master_password_retries += 1
        self.check_master_password()
    else:
      master_password = input('Enter master password to save (Make sure it\'s rememberable): ')
      self.password_manager.set_master_password(master_password)
      
      self.display_menu()
      

  def greet_user(self):
      """Prints a cyberpunk-themed greeting in ASCII art."""

      # Generate ASCII art with pyfiglet
      ascii_art = pyfiglet.figlet_format("khaledCSE", font="slant")

      # Apply cyberpunk colors using termcolor
      colored_art = colored(ascii_art, color='green', attrs=["bold"])

      # Print the colored word art
      print(colored_art)

      # Display a cyberpunk-style welcome message
      print(colored("Welcome to the", color="cyan", attrs=["bold", "blink"]))
      print(colored("Password Manager!", color="yellow", attrs=["bold", "blink"]))

      # Add a cyberpunk-style border
      print("-" * 50)
      print(colored("▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓", color="magenta", attrs=["bold"]))
      print("-" * 50)
      
  def display_menu(self):
    print("\nMenu:")
    print("1. 🔑 Add Password")
    print("2. 🛡️  Update Password")
    print("3. 👀 Get Password")
    print("4. 📃 List Passwords")
    print("5. 💣 Reset Master Password")
    print("6. 🗑️  Delete a Password")
    print("7. ❌ Exit")

    choice = input("Enter your choice: ")
    
    if choice == '1':
      self.add_password()
    elif choice == '3':
      self.get_password()
    elif choice == '4':
      self.list_passwords()
    elif choice == '7':
      print('Thanks for using the password manager 👏👏👏')
      exit(1)

  def add_password(self):
      url = input("Enter URL: ")
      category = input("Enter Category (games/desktop/social): ")
      password = input("Enter Password (Leave blank to generate a strong password): ")
      self.password_manager.add_password(url, category, password)
      self.password_manager.copy_password_to_clipboard(url)
      print("Password added successfully!")
      
      self.display_menu()
      
  def get_password(self):
    url = input("Enter URL: ")
    password = self.password_manager.get_password(url)
    print(f'Password: {password}')
    
  def list_passwords(self):
    passwords = self.password_manager.list_passwords()
    table = PrettyTable()
    table.field_names = ['ID', 'Category', 'URL', 'Password']
    table.add_rows(passwords)
    print(table)
    
    self.display_menu()
    