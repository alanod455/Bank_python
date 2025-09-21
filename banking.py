import csv
from colorama import Style, Back
from rich.console import Console
from rich.progress import track

bank_Data = "bank.csv"


def load_accounts_from_csv(bank_Data):
    accounts = []
    with open(bank_Data, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            account = BankAccount(
                id=int(row['id']),
                first_name=row['first_name'].strip(),
                last_name=row['last_name'].strip(),
                password=row['password'],
                checking=float(
                    row['checking']) if row['checking'] != 'False' else 0.0,
                savings=float(
                    row['savings']) if row['savings'] != 'False' else 0.0,
                active=row['active'].strip().lower() == 'true',

            )
            accounts.append(account)
    return accounts


class BankAccount:
    def __init__(self, id, first_name, last_name, password, checking=0.0, savings=0.0, active=True):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.checking = checking
        self.savings = savings
        self.active = active

    def log_Account(self, accounts_list):

        console = Console()
        account_id = int(
            console.input("Please enter your [bold green] ID number [/bold green]to Log In: "))
        password = input(
            Style.BRIGHT + "Enter your password: "+Style.RESET_ALL)
        account = find_account_by_id(account_id, accounts_list)
        if account and account.password == password:
            print(
                f"Login successful. Welcome {account.first_name} {account.last_name}!")
            return account
        else:
            print("Wrong ID or password.")
            return None

    def new_Account(self, accounts_list, bank_Data=bank_Data):
        while True:
            response = input(
                "Would you like to open a new account? (Yes/No): ").strip().capitalize()
            if response == "Yes":
                first_name = input("Please enter your First name: ")
                last_name = input("Please enter your Last name: ")
                password = input("Enter password: ")
                import time

                for step in track(range(10), description="[bold green]Create your Account[/bold green]"):
                 time.sleep(0.2)

                new_id = max(acc.id for acc in accounts_list) + \
                    1 if accounts_list else 1

                new_account = BankAccount(
                    new_id, first_name, last_name, password)
                accounts_list.append(new_account)

                with open(bank_Data, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        [new_id, first_name, last_name, password, 0.0, 0.0, True])

                print(
                    f"Account created for {first_name}. Welcome to Green Bank! Your ID to log in is {new_id}")
                return new_account

            elif response == "No":
                print("Okay, see you soon!")
                return None

            else:
                print("Invalid input. Please enter 'Yes' or 'No'.")


def find_account_by_id(account_id, accounts_list):
    for acc in accounts_list:
        if acc.id == account_id:
            return acc
    return None


if __name__ == "__main__":

    accounts = load_accounts_from_csv(bank_Data)

    print(Style.BRIGHT + Back.GREEN +
          "Hello, welcome to Green Bank!" + Style.RESET_ALL)
    while True:
        user_Account = input(
            Style.RESET_ALL + "Do you have an account in the bank? (Yes/No): ").strip().capitalize()
        if user_Account == "Yes":
            BankAccount(0, "", "", "").log_Account(accounts)
            break
        elif user_Account == "No":
            new_acc = BankAccount(0, "", "", "").new_Account(accounts)
            if new_acc:
                BankAccount(0, "", "", "").log_Account(accounts)
            break
        else:
            print("Please enter 'Yes' or 'No'.")
