# import csv
# from colorama import Style, Back
# from rich.console import Console
# from rich.progress import track
# import time

# console = Console()
# bank_Data = "bank.csv"


# def from_Csv(bank_Data):
#     accounts = []
#     try:
#         with open(bank_Data, newline='', encoding='utf-8') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 account = BankAccount(
#                     id=int(row['id']),
#                     first_name=row['first_name'].strip(),
#                     last_name=row['last_name'].strip(),
#                     password=row['password'],
#                     checking=None if row['checking'] == 'None' else int(
#                         row['checking']),
#                     savings=None if row['savings'] == 'None' else int(
#                         row['savings']),
#                 )
#                 accounts.append(account)
#     except FileNotFoundError:
#         pass
#     return accounts


# class BankAccount:


#     def __init__(self, id, first_name, last_name, password, checking=0, savings=0):
#         self.id = id
#         self.first_name = first_name
#         self.last_name = last_name
#         self.password = password
#         self.checking = checking
#         self.savings = savings

#     def log_Account(self, accounts_list):
#         while True:
#             try:
#                 account_id = int(console.input(
#                     "[bold]Please enter your [green]ID number [/green]to Log In: [/bold]"))
#             except ValueError:
#                 console.print(
#                     "[bold red]Please enter a numeric ID.[/bold red]")
#                 continue

#             password = console.input(
#                 "[bold]Enter your [green]password[/green] : [/bold]")
#             account = find_id(account_id, accounts_list)

#             if account and account.password == password:
#                 print(
#                     f"Login successful. Welcome {account.first_name} {account.last_name}!")
#                 return account
#             else:
#                 console.print(
#                     "[bold red]Wrong ID or password. Please try again.[/bold red]")

#     def new_Account(self, accounts_list, bank_Data=bank_Data):
#         while True:
#             response = input(
#                 "Would you like to open a new account? (Yes/No): ").strip().capitalize()
#             if response == "Yes":
#                 first_name = input("Please enter your First name: ")
#                 last_name = input("Please enter your Last name: ")
#                 password = input("Enter password: ")

#                 while True:
#                     account_type = input(
#                         "Which account do you want? \n1. Checking\n2. Savings\n3. Both\nChoose (1/2/3): ").strip()
#                     if account_type in ["1", "2", "3"]:
#                         break
#                     else:
#                         console.print(
#                             "[bold red]Please enter 1, 2, or 3.[/bold red]")
#                 checking = 0
#                 savings = 0
#                 if account_type == "1":
#                     checking = int(
#                         input("Enter initial deposit for Checking: "))
#                 elif account_type == "2":
#                     savings = int(
#                         input("Enter initial deposit for Savings: "))
#                 elif account_type == "3":
#                     checking = int(
#                         input("Enter initial deposit for Checking: "))
#                     savings = int(
#                         input("Enter initial deposit for Savings: "))

#                 for step in track(range(10), description="[bold green]Creating your Account[/bold green]"):
#                     time.sleep(0.2)

#                 new_id = max(acc.id for acc in accounts_list) + \
#                     1 if accounts_list else 1
#                 new_account = BankAccount(
#                     new_id, first_name, last_name, password, checking, savings)
#                 accounts_list.append(new_account)

#                 with open(bank_Data, "a", newline="", encoding="utf-8") as f:
#                     writer = csv.writer(f)
#                     if f.tell() == 0:
#                         writer.writerow(
#                             ['id', 'first_name', 'last_name', 'password', 'checking', 'savings'])
#                     writer.writerow(
#                         [new_id, first_name, last_name, password, checking, savings])

#                 print(
#                     f"Account created for {first_name}. Welcome to Green Bank! Your ID to log in is {new_id}")
#                 return new_account

#             elif response == "No":
#                 print("Okay, see you soon!")
#                 return None
#             else:
#                 console.print(
#                     "[bold red]Please enter 'Yes' or 'No'.[/bold red]")


# def find_id(account_id, accounts_list):
#     for acc in accounts_list:
#         if acc.id == account_id:
#             return acc
#     return None


# if __name__ == "__main__":
#     accounts = from_Csv(bank_Data)

#     print(Style.BRIGHT + Back.GREEN +
#           "Hello, welcome to Green Bank!" + Style.RESET_ALL)
#     while True:
#         user_Account = input(
#             Style.RESET_ALL + "Do you have an account in the bank? (Yes/No): ").strip().capitalize()
#         if user_Account == "Yes":
#             BankAccount(0, "", "", "").log_Account(accounts)
#             break
#         elif user_Account == "No":
#             new_acc = BankAccount(0, "", "", "").new_Account(accounts)
#             if new_acc:
#                 BankAccount(0, "", "", "").log_Account(accounts)
#             break
#         else:
#             console.print("[bold red]Please enter 'Yes' or 'No'.[/bold red]")

#الكود الاقدم كلاس واحد