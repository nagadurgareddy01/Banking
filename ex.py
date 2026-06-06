import os
import csv
import re
from datetime import datetime
from abc import ABC, abstractmethod

USERS_FILE = "users.csv"
TRANSACTIONS_FILE = "transactions.csv"

class Bank(ABC):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    @abstractmethod
    def deposit(self, amount):
        pass
        
    @abstractmethod
    def withdraw(self, amount):
        pass
    
class Transactions(Bank):
    def __init__(self, username, password, initial_balance=0.0):
        super().__init__(username, password)
        self.balance = initial_balance
        
    def log_transaction(self, trans_type, amount):
        file_exists = os.path.exists(TRANSACTIONS_FILE)
        with open(TRANSACTIONS_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Timeduration", "Username", "Type", "Amount", "Remaining Balance"])
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, self.username, trans_type, amount, self.balance])

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f'Your amount {amount} is deposited.')
            self.log_transaction("Deposit", amount)
            return True
        else:
            print('Please enter an amount above 0.')
            return False
            
    def withdraw(self, amount):
        if amount > self.balance:
            print('Please enter a lesser amount.')
            return False
        elif amount <= 0:
            print('Please enter more than 0.')
            return False
        else:
            self.balance -= amount
            print(f'You withdrew {amount} successfully. Balance is {self.balance}.')
            self.log_transaction("Withdrawal", amount)
            return True
            
    def checkbalance(self):
        print(f'The total balance is {self.balance}')

class Account:
    def __init__(self):
        self.accounts = {}
        self.load_data()  
        
    def load_data(self):
        """Reads user credentials and balances from users.csv"""
        if not os.path.exists(USERS_FILE):
            return
            
        with open(USERS_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader, None)             
            for row in reader:
                if row:
                    username, password, balance = row
                    
                    self.accounts[username] = Transactions(username, password, float(balance))
    def check_password(self, password):

        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,16}$"
        return re.match(password_pattern, password)
    

    def save_all_users(self):
        """Overwrites users.csv with the most up-to-date program state"""
        with open(USERS_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Password", "Current Balance"])
            for username, account in self.accounts.items():
                writer.writerow([account.username, account.password, account.balance])

    def signup(self):
        print('Welcome to sign up:')
        username = input('Please enter your username: ')
        if username in self.accounts:
            print(f'Username {username} already exists, please sign in.')
            return None

        password = input('Please enter your password: ')
        if not self.check_password(password):
            print('please enter valid password like \n conatins atleast one small alphabet and one large alphabet and one number \n minumum 8 characters and maximum of 16 characters')
            return 
        new_account = Transactions(username, password)
        self.accounts[username] = new_account
        
        
        self.save_all_users()
        print(f'Account created successfully. Welcome, {username}!')

    def signin(self):
        print('Welcome to sign in')
        username = input('Enter your username: ')
        if username not in self.accounts:
            print("Username doesn't exist, please sign up.")
            return None
            
        password = input('Enter your password: ')
        account = self.accounts[username]
        if account.password != password:
            print('Wrong password, please sign in again.')
            return None
            
        print(f'Login successful! {username}')
        return account
    

def AccountMenu(account, bank_system):
    while True:
        print(f"\n====== ACCOUNT MENU ({account.username}) ======")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. Logout")
        choice = input('Choose your option: ')

        if choice == '1':
            amount = float(input('Enter money for deposit: '))
            if account.deposit(amount):
                bank_system.save_all_users() 
            
        elif choice == '2':
            amount = float(input('Enter money for withdraw: '))
            if account.withdraw(amount):
                bank_system.save_all_users() 
            
        elif choice == '3':
            account.checkbalance()
            
        elif choice == '4':
            print('Logged out successfully. Bye!')
            break 
        else:
            print('Please select a proper choice.')

def main():
    print('* ' * 40)
    print('Welcome to Bank of Python')
    print('- ' * 40)
    my_bank = Account()

    while True:
        print("\n====== MAIN MENU ======")
        print("1. Sign Up  (New User)")
        print("2. Sign In  (Existing User)")
        print("3. Exit")
        print("=" * 40)

        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            my_bank.signup()
        elif choice == "2":
            account = my_bank.signin()
            if account:              
                AccountMenu(account, my_bank) 
        elif choice == "3":
            print("\nThank you for using Python Bank. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")


main()
