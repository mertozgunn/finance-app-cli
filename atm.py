from pymongo import MongoClient

class MongoDBManager:
    def __init__(self, connection_string, database_name):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.users_collection = self.db["users"]

    def find_user(self, username):
        return self.users_collection.find_one({"username": username}, {'_id': 0})  # Exclude _id field

    def insert_user(self, user_data):
        self.users_collection.insert_one(user_data)

class User:
    def __init__(self, username, name, surname, phone, email, password, primary=0, loan=0):
        self.username = username
        self.name = name
        self.surname = surname
        self.phone = phone
        self.email = email
        self.password = password
        self.primary = primary
        self.loan = loan

    def to_dict(self):
        return {
            "username": self.username,
            "name": self.name,
            "surname": self.surname,
            "phone": self.phone,
            "email": self.email,
            "password": self.password,
            "primary": self.primary,
            "loan": self.loan
        }

class FinanceApp:
    def __init__(self, mongodb_manager):
        self.mongodb_manager = mongodb_manager
        self.current_user = None

    def display_starting_menu(self):
        print("\n**********Starting Menu**********")
        print("\n1.Login\n2.Register\n3.Exit")
        while True:
            try:
                choice = int(input("\nPlease enter the number of the menu option you want to choose: "))
                if choice == 1:
                    self.login()
                    break
                elif choice == 2:
                    self.register()
                    break
                elif choice == 3:
                    self.exit()
                else:
                    print("Invalid input. Please enter a valid number.")
                    continue
            except ValueError:
                print("You must enter only the number of menu Item!")
                continue
            break

    def display_main_menu(self):
        print("\n\n**************Main Menu************")
        print(f"\nHello {self.current_user.username}, have a good day.")
        print("\n1.Account İnformation\n2.Deposit Money\n3.Withdraw Money\n4.Apply for Loan\n5.Log-out")
        while True:
            try:
                choice = int(input("\nPlease enter the number of the menu option you want to choose: "))
                if choice == 1:
                    self.account_information()
                    break
                elif choice == 2:
                    self.deposit_money()
                    break
                elif choice == 3:
                    self.withdraw_money()
                    break
                elif choice == 4:
                    self.apply_for_loan()
                    break
                elif choice == 5:
                    self.logout()
                    break
                else:
                    print("Invalid input. Please enter a valid number.")
                    continue
            except ValueError:
                print("You must enter only the number of menu item.")
                continue

    def login(self):
        print("\n\n**************LOGIN**************")
        print("Provide your credentials below.\n")
        while True:
            username = input("Please write your name: ")
            password = input("Please write your password: ")
            user_data = self.mongodb_manager.find_user(username)

            if user_data and user_data["password"] == password:
                self.current_user = User(**user_data)
                self.display_main_menu()
            else:
                print("\nThe username or password is WRONG!")

    def register(self):
        print("\n\n************REGISTER****************")
        print("\nPlease fill the personal information form.\n")
        new_user = {}
        username = ""
        name = input("Name: ")
        surname = input("Surname: ")
        phone = input("Phone Number: ")
        email = input("Email: ")

        while True:
            username = input("\nUsername: ")
            if not self.mongodb_manager.find_user(username):
                password = input("Password: ")
                password_again = input("Password (again): ")
                if password == password_again:
                    new_user = User(username, name, surname, phone, email, password)
                    self.mongodb_manager.insert_user(new_user.to_dict())
                else:
                    print("The password does not match! Please check again!")
                    continue
            else:
                print("The chosen username is already in use. Please select a different one.")

                continue
            break

        print("\n Saving your information")
        print("Returning to Starting Menu...")
        self.display_starting_menu()

    def account_information(self):
        print("\n\n**** Account Information ****")
        print(f"|Name/Surname: {self.current_user.name} {self.current_user.surname}" + (40 - len(self.current_user.name) - len(self.current_user.surname) - 13) * " " + "|")
        print("|" + 41 * " " + "|")
        print("|" + "Contact Information: " + (41 - 21) * " " + "|")
        print("|\t" + f"Phone Number: {self.current_user.phone}" + (41 - 14 - len(self.current_user.phone) - 7) * " " + "|")
        print("|\t" + f"Email: {self.current_user.email}" + (41 - 7 - len(self.current_user.email) - 7) * " " + "|")
        print("|" + 41 * " " + "|")
        print("|" + "Balance Information: " + (41 - 21) * " " + "|")
        print("|\t" + f"Primary Account Balance: {self.current_user.primary}$" + (40 - 25 - len(str(self.current_user.primary)) - 7) * " " + "|")
        print("|\t" + f"Loan Account Balance: {self.current_user.loan}$" + (40 - 22 - len(str(self.current_user.loan)) - 7) * " " + "|")
        print("|" + 41 * "_" + "|")

        print("Returning back to Main Menu...")
        self.display_main_menu()

    def deposit_money(self):
        print("\n*********** Deposit Money ************")
        print(f"\n Your current balance in Primary Account is {self.current_user.primary}$")
        while True:
            deposit_amount = int(input("\nPlease write the amount you would like to deposit: "))
            self.current_user.primary += deposit_amount
            print("\nDepositing your money")
            print(f"Your updated balance is {self.current_user.primary}$")
            while True:
                try:
                    again = input("\nWould you like to deposit again? (Y/N): ").upper()
                    if again == "Y" or again == "YES":
                        break
                    elif again == "N" or again == "NO":
                        print("\nReturning to Main Menu")
                        self.display_main_menu()
                        break
                    else:
                        print("Please write valid answer to question")
                        continue
                except ValueError:
                    print("Please enter a valid positive number to proceed with your operation.")
                    continue
                break
            break


