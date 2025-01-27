
# MIT License
#
# Copyright (c) 2025 TheHolyOneZ
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



import requests
import random
import string
import time
from typing import List
from colorama import init, Fore, Back, Style
from datetime import datetime
import os
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.panel import Panel
from rich.prompt import Prompt

init(autoreset=True)
console = Console()

class InviteGenerator:
    def __init__(self):
        self.patterns = [
            (6, string.ascii_letters + string.digits),
            (8, string.ascii_letters + string.digits),
            (10, string.ascii_letters + string.digits),
        ]
        
    def generate_invite_code(self) -> str:
        length, charset = random.choice(self.patterns)
        code = ''
        for _ in range(length):
            if random.random() < 0.3:
                code += random.choice(string.ascii_uppercase)
            else:
                code += random.choice(charset)
        return code

def check_invite(invite_code: str) -> bool:
    url = f"https://discord.com/api/v9/invites/{invite_code}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    
    try:
        response = requests.get(url, headers=headers)
        return response.status_code == 200
    except:
        return False

def save_invite(invite: str, guild_name: str = "Unknown"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("valid.txt", "a", encoding='utf-8') as f:
        f.write(f"+=========================+\n")
        f.write(f"| Found: {timestamp}\n")
        f.write(f"| Invite: https://discord.gg/{invite}\n")
        f.write(f"| Server: {guild_name}\n")
        f.write(f"+=========================+\n\n")

def test_specific_invite():
    should_test = Prompt.ask("[yellow]Would you like to test a specific invite first?[/yellow] (y/n)")
    if should_test.lower() == 'y':
        test_invite = Prompt.ask("[cyan]Enter Discord invite code or full URL[/cyan]")
        if 'discord.gg/' in test_invite:
            test_invite = test_invite.split('discord.gg/')[-1]
        
        console.print(f"\n[bold]Testing invite: {test_invite}[/bold]")
        if check_invite(test_invite):
            console.print("[bold green]✓ Test invite is VALID![/bold green]")
            save_invite(test_invite)
        else:
            console.print("[bold red]✗ Test invite is INVALID![/bold red]")
        
        time.sleep(2)
        console.print("\n[bold cyan]Starting random invite checker...[/bold cyan]\n")

def display_banner():
    banner = """
    ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗ 
    ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗
    ██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║
    ██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║
    ██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝
    ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
    """
    console.print(f"[bold magenta]{banner}[/bold magenta]")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    display_banner()
    console.print(Panel.fit(
        "[bold magenta]Discord Invite Finder[/bold magenta]\n"
        "[cyan]    Made by TheZ[/cyan]",
        border_style="green"
    ))
    
    test_specific_invite()
    
    generator = InviteGenerator()
    valid_count = 0
    total_checked = 0
    start_time = datetime.now()
    
    while True:
        total_checked += 1
        invite = generator.generate_invite_code()
        
        with console.status(f"[bold blue]Checking invite: {invite}...") as status:
            if check_invite(invite):
                console.print(f"[bold green]✓ VALID[/bold green] Found working invite: discord.gg/{invite}")
                save_invite(invite)
                valid_count += 1
            else:
                console.print(f"[red]✗ Invalid[/red] discord.gg/{invite}")
        
        elapsed_time = datetime.now() - start_time
        checks_per_minute = total_checked / (elapsed_time.total_seconds() / 60)
        
        console.print(Panel(
            f"[yellow]Stats:[/yellow]\n"
            f"Checked: {total_checked}\n"
            f"Valid: {valid_count}\n"
            f"Success Rate: {(valid_count/total_checked)*100:.2f}%\n"
            f"Checks per minute: {checks_per_minute:.1f}\n"
            f"Running time: {str(elapsed_time).split('.')[0]}",
            border_style="blue"
        ))
        
        time.sleep(1.5)

if __name__ == "__main__":
    main()
