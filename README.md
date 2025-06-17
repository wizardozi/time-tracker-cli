# ⏱ Time Tracker CLI App

A lightweight command-line tool for logging and summarizing work hours across personal and professional projects.

## ✨ Features

- Log time with description, project, hours, date, and category
- CSV-based logging (easy to inspect, edit, or back up)
- Inquirer-powered interactive CLI (arrow keys, cancel with `q`)
- Edit existing entries
- View summaries or full log history
- Minimal, readable terminal UI

---

## 🛠 Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/time-tracker-cli.git
cd time-tracker-cli
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install InquirerPy
```

### 3. (Optional) Create a symlink to run tracker from anywhere:

```bash
chmod +x tracker.py
ln -s $(pwd)/tracker.py ~/bin/tracker
```

### 4. Add ~/bin to your system $PATH (if not already)

In your shell config file (~/.zshrc, ~/.bashrc, or ~/.bash_profile), add:

```bash
export PATH="$HOME/bin:$PATH"
```

Then reload your shell:

```bash
source ~/.zshrc  # or source ~/.bashrc
```

## Usage

```bash
tracker
```

…from any directory to launch the app.

### Inside the app:

• Navigate menus using arrow keys
• Press q at any prompt to cancel or return
• All data is saved to work_log.csv in the project folder (not committed to Git)

### Notes

• You can categorize entries (e.g., Personal, Client, Freelance)
• Easily extendable with filters, exports, time-based summaries, or SQLite
• Designed for minimalism and utility — a clean daily-use CLI

### Future Ideas (Optional Extensions)

• --help flag with CLI argument support
• Weekly/monthly summary views
• Tagging and search
• CSV export filters or markdown reports
• Live timer mode (start / stop log)

---

Let me know if you want to add support for a `--help` flag or command-line arguments down the line!
