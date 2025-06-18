import rumps
import sys
from datetime import datetime
from datetime import timedelta

class TrackerTimerApp(rumps.App):
    def __init__(self, project):
        super().__init__("⏱ Tracker", icon=None, menu=["Stop", "Reset", None])
        self.timer_running = True
        self.start_time = datetime.now()
        self.total_elapsed = timedelta(0)
        self.last_started = datetime.now()
        self.project = project
        self.update_timer = rumps.Timer(self.update_title, 1)  # runs every 1 second
        self.update_timer.start()

    @rumps.clicked("Stop")
    def toggle_timer(self, sender):
        if not self.timer_running:
            self.last_started = datetime.now()
            self.update_timer.start()
            self.timer_running = True
            sender.title = "Stop"
        else:
            self.total_elapsed += datetime.now() - self.last_started
            self.update_timer.stop()
            self.timer_running = False
            sender.title = "Start"

    @rumps.clicked("Reset")
    def reset_timer(self, _):
        if self.timer_running:
            self.total_elapsed += datetime.now() - self.last_started
            self.timer_running = False
            self.update_timer.stop()
            end_time = datetime.now()

            self.title = "⏱ Tracker"
            hours = round(self.total_elapsed.total_seconds() / 3600, 2)
            rumps.alert(title="Timer Stopped", message=f"Logged {hours} hours to {self.project}")
            self.total_elapsed = timedelta(0)

            # TODO: Save to CSV here

    def update_title(self, _):
        elapsed = self.total_elapsed
        if self.timer_running:
            elapsed += datetime.now() - self.last_started
            h, m, s = elapsed.seconds // 3600, (elapsed.seconds % 3600) // 60, elapsed.seconds % 60
            self.title = f"{self.project} | {h:02}:{m:02}:{s:02}"

project_name = None
project_name = sys.argv[1]
# if len(sys.argv) > 1:
# else:
#     project_name = "Default"

if __name__ == "__main__":
    TrackerTimerApp(project_name).run()