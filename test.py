
# # from colorama import Fore, Back, Style

# # print(Fore.YELLOW + "lsdvm.sdml")
# # print(Style.RESET_ALL + "رجوع للوضع العادي")

# # print(Back.BLUE + "lsajcvlaksvnlksavn")
# # print(Style.BRIGHT + "ksclsjaclsjac")

# # import pyfiglet

# # print(pyfiglet.figlet_format("Hello!"))

# from rich.console import Console

# console = Console()

# console.print("[bold red]HHHHHHHHHHHHHHHI[/bold red] [green]Welcomeeeeeeeeeeeeee[/green] [blue]!![/blue]")
# import time
# from rich.progress import track

# for step in track(range(10), description="Creat you Account"):
#     time.sleep(0.2)
import time
from rich.progress import track

for step in track(range(10), description="[bold green]Create your Account[/bold green]"):
    time.sleep(0.2)
