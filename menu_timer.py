import rumps
import sys
from datetime import datetime
from datetime import timedelta
from AppKit import NSApplication
from log import write_file
from tracker import get_project_category_map, get_category, get_description
NSApplication.sharedApplication().setActivationPolicy_(2)

class TrackerTimerApp(rumps.App):
    def __init__(self, project):
        super().__init__("⏱ Tracker", icon=None, menu=["Stop", "Reset", "Save", None])
        self.timer_running = True
        self.start_time = datetime.now()
        self.total_elapsed = timedelta(0)
        self.last_started = datetime.now()
        self.project = project
        self.update_timer = rumps.Timer(self.update_title, 1)  # runs every 1 second
        self.update_timer.start()
        self.timer_state = "Stop"

    @rumps.clicked("Stop")
    def toggle_timer(self, sender):
        if not self.timer_running:
            self.last_started = datetime.now()
            self.update_timer.start()
            self.timer_running = True
            self.menu["Stop"].title = "Stop"
        else:
            self.total_elapsed += datetime.now() - self.last_started
            self.update_timer.stop()
            self.timer_running = False
            self.menu["Stop"].title = "Start"


    @rumps.clicked("Reset")
    def reset_timer(self, _):
        self.timer_running = False
        self.update_timer.stop()
        self.total_elapsed = timedelta(0)
        self.title = f"{self.project} | {0:02}:{0:02}:{0:02}"
        self.menu["Stop"].title = "Start"


    @rumps.clicked('Save')
    def save_time(self, _):
        self.timer_running = False
        self.update_timer.stop()
        self.total_elapsed += datetime.now() - self.last_started
        hours = round(self.total_elapsed.total_seconds() / 3600, 2)
        self.total_elapsed = timedelta(0)
        self.title = f"{hours} hours saved to {self.project}"
        self.menu["Stop"].title = "Start"
        self.save_to_csv(hours)

    def save_to_csv(self, hours):
        timestamp = datetime.now().isoformat()
        date = datetime.today().date()
        project_category_map = get_project_category_map()
        category = project_category_map.get(self.project, "Uncategorized")  # ✅ fallback
        description = "No description"  # ✅ safe default
        write_file([timestamp, self.project, date, hours, category, description])

    def update_title(self, _):
        elapsed = self.total_elapsed
        if self.timer_running:
            elapsed += datetime.now() - self.last_started
            h, m, s = elapsed.seconds // 3600, (elapsed.seconds % 3600) // 60, elapsed.seconds % 60
            self.title = f"{self.project} | {h:02}:{m:02}:{s:02}"

project_name = None
project_name = sys.argv[1]

if __name__ == "__main__":
    TrackerTimerApp(project_name).run()