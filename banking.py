import csv
from colorama import Style, Back
from rich.console import Console
from rich.progress import track
import time

console = Console()
bank_Data = "bank.csv"

# ----------------Csv----------------class1


class Csv:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_accounts(self):
        accounts = []
        try:
            with open(self.file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    checking = None if row['checking'] == "None" else int(
                        row['checking'])
                    savings = None if row['savings'] == "None" else int(
                        row['savings'])
                    overdrafts = int(row.get('overdrafts', 0))
                    active = row.get('active', "True") == "True"
                    account = Customer(
                        id=int(row['id']),
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        password=row['password'],
                        checking=checking,
                        savings=savings,
                        overdrafts=overdrafts,
                        active=active
                    )
                    accounts.append(account)
        except FileNotFoundError:
            pass
        return accounts

    def save_all(self, accounts):
        with open(self.file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                                    'id', 'first_name', 'last_name', 'password', 'checking', 'savings', 'overdrafts', 'active'])
            writer.writeheader()
            for acc in accounts:
                writer.writerow({
                    'id': acc.id,
                    'first_name': acc.first_name,
                    'last_name': acc.last_name,
                    'password': acc.password,
                    'checking': acc.checking if acc.checking is not None else "None",
                    'savings': acc.savings if acc.savings is not None else "None",
                    'overdrafts': acc.overdrafts,
                    'active': acc.active
                })

# ----------------Customer----------------class2


class Customer:
    def __init__(self, id, first_name, last_name, password, checking=None, savings=None, overdrafts=0, active=True):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.checking = checking
        self.savings = savings
        self.overdrafts = overdrafts
        self.active = active
        self.transactions = []

# ----------------Transaction---------------- class3


class Transaction:
    def __init__(self, type, amount, account_from=None, account_to=None):
        self.type = type
        self.amount = amount
        self.account_from = account_from
        self.account_to = account_to

# ----------------Bank---------------- class4


