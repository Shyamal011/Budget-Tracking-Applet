#define functions preferably within user_account class because it will be easier to access the path names for different files
"""Try to complete the entire program by 4 o'clock p.m.(1600), Sunday, 18.05.2025. I will create report and send it back to you for revision
   by Sunday midnight. Do let me know if there are any mistakes from my end and correct them by yourself if you can. 
   Thank you,
   Yours faithfully,
   Shyamal"""
import os

user_names = {}
user_list = {}
user_db = "user_accounts.txt"

def load_user_data():
    if os.path.exists(user_db):
        with open(user_db, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    username, filepath = parts
                    user_names[username] = filepath
                    user_list[username] = user_account(username, init_files=False)

def save_user_data():
    with open(user_db, "w") as f:
        for username, filepath in user_names.items():
            f.write(f"{username},{filepath}\n")

class user_account:
    def __init__(self, username, init_files=True):
        self.username = username
        self.r_a = 'n'
        x = os.getcwd()
        self.acc_file_path = os.path.join(x, f"{self.username}_acc_details.txt")
        self.trnsctn_file_path = os.path.join(x, f"{self.username}_trnsctn_history.txt")
        self.budget_file_path = os.path.join(x, f"{self.username}_budget.txt")
        self.report_file_path = os.path.join(x, f"{self.username}_report.xlsx")

        if init_files:
            self.file = open(self.acc_file_path, "w+")
            self.trnsctn = open(self.trnsctn_file_path, "w+")
            self.report = open(self.report_file_path, "w+")
        else:
            self.file = open(self.acc_file_path, "r+")
            self.trnsctn = open(self.trnsctn_file_path, "a+")
            self.report = open(self.report_file_path, "a+")

    def create_account(self): 
        password = str(input("Enter password containing alphanumerical characters: "))
        while not password.isalnum():
            print("Password contains special characters!")
            password = str(input("Enter password containing alphanumerical characters: "))
        name = str(input("Enter your full name: "))
        bank_acc_no = str(int(input("Enter bank account number: ")))
        details = f"Username: {self.username}\nPassword: {password}\nName: {name}\nBank Account Number: {bank_acc_no}"
        self.file.write(details)
        print("Account has been created successfully!\nCongratulations!")
        self.report.close()
        os.remove(self.report_file_path)

    def display_user_details(self):
        self.file.seek(0)  # Go to the beginning of the file
        print("\n--- USER ACCOUNT DETAILS ---")
        for line in self.file:
            print(line.strip())
        print("----------------------------\n")
        

    def change_user_details(self):
        self.file.seek(0)
        lines = self.file.readlines()

        details = {}
        for line in lines:
            if ':' in line:
                key, value = line.strip().split(':', 1)
                details[key.strip()] = value.strip()

        print("\nWhich detail would you like to change?")
        print("1. Password")
        print("2. Name")
        print("3. Bank Account Number")
        choice = input("Enter choice: ")

        if choice == '1':
            new_password = input("Enter new alphanumerical password: ")
            while not new_password.isalnum():
                print("Invalid password! Use only letters and numbers.")
                new_password = input("Enter new alphanumerical password: ")
            details["Password"] = new_password

        elif choice == '2':
            new_name = input("Enter new full name: ")
            details["Name"] = new_name

        elif choice == '3':
            new_bank_acc_no = str(int(input("Enter new bank account number: ")))
            details["Bank Account Number"] = new_bank_acc_no

        else:
            print("Invalid choice!")
            return

        # Rewrite updated details
        self.file.seek(0)
        self.file.truncate(0)  # Clear the file
        for key in ["Username", "Password", "Name", "Bank Account Number"]:
            self.file.write(f"{key}: {details[key]}\n")

        self.file.flush()
        print("\nUser details updated successfully!\n")

    def remove_user(self):
        confirm = input("Are you sure you want to delete your account? (y/n): ").lower()
        if confirm != 'y':
            print("Account deletion canceled.")
            return

        # Close open files first
        self.close()

        # Delete account-related files
        try:
            os.remove(self.acc_file_path)
            os.remove(self.trnsctn_file_path)
            if os.path.exists(self.report_file_path):
                os.remove(self.report_file_path)
        except Exception as e:
            print(f"Error deleting files: {e}")
            return

        # Remove from global dictionaries
        if self.username in user_names:
            del user_names[self.username]
        if self.username in user_list:
            del user_list[self.username]

        # Save the updated user list
        save_user_data()

        print("Your account and all associated data have been permanently deleted.\nThank you for using our applet.")
        end()

    def track_expenses(self):
        self.trnsctn.seek(0)
        print("\n--- Transaction History ---")
        for line in self.trnsctn:
            print(line.strip())
        print("----------------------------\n")
        menu(self)

    def set_budget(self):
        try:
            goal = float(input("Set your monthly budget limit: "))
            with open(self.budget_file_path, "w") as f:
                f.write(str(goal))
            print(f"Monthly budget set to: {goal}")
        except ValueError:
            print("Invalid input. Please enter a number.")
        if not os.path.exists(self.budget_file_path):
            print("No budget set. Please set your monthly budget first.")
            return
        menu(self)


    def compare_budget(self):
        try:
            with open(self.budget_file_path, "r") as f:
                budget = float(f.read().strip())
        except ValueError:
            print("Something went wrong. Please reset your budget.")
            return
        self.trnsctn.seek(0)
        total_expense = 0.0
        for line in self.trnsctn:
            parts = line.strip().split(",")
            if len(parts) >= 4:
                try:
                    amount = float(parts[3].strip())
                    if amount < 0:
                        total_expense += abs(amount)
                except ValueError:
                    continue
        print(f"\nYour set monthly budget: {budget}")
        print(f"Total expenses so far: {total_expense}")
        if total_expense > budget:
            print("Warning: You have exceeded your budget!")
        else:
            print("Good job! You are within your budget.")
        menu(self)

        def close(self):
            self.file.close()
            self.trnsctn.close()
            self.report.close()

def menu(r):
    print("MENU")
    print("1. Add expense")
    print("2. Expenses history")
    print("3. Add/Change budget goal")
    print("4. Check budget status")
    print("5. Analysis of user expenses")
    print("6. Account settings")
    print("7. Exit")
    i = str(input("Enter choice: "))
    if i == '1':
        t_type = input("Enter type (income / expense): ").strip().lower()
        if t_type not in ['income', 'expense']:
            print("Invalid type! Must be 'income' or 'expense'.")
            return

        category = input("Enter category (e.g., salary, food, bills): ")
        amount = input("Enter amount: ")
        try:
            amount = float(amount)
        except ValueError:
            print("Amount must be a number.")
            return

        # Make expenses negative
        if t_type == 'expense':
             amount = -abs(amount)
        else:
            amount = abs(amount)

        description = input("Enter short description (optional): ")
    
        import datetime
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        expense_entry = f"{date}, {t_type}, {category}, {amount}, {description}\n"
        r.trnsctn.write(expense_entry)
        r.trnsctn.flush()

        print("Transaction recorded successfully!")
        menu(self)
    elif i == '2':
        r.track_expenses()
    elif i == '3':
        r.set_budget()
    elif i == '4':
        r.compare_budget()
    elif i == '5':
        #Shashwat-->Report and analysis
        pass
    elif i == '6':
        print("1. Display user details")
        print("2. Change user details")
        print("3. Remove user details")
        print("4. Go back to menu")
        j = input("Enter choice: ")
        if j == '1':
            r.display_user_details()
        elif j == '2':
            r.change_user_details()
        elif j == '3':
            r.remove_user()
        elif j == '4':
            menu(self)
        else:
            end()
        menu(self)
    elif i == '7':
        end()
    else:
        print("Invalid choice!")
        menu(self)

def end():
    print("Thank you for using the applet!\nVisit us again!")
    exit()

def start():       
    load_user_data()
    print("1. Login")
    print("2. Create account")
    print("3. Exit")
    ch = input("Enter your choice:")
    if ch == '1':
        user_name = str(input("Please enter your username: "))
        if user_name in user_names:
            g_password = str(input("Please enter your password: "))
            with open(user_names[user_name], "r") as f:
                for line in f:
                    if line.startswith("Password: "):
                        password = line.strip().split(":")[1].strip()
                        if g_password == password:
                            print("Login successful!")
                            a = user_list[user_name]
                            menu(a)
                            return
                        else:
                            print("Password incorrect!")
                            return
        else:
            print("Username not found!\n")
            start()
    elif ch == '2':
        user_name = str(input("Please enter a username: "))
        r = user_account(user_name)
        r.create_account()
        user_names[user_name] = r.acc_file_path
        user_list[user_name] = r
        save_user_data()
    else:
        end()

print("Welcome to the budget-tracking applet!\n")
start()
