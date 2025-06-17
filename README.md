# ⏱ Time Tracker CLI App

A lightweight command-line tool for logging and summarizing work hours across personal and proffesional projects.

## Features

- Log time with description, category, and project
- CSV-based logging
- Inquirer-powered interactive CLI
- Edit entries and view logs
- Minimal and clean UI

## Setup

    1.	Clone the repo

    ```bash
    git clone https://github.com/YOUR_USERNAME/time-tracker-cli.git
    cd time-tracker-cli
    ```

    2.	Create a virtual environment and install dependencies

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install InquirerPy
    ```

    3.	(Optional) Create a symlink to run tracker from anywhere:

    ```bash
    chmod +x tracker.py
    ln -s $(pwd)/tracker.py ~/bin/tracker
    ```
    4.	Make sure ~/bin is in your $PATH. If not, add this line to your ~/.zshrc or ~/.bashrc:

    ```bash
    export PATH="$HOME/bin:$PATH"
    ```
    5.	Then restart your terminal or run source ~/.zshrc.

    6.	Now you can just type:

    ```bash
    tracker
    ```
    …from any directory to launch the app.

---

Let me know if you want to add support for a `--help` flag or command-line arguments down the line!
