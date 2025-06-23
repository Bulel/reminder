import json
import os
import time
import datetime
import ctypes
import threading

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def show_reminder(msg):
    ctypes.windll.user32.MessageBoxW(0, msg, "Health Reminder", 0x40)

def is_quiet_hour(now, quiet_hours):
    start, end = quiet_hours
    if start < end:
        return start <= now.hour < end
    else:
        return now.hour >= start or now.hour < end

def start_reminder_thread(reminder, quiet_hours):
    def loop():
        while True:
            now = datetime.datetime.now()
            weekday = now.isoweekday()
            hour = now.hour

            if (weekday in reminder["days"] and
                reminder["hour_range"][0] <= hour < reminder["hour_range"][1] and
                not is_quiet_hour(now, quiet_hours)):
                show_reminder(reminder["message"])
            time.sleep(reminder["interval_minutes"] * 60)

    threading.Thread(target=loop, daemon=True).start()

def main():
    config = load_config()
    for r in config["reminders"]:
        start_reminder_thread(r, config["quiet_hours"])
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
