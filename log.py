
import os
import csv
from config import LOG_FILE

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

LOG_FILE = os.path.join(SCRIPT_DIR, 'work_log.csv')
def ensure_log_file_exists():
    if not os.path.isfile(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
        with open(LOG_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Project', 'Date', 'Hours', 'Category', 'Description'])


def write_file(new_entry):

    filename = LOG_FILE

    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists or os.stat(filename).st_size == 0:
            writer.writerow(['Timestamp', 'Project', 'Date', 'Hours', 'Category', 'Description'])

        writer.writerow(new_entry)

    print("✅ Entry saved.")

def get_projects():
    projects = set()
    with open(LOG_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("Project"):  # Only collect non-empty project names
                projects.add(row["Project"])
    return projects
