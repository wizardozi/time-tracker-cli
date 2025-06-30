#!/Users/alexandredenommee/Workspace/Coding/Projects/time-tracker-app/venv/bin/python
# App built to track my hours worked
import csv
import datetime
from InquirerPy import inquirer
from log import write_file, get_projects, ensure_log_file_exists
from utils import clear_terminal, ask_yes_no, parse_time_estimate
from config import LOG_FILE, TIMER_FILE
import subprocess
import sys
import click

def launch_timer(project):
    subprocess.Popen([sys.executable, TIMER_FILE, project], stdin=subprocess.DEVNULL)


def select_project(projects):
    return inquirer.select(
        message="Select a project:",
        choices=sorted(projects),
        default=None,
    ).execute()


def get_project_category_map(log_file=LOG_FILE):
    mapping =  {}
    try:
        with open(log_file, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                project = row.get("Project")
                category = row.get("Category")
                if project and category and project not in mapping:
                    mapping[project] = category
    except FileNotFoundError:
        pass
    return mapping


def get_project(projects):
    project = ''
    while True:
        if projects:
            choice = ''
            while choice not in ['1', '2']:
                clear_terminal()
                print("Choose an option:")
                print("1. List projects")
                print("2. Enter new project")
                choice = input("> ").strip().lower()

                if choice == 'q':
                    return None

                if choice == '1':
                    clear_terminal()
                    project = select_project(projects)
                    if project is None:
                        return None
                    confirm = ask_yes_no()
                    if confirm == 'y':
                        return project
                    else:
                        break
                elif choice == '2':
                    clear_terminal()
                    print("Enter new project:")
                    project = input('> ').strip()
                    if project.lower() == 'q':
                        return None
                    confirm = ask_yes_no()
                    if confirm == 'y':
                        return project
                    else:
                        break
        else:
            clear_terminal()
            print('---------------------------')
            print("⚠️ No projects logged yet.")
            print('---------------------------\n')
            print("Enter new project:")
            project = input('> ').strip()
            if project.lower() == 'q':
                return None
            confirm = ask_yes_no()
            if confirm == 'y':
                return project


def get_date():
    date = ''
    while True:
        clear_terminal()
        print('Choose an option:')
        print("1. Today")
        print("2. Enter Date")
        choice = ''
        while choice not in ['1', '2']:
            choice = input("> ").strip().lower()
            if choice == 'q':
                return None

            if choice == '1':
                date = datetime.date.today()
                print(f"> {date}")
            elif choice == '2':
                print("Enter a date (YYYY-MM-DD):")
                user_input = input('> ').strip()
                if user_input.lower() == 'q':
                    return None
                try:
                    date_obj = datetime.datetime.strptime(user_input, "%Y-%m-%d")
                    if date_obj.year != datetime.datetime.now().year:
                        raise ValueError("Invalid year")
                    date = user_input
                except ValueError:
                    print("⚠️ Year must be current and format valid (e.g. 2025-06-16)")
                    input("Press Enter to try again...")
                    continue

        confirm = ask_yes_no()
        if confirm == 'y':
            return date


def get_hours():
    while True:
        clear_terminal()
        print("Enter hours worked (e.g. 1.5):")
        user_input = input('> ').strip().lower()
        if user_input == 'q':
            return None
        hours = parse_time_estimate(user_input)
        if hours is None or hours <= 0:
            print('⚠️ Please enter a valid time (e.g. 1.5, 30m, 1h).')
            input("Press Enter to try again...")
            continue
        click.echo(hours)
        confirm = ask_yes_no()
        if confirm == 'y':
            return hours


def get_category():
    categories = ["Personal","Creative", "Music", "Client", "Freelance", "Learning", "Other"]

    category = inquirer.select(
        message="Select a category for this work:",
        choices=categories,
        default="Personal",
    ).execute()
    confirm = ask_yes_no()
    if confirm == 'y':
        return category


def get_description():
    while True:
        clear_terminal()
        print('Enter description (max 250 characters):')
        description = input('> ').strip()
        if description.lower() == 'q':
            return None
        if len(description) > 250:
            print(f"⚠️ Description too long ({len(description)} characters). Max is 250.")
            input("Press Enter to try again...")
            continue
        confirm = ask_yes_no()
        if confirm == 'y':
            return description


def log_hours():
    while True:
        clear_terminal()
        timestamp = datetime.datetime.now().isoformat()
        projects = get_projects()

        project = get_project(projects)
        if project is None:
            print("❌ Entry canceled at project step.")
            input("Press Enter to return to main menu...")
            return

        date = get_date()
        if date is None:
            print("❌ Entry canceled at date step.")
            input("Press Enter to return to main menu...")
            return

        hours = get_hours()
        if hours is None:
            print("❌ Entry canceled at hours step.")
            input("Press Enter to return to main menu...")
            return

        project_category_map = get_project_category_map()
        category = project_category_map.get(project)

        if not category:
            category = get_category()
            if category is None:
                print("❌ Entry canceled at category step.")
                input("Press Enter to return to main menu...")
                return

        description = get_description()
        if description is None:
            print("❌ Entry canceled at description step.")
            input("Press Enter to return to main menu...")
            return

        print("\n📝 New Entry:")
        print(f"Project: {project}")
        print(f"Date: {date}")
        print(f"Hours: {hours}")
        print(f"Category: {category}")
        print(f"Description: {description}\n")

        confirm = ask_yes_no("Save this entry? (y/n): ")
        if confirm == 'y':
            write_file([timestamp, project, date, hours, category, description])
            return
        elif confirm == 'n':
            print('🔁 Resetting entry...')







def edit_entry():
    clear_terminal()
    print("📋 Loading entries...\n")

    # Load all entries
    with open(LOG_FILE, 'r', newline='') as file:
        reader = csv.DictReader(file)
        entries = list(reader)

    if not entries:
        print("⚠️ No entries found to edit.")
        input("Press Enter to return to main menu...")
        return

    # Build list of entry labels
    entry_labels = [
        f"{i+1}. {row['Date']} | {row['Project']} | {row['Hours']}h | {row['Category']} | {row['Description'][:30]}..."
        for i, row in enumerate(entries)
    ]

    # User selects an entry
    selected_label = inquirer.select(
        message="Select an entry to edit:",
        choices=entry_labels,
    ).execute()

    selected_index = entry_labels.index(selected_label)
    entry = entries[selected_index]

    # Show old values and ask for updated values
    clear_terminal()
    print("🔧 Editing Entry:")
    print(f"Original - Project: {entry['Project']}, Date: {entry['Date']}, Hours: {entry['Hours']}, Description: {entry['Description']}\n")

    projects = get_projects()

    updated_project = get_project(projects) or entry['Project']
    updated_date = get_date() or entry['Date']
    updated_hours = get_hours() or float(entry['Hours'])
    updated_category = get_category() or entry['Category']
    updated_description = get_description() or entry['Description']

    confirm = ask_yes_no("Save these changes? (y/n): ")
    if confirm != 'y':
        print("❌ Edit canceled.")
        input("Press Enter to return to main menu...")
        return

    # Update the selected entry
    entries[selected_index] = {
        "Timestamp": entry["Timestamp"],  # Keep original timestamp
        "Project": updated_project,
        "Date": updated_date,
        "Hours": str(updated_hours),
        "Category": updated_category,
        "Description": updated_description
    }

    # Rewrite CSV with updated entry list
    with open(LOG_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Timestamp", "Project", "Date", "Hours", "Category", "Description"])
        writer.writeheader()
        writer.writerows(entries)

    print("✅ Entry updated successfully.")
    input("Press Enter to return to main menu...")
    return


def delete_entry():
    clear_terminal()
    print("🗑️  Delete an Entry\n")

    # Load all entries
    with open(LOG_FILE, 'r', newline='') as file:
        reader = csv.DictReader(file)
        entries = list(reader)

    if not entries:
        print("⚠️ No entries found to delete.")
        input("Press Enter to return to main menu...")
        return

    # Build list of entry labels
    entry_labels = [
        f"{i+1}. {row['Date']} | {row['Project']} | {row['Hours']}h | {row['Category']} | {row['Description'][:30]}..."
        for i, row in enumerate(entries)
    ]

    # User selects an entry
    selected_label = inquirer.select(
        message="Select an entry to delete:",
        choices=entry_labels,
    ).execute()

    selected_index = entry_labels.index(selected_label)
    entry = entries[selected_index]

    clear_terminal()
    print("⚠️ Confirm Deletion")
    print(f"Project: {entry['Project']}")
    print(f"Date: {entry['Date']}")
    print(f"Hours: {entry['Hours']}")
    print(f"Category: {entry['Category']}")
    print(f"Description: {entry['Description']}\n")

    confirm = ask_yes_no("Are you sure you want to delete this entry? (y/n): ")
    if confirm != 'y':
        print("❌ Deletion canceled.")
        input("Press Enter to return to main menu...")
        return

    # Remove the entry and rewrite file
    del entries[selected_index]
    with open(LOG_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Timestamp", "Project", "Date", "Hours", "Category", "Description"])
        writer.writeheader()
        writer.writerows(entries)

    print("✅ Entry deleted successfully.")
    input("Press Enter to return to main menu...")

def get_projects_by_date(day=False, week=False, month=False, date_range=None, project=None):
    with open(LOG_FILE, 'r') as file:
        reader = csv.DictReader(file)
        entries = list(reader)

    if not entries:
        print("⚠️ No entries found.")
        input("Press Enter to return to main menu...")
        return

    today = datetime.date.today()
    filtered = []
    for row in entries:
        entry_date = datetime.datetime.strptime(row['Date'], "%Y-%m-%d").date()

        if day and entry_date != today:
            continue
        elif week and not (today - datetime.timedelta(days=today.weekday()) <= entry_date <= today):
            continue
        elif month and not (entry_date.year == today.year and entry_date.month == today.month):
            continue
        elif date_range:
            try:
                start = datetime.datetime.strptime(date_range[0], "%Y-%m-%d").date()
                end = datetime.datetime.strptime(date_range[1], "%Y-%m-%d").date()
                if not (start <= entry_date <= end):
                    continue
            except ValueError:
                print("⚠️ Invalid date range format. Use YYYY-MM-DD.")
                input("Press Enter to return...")
                return
        if project and row['Project'] != project:
            continue

        filtered.append(row)
    return filtered

def view_entries(day=False, week=False, month=False, date_range=None, project=None):
    clear_terminal()
    filtered = get_projects_by_date(day, week, month, date_range, project)
    if not filtered:
        print("⚠️ No matching entries.")
    else:
        for i, row in enumerate(filtered, start=1):
            print(f"{i}. {row['Date']} | {row['Project']} | {row['Hours']}h")
            print(f"   {row['Description']}\n")


def show_summary(day=False, week=False, month=False, date_range=None, project=None):
    clear_terminal()
    summary_dict = {}
    filtered = get_projects_by_date(day, week, month, date_range, project)
    if not filtered:
        print("⚠️ No matching entries.")
    else:
        for row in filtered:
            try:
                hours = float(row.get("Hours", 0))
            except ValueError:
                continue  # skip invalid rows
            project = row.get("Project")
            if project in summary_dict:
                summary_dict[project] += hours
            else:
                summary_dict[project] = hours

    print("📊 Work Summary by Project:")
    print("---------------------------")
    for project, total_hours in summary_dict.items():
        print(f"{project}: {total_hours:.2f} hours")

# --- Click CLI group and subcommands ---

@click.group()
def cli():
    """Time Tracker CLI"""
    ensure_log_file_exists()

@cli.command()
def log():
    """Log hours manually"""
    log_hours()

@cli.command()
def timer():
    """Launch timer for a selected project"""
    projects = get_projects()
    selected_project = get_project(projects)
    if selected_project:
        launch_timer(selected_project)
    else:
        launch_timer("Default")

@cli.command()
@click.option('--day', is_flag=True, help="Show today's summary")
@click.option('--week', is_flag=True, help="Show summary for this week")
@click.option('--month', is_flag=True, help="Show summary for this month")
@click.option('--range', nargs=2, type=str, metavar='<START> <END>', help="Custom date range (YYYY-MM-DD YYYY-MM-DD)")
@click.option('--project', is_flag=True, help="Filter by project")
def summary(day, week, month, range, project):
    """Show project summary"""
    selected_project = None
    if project:
        selected_project = select_project(get_projects())
    show_summary(day=day, week=week, month=month, date_range=range, project=selected_project)

@cli.command()
@click.option('--day', is_flag=True, help="View today's entries")
@click.option('--week', is_flag=True, help="View entries from this week")
@click.option('--month', is_flag=True, help="View entries from this month")
@click.option('--range', nargs=2, type=str, metavar='<START> <END>', help="View entries in date range (YYYY-MM-DD YYYY-MM-DD)")
@click.option('--project', is_flag=True, help="Filter by project")
def view(day, week, month, range, project):
    """View all or filtered entries"""
    selected_project = None
    if project:
        selected_project = select_project(get_projects())
    view_entries(day=day, week=week, month=month, date_range=range, project=selected_project)

@cli.command()
def edit():
    """Edit an entry"""
    edit_entry()

@cli.command()
def delete():
    """Delete an entry"""
    delete_entry()


if __name__ == "__main__":
    cli()
