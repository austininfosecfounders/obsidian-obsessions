#!/Users/pedram/venv3/bin/python

import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from chrome_fetch import chrome_fetch

FABRIC   = "/Users/pedram/.local/bin/fabric"
PATTERNS = "/Users/pedram/Library/Mobile Documents/iCloud~md~obsidian/Documents/Pedsidian/Fabric/Patterns"
DEBUG    = 0 or os.getenv("DEBUG")

class TaskHandler(FileSystemEventHandler):
    def process(self, event):
        if not event.is_directory and event.event_type in ("created", "modified"):
            if os.path.exists(event.src_path):
                with open(event.src_path, 'r') as file:
                    content = file.read()
                if "ready_to_process: true" in content:
                    print(f"{event.src_path[len(PATTERNS):]} was just {event.event_type}")
                    task_content = self.extract_task(content)
                    if task_content:
                        self.execute_task(task_content, event.src_path)

    def extract_task(self, content):
        task_start = content.find('# Input')
        if task_start != -1:
            return content[task_start + len('# Input'):].strip()
        return None

    def execute_task(self, task_content, src_path):
        pattern = src_path.split('/')[-3]  # Extract pattern name dynamically
        outbox_path = src_path.replace("INBOX", "OUTBOX")
        outbox_dir = os.path.dirname(outbox_path)

        if not os.path.exists(outbox_dir):
            os.makedirs(outbox_dir)
            print(f"Created OUTBOX directory at {outbox_dir}")

        print(f"processing with {pattern}...")

        if DEBUG:
            print(task_content)
            print(f"{FABRIC} --pattern {pattern}")

        result = subprocess.run([FABRIC, "--pattern", pattern], input=task_content, text=True, capture_output=True)
        print(f"writing to {outbox_path[len(PATTERNS):]}")

        if DEBUG:
            print(result.stdout)

        with open(outbox_path, 'w') as out_file:
            out_file.write(result.stdout)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

if __name__ == "__main__":
    if DEBUG:
        print("DEBUG enabled")

    print("watching folders...")
    paths = []
    for root, dirs, files in os.walk(PATTERNS):
        if "INBOX" in dirs:
            inbox_path = os.path.join(root, "INBOX")
            paths.append(inbox_path)
            print(f"    {inbox_path[len(PATTERNS):]}")

    event_handler = TaskHandler()
    observer = Observer()
    for path in paths:
        observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
