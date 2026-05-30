from abc import ABC , abstractmethod
import os
import csv 
import datetime

user_data='user.csv'
Transction_data='transaction.csv'

class Bank(ABC):
    def __init__(self,username,password):
        self.username = username
        self.password = password
        
    @abstractmethod
    def deposit(self,amount):
        pass
    @abstractmethod
    def withdraw(self,amount):
        pass
    
class Transactions(Bank):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.__balance = 0
    def get_balance(self):
        return self.__balance
    def transaction_data(self,trans_type,amount):
        file_exists=os.path.exists(Transction_data)
        with open(Transction_data,'a') as f:
            writer=csv.writer(f)
            if not file_exists:
                writer.writerow(['date&time','username','Transaction_type','amount','Balance'])
            date_time=datetime.datetime.now()
            writer.writerow([date_time,self.username,trans_type,amount,self.__balance])
    def deposit(self,amount):
        if amount > 0 :
            self.__balance += amount
            self.transaction_data('Deposit',amount)
            print(f'your amount {amount} is deposited ')
        else:
            print('please enter amount above 0')
    def withdraw(self, amount):
        if amount >= self.__balance:
            print('please enter lesser amount')
        elif amount <=0:
            print('please enter more than 0')
        else:
            self.__balance -= amount
            print(f'you withdraw {amount} success and balance is {self.__balance}')
            self.transaction_data('Withdraw',self.__balance)
    def checkbalance(self):
        print(f'the total balance is {self.__balance}')

class Account():
    
    def __init__(self):
        self.accounts={}
    def log_login(self,username,password,login_type):
        file_exists=os.path.exists(user_data)
        with open(user_data,'a') as f:
            writer=csv.writer(f)
            if not file_exists:
                writer.writerow(['datetime','username','password','login_type'])
            date_time=datetime.datetime.now()
            writer.writerow([date_time,username,password,login_type])


    def signup(self):
        print('welcome to sign up :')
        username = input('please enter your user name : ')
        if username in self.accounts :
            print(f'username {username} already exists please sign in ')
            return None

        password = input('please enter your password : ')
        new_account = Transactions(username,password)
        self.accounts[username]=new_account
        
        self.log_login(username,password,'sign_up')
      
        print(f'Account created successfully welcome {username}')

    def signin(self):
        print('welcome to sign in')
        username = input('enter your username : ')
        if username not in self.accounts :
            print('username doesn\'t exits please sign up')
            return None
        password = input('enter your password : ')
        account = self.accounts[username]
        if account.password != password:
            print('wrong password please sign in again ')
            return None
        print(f'login successfull {username}')
        self.log_login(username,password,'sign_in')
        return account
    

def AccountMenu(account):
    while True:
        print(f"\n====== ACCOUNT MENU ({account.username}) ======")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. Logout")
        choice = input('choose your option ')

        if choice == '1':
            try :
                amount = float(input('enter money for deposit : '))
                account.deposit(amount)
            except ValueError:
                print('enter proper amount')
            
        elif choice == '2':
            try:
                amount = float(input('enter money for withdraw : '))
                account.withdraw(amount)
            except ValueError:
                print('enter proper value')
        elif choice == '3':
            account.checkbalance()
        elif choice == '4':
            print('logout successfully , bye')
            break 
        else :
            print('please select proper choice')

def main():
    print('* '*40)
    print('welcome to bank of python ')
    print('- '*40)
    my_bank=Account()

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
                AccountMenu(account) 

        elif choice == "3":
            print("\n Thank you for using Python Bank. Goodbye!")
            break

        else:
            print("Invalid choice! Please enter 1, 2, or 3.")

            

main()

        

            


    






        