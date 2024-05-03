from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import PIPE, run

import subprocess

FILE_LIST_PATH = "files.txt"
COMMAND_FILE_PATH = "command.sh"
POST_COMMAND_FILE_PATH = "post_command.sh"

all_files = []
with open(FILE_LIST_PATH, "r") as f:
    s = f.read()
    all_files = s.split("\n")

print("[Watcher] Watching Files: ", all_files)

def execute():
    command = ""
    with open(COMMAND_FILE_PATH, "r") as f:
        command = f.read()
    print("[Watcher] Command:", command)

    post_command = ""
    with open(POST_COMMAND_FILE_PATH, "r") as f:
        post_command = f.read()
    print("[Watcher] Post Command:", post_command)

    result = subprocess.run(['bash', '-c', command], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    if (result.returncode == 0):
        print("[Watcher] Command Executed Successfully")
        code_output = subprocess.run(['bash', '-c', post_command], universal_newlines=True)
        if code_output.returncode == 0:
            print("\n[Watcher] Exited Successfully")
        else:
            print(f"\n[Watcher] BAD EXIT: {code_output.returncode}")
    else:
        print(result.returncode)

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            execute()

if __name__ == "__main__":
    observer = Observer()
    event_handler = MyHandler()
    for file in all_files:
        observer.schedule(event_handler, path=f"./{file}", recursive=False)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()