import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def ask_yes_no(prompt="Confirm (y/n): "):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ['y', 'n']:
            return choice
        print("Please enter 'y' or 'n'.")