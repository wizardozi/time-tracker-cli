import os
import click

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def ask_yes_no(prompt="Confirm (y/n): "):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ['y', 'n']:
            return choice
        print("Please enter 'y' or 'n'.")

def parse_time_estimate(input_str):
    input_str = input_str.strip().lower()

    if input_str in ['q', 'quit']:
        return None

    # Handle minutes (e.g., 5m, 30m)
    if input_str.endswith("m"):
        try:
            minutes = float(input_str[:-1])
            return round(minutes / 60, 2)
        except ValueError:
            return None

    # Handle hours (e.g., 1h, 1.5h)
    if input_str.endswith("h"):
        try:
            hours = float(input_str[:-1])
            return round(hours, 2)
        except ValueError:
            return None

    # Fallback: allow just numbers (assumed to be hours)
    try:
        return round(float(input_str), 2)
    except ValueError:
        return None

def prompt_estimate_rounded():
    raw = click.prompt("Enter time estimate (e.g., 1.5 or 90m or 1:15)")
    try:
        parsed = parse_time_estimate(raw)
        rounded = round(parsed * 4) / 4  # round to nearest 0.25
        return rounded
    except ValueError:
        click.echo("Invalid time format. Try something like 1.5, 90m, or 1:15")
        return prompt_estimate_rounded()