class Bank:
    def __init__(self, csv_handler):
        self.csv_handler = csv_handler
        self.accounts = csv_handler.load_accounts()
        self.curr_user = None

    def find_id(self, account_id):
        for acc in self.accounts:
            if acc.id == account_id:
                return acc
        return None

    def sign_in(self):
        while True:
            try:
                account_id = int(console.input(
                    "[bold]Please enter your [green]ID number [/green]to Log In: [/bold]"))
            except ValueError:
                console.print(
                    "[bold red]Please enter a numeric ID.[/bold red]")
                continue

            password = console.input(
                "[bold]Enter your [green]password[/green] : [/bold]")
            account = self.find_id(account_id)

            if account and account.password == password:
                if not account.active:
                    console.print(
                        "[red]Your account is deactivated due to overdraft. Please deposit funds to reactivate.[/red]")
                self.curr_user = account
                console.print(
                    f"Login successful. Welcome[bold] {account.first_name} {account.last_name}[/bold]✨")
                self.user_menu()
                return
            else:
                console.print(
                    "[bold red]Wrong ID or password. Please try again.[/bold red]")

    def show_account_info(self):
        print("\nYour account balances:")
        if self.curr_user.checking is not None:
            print(f"Checking: ${self.curr_user.checking}")
        else:
            print("Checking: Not created yet")
        if self.curr_user.savings is not None:
            print(f"Savings: ${self.curr_user.savings}")
        else:
            print("Savings: Not created yet")
        print("")

    def create_account(self):
        response = input(
            "Would you like to create a new account? (Yes/No): ").strip().capitalize()
        if response != "Yes":
            console.print("[bold]Okay, See You Soon 😓[/bold]")
            return None

        first_name = console.input(
            "Please enter your [bold]First name:[/bold] ")
        last_name = console.input("Please enter your [bold]Last name:[/bold]")
        password = console.input("Enter [bold]password:[/bold] ")

        print("Select account type to create:")
        print("1. Checking")
        print("2. Savings")
        print("3. Both")

        while True:
            account_type = input("Choose (1/2/3): ").strip()
            if account_type in ["1", "2", "3"]:
                break
            console.print("[bold red]Please enter 1, 2, or 3.[/bold red]")

        checking, savings = None, None
        if account_type == "1":
            checking = int(input("Enter initial deposit for Checking: "))
        elif account_type == "2":
            savings = int(input("Enter initial deposit for Savings: "))
        elif account_type == "3":
            checking = int(input("Enter initial deposit for Checking: "))
            savings = int(input("Enter initial deposit for Savings: "))

        for step in track(range(10), description="[bold green]Creating your Account[/bold green]"):
            time.sleep(0.2)

        new_id = max([acc.id for acc in self.accounts], default=0) + 1
        new_account = Customer(
            new_id, first_name, last_name, password, checking, savings)
        self.accounts.append(new_account)
        self.csv_handler.save_all(self.accounts)

        console.print(
            f"Account created for {first_name} {last_name}. [bold green] Your ID to log in is: {new_id} [bold green]")
        return new_account

    def add_missing_account(self):
        if not self.curr_user:
            console.print("[bold red]No user is logged in.[/bold red]")
            return

        options = {}
        if self.curr_user.checking is None:
            options["1"] = "Checking"
        if self.curr_user.savings is None:
            options["2"] = "Savings"

        if not options:
            console.print("[bold]]You already have both Checking and Savings accounts.[/bold]")
            return

        print("You can create the following missing account(s):")
        for key, name in options.items():
            print(f"{key}. {name}")

        while True:
            choice = input("Choose account to create: ").strip()
            if choice in options:
                break
            console.print(
                "[bold red]Invalid choice. Please try again.[/bold red]")

        amount = int(input(f"Enter initial deposit for {options[choice]}: "))
        if choice == "1":
            self.curr_user.checking = amount
        else:
            self.curr_user.savings = amount

        self.csv_handler.save_all(self.accounts)
        print(f"{options[choice]} account created with ${amount}.")

    def withdraw(self):
        if not self.curr_user:
            return
        print("Which account to withdraw from?")
        print("1. Checking")
        print("2. Savings")
        while True:
            choice = input("Choose: ").strip()
            if choice in ["1", "2"]:
                break
            console.print("[bold red]Please select 1 or 2.[/bold red]")
        if choice == "1" and self.curr_user.checking is None:
            print("You don't have a Checking account.")
            return
        if choice == "2" and self.curr_user.savings is None:
            print("You don't have a Savings account.")
            return
        while True:
          raw_amount = input("How much do you want to withdraw? ").strip()
          if not raw_amount.isdigit():
             console.print("[bold red]Amount must be a valid number.[/bold red]")
             continue
          amount = int(raw_amount)
          if amount <= 0:
             console.print("[bold red]Amount must be positive.[/bold red]")
             continue
          break
        if amount > 100:
            console.print(
                "[bold]Cannot withdraw more than $100 in one transaction.[/bold]")
            return

        if choice == "1":
            new_balance = self.curr_user.checking - amount
            if new_balance < -100:
                console.print(
                    "[bold]Cannot overdraw more than $100 in Checking.[/bold]")
                return
            self.curr_user.checking = new_balance
        else:
            new_balance = self.curr_user.savings - amount
            if new_balance < -100:
                console.print(
                    "[bold]Cannot overdraw more than $100 in Savings.[/bold]")
                return
            self.curr_user.savings = new_balance

        overdraft_occurred = False

        if (choice == "1" and self.curr_user.checking < 0 and self.curr_user.checking - 35 < -100) or \
                (choice == "2" and self.curr_user.savings < 0 and self.curr_user.savings - 35 < -100):
            console.print(
                "Transaction denied: [bold]Overdraft fee would exceed $-100 limit.[/bold]")
            return

        if (choice == "1" and self.curr_user.checking < 0) or \
           (choice == "2" and self.curr_user.savings < 0):
            console.print("[bold]Overdraft! $35 fee applied.[/bold]")
            if choice == "1":
                self.curr_user.checking -= 35
            else:
                self.curr_user.savings -= 35
            self.curr_user.overdrafts += 1
            overdraft_occurred = True

        if self.curr_user.overdrafts >= 2:
            console.print(
                "[bold red]Your account has been deactivated due to repeated overdrafts.[/bold red]")
            self.curr_user.active = False

        self.curr_user.transactions.append(Transaction(
            "Withdraw", amount, account_from=("Checking" if choice == "1" else "Savings")))
        self.csv_handler.save_all(self.accounts)
        print(f"${amount} withdrawn successfully." +
              (" Overdraft applied." if overdraft_occurred else ""))

    def deposit(self):
        if not self.curr_user:
            return
        print("Which account to deposit to?")
        print("1. Checking")
        print("2. Savings")
        while True:
            choice = input("Choose: ").strip()
            if choice in ["1", "2"]:
                break
            console.print("[bold red]Please select 1 or 2.[/bold red]")

        if choice == "1" and self.curr_user.checking is None:
            print("You don't have a Checking account.")
            return
        if choice == "2" and self.curr_user.savings is None:
            print("You don't have a Savings account.")
            return

        while True:
           raw_amount = input("Enter amount to deposit: ").strip()
           if not raw_amount.isdigit():
               console.print("[bold red]Amount must be a valid number.[/bold red]")
               continue
           amount = int(raw_amount)
           if amount <= 0:
             console.print("[bold red]Amount must be positive.[/bold red]")
             continue
           break
        if choice == "1":
            self.curr_user.checking += amount
        else:
            self.curr_user.savings += amount

        if not self.curr_user.active and ((self.curr_user.checking or 0) >= 0 and (self.curr_user.savings or 0) >= 0):
            self.curr_user.active = True
            self.curr_user.overdrafts = 0
            print("Your account has been reactivated.")

        self.curr_user.transactions.append(Transaction(
            "Deposit", amount, account_to=("Checking" if choice == "1" else "Savings")))
        self.csv_handler.save_all(self.accounts)
        print(f"${amount} deposited successfully.")

    def transfer(self):
        if not self.curr_user:
            return
        print("Transfer options:")
        print("1. Between your own accounts")
        print("2. To another user")
        while True:
            choice = input("Choose: ").strip()
            if choice in ["1", "2"]:
                break
            console.print("[bold red]Please select 1 or 2.[/bold red]")

        if choice == "1":
            if self.curr_user.checking is None or self.curr_user.savings is None:
                print("You need both accounts to transfer between them.")
                return
            print("Transfer from:")
            print("1. Checking to Savings")
            print("2. Savings to Checking")
            while True:
                 t_choice = input("Choose: ").strip()
                 if t_choice in ["1", "2"]:
                     break
                 console.print("[bold red]Please select 1 or 2.[/bold red]")
            while True:
               raw_amount = input("Enter amount: ").strip()
               if not raw_amount.isdigit():
                  console.print("[bold red]Amount must be a valid number.[/bold red]")
                  continue
               amount = int(raw_amount)
               if amount <= 0:
                   console.print("[bold red]Amount must be positive.[/bold red]")
                   continue
               break
               
            if t_choice == "1":
                if self.curr_user.checking - amount < -100:
                    print("Cannot overdraw more than $100.")
                    return
                self.curr_user.checking -= amount
                self.curr_user.savings += amount
                self.curr_user.transactions.append(Transaction(
                    "Transfer", amount, "Checking", "Savings"))
            elif t_choice == "2":
                if self.curr_user.savings - amount < -100:
                    print("Cannot overdraw more than $100.")
                    return
                self.curr_user.savings -= amount
                self.curr_user.checking += amount
                self.curr_user.transactions.append(Transaction(
                    "Transfer", amount, "Savings", "Checking"))
            else:
                print("Invalid choice.")
                return

            self.csv_handler.save_all(self.accounts)
            print("Transfer successful.")

        elif choice == "2":
            while True:
              raw_id = console.input("Enter the [bold green]user ID[/bold green] to transfer to: ").strip()
              if raw_id.isdigit():
                 target_id = int(raw_id)
                 break
              console.print("[bold red]User ID must be a valid number only.[/bold red]")
            target = self.find_id(target_id)
            if not target:
                print("User not found.")
                return

            print("Which of your accounts to transfer from?")
            print("1. Checking")
            print("2. Savings")
            while True:
              t_choice = input("Choose: ").strip()
              if t_choice in ["1", "2"]:
                  break
              console.print("[bold red]Please select 1 or 2.[/bold red]")
            while True:
               try:
                  amount = int(input("Enter amount: "))
                  if amount <= 0:
                    console.print("[bold red]Amount must be positive.[/bold red]")
                    continue
                  break
               except ValueError:
                  console.print("[bold red]Please enter a valid number.[/bold red]")

            if t_choice == "1":
                if self.curr_user.checking is None:
                    console.print(
                        "[bold]You don't have a Checking account.[/bold]")
                    return
                if self.curr_user.checking - amount < -100:
                    console.print(
                        "[bold]Cannot overdraw more than $100.[/bold]")
                    return
            else:
                if self.curr_user.savings is None:
                    console.print(
                        "[bold]You don't have a Savings account.[/bold]")
                    return
                if self.curr_user.savings - amount < -100:
                    console.print(
                        "[bold]Cannot overdraw more than $100.[/bold]")
                    return

            print("Which account of the recipient?")
            print("1. Checking")
            print("2. Savings")
            while True:
                r_choice = input("Choose: ").strip()
                if r_choice in ["1", "2"]:
                       break
                console.print("[bold red]Please select 1 or 2.[/bold red]")
            if r_choice == "1":
                if target.checking is None:
                    console.print(
                        "Recipient does not have a Checking account.[bold] Transfer cancelled.[/bold]")
                    return
            else:
                if target.savings is None:
                    console.print(
                        "Recipient does not have a Savings account.[bold] Transfer cancelled.[/bold]")
                    return

            if t_choice == "1":
                self.curr_user.checking -= amount
            else:
                self.curr_user.savings -= amount

            if r_choice == "1":
                target.checking += amount
            else:
                target.savings += amount

            self.curr_user.transactions.append(
                Transaction("Transfer", amount, "User", "Recipient"))
            self.csv_handler.save_all(self.accounts)
            console.print("Transfer to other user [bold]successful.[/bold]")

    def user_menu(self):
        while True:
            console.print("\n[bold]Select an action:[/bold]")
            print("1. Show account balances")
            print("2. Add missing account")
            print("3. Withdraw")
            print("4. Deposit")
            print("5. Transfer")
            print("6. Logout")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.show_account_info()
            elif choice == "2":
                self.add_missing_account()
            elif choice == "3":
                self.withdraw()
            elif choice == "4":
                self.deposit()
            elif choice == "5":
                self.transfer()
            elif choice == "6":
                console.print(
                    f"See you later,[bold] {self.curr_user.first_name} {self.curr_user.last_name}[/bold]✨")
                self.curr_user = None
                break
            else:
                console.print(
                    "[bold red]Invalid choice. Please enter a number from 1 to 6.[/bold red]")


# ---------------- Main ----------------
if __name__ == "__main__":
    csv_handler = Csv(bank_Data)
    bank = Bank(csv_handler)

    print(Style.BRIGHT + Back.GREEN +
          "Hello, welcome to Green Bank!" + Style.RESET_ALL)

    while True:
        user_choice = input(
            "Do you have an account? (Yes/No): ").strip().capitalize()
        if user_choice == "Yes":
            bank.sign_in()
            break
        elif user_choice == "No":
            new_acc = bank.create_account()
            if new_acc:
                bank.sign_in()
            break
        else:
            console.print("[bold red]Please enter Yes or No.[/bold red]")
