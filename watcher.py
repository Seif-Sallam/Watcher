from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from subprocess import PIPE, run

import threading, os, time, subprocess

FILE_LIST_PATH = "files.txt"
COMMAND_FILE_PATH = "command.sh"
POST_COMMAND_FILE_PATH = "post_command.sh"

changed_files = set()
is_live = True
# This function sleeps for 100ms and checks if the file has been modified
def check_files():
    global is_live, changed_files
    while is_live:
        time.sleep(0.1)
        if len(changed_files) > 0:
            print("[Watcher] Files Modified: ", changed_files)
            execute()
            changed_files.clear()

all_files = []
with open(FILE_LIST_PATH, "r") as f:
    s = f.read()
    all_files = s.split("\n")
    all_files = [os.path.join(".", x) for x in all_files]

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
        if event.src_path in all_files and not event.is_directory:
            changed_files.add(event.src_path)

if __name__ == "__main__":
    observer = Observer()
    event_handler = MyHandler()
    observer.schedule(event_handler, path=f".", recursive=False)
    observer.start()

    # start the thread
    thread = threading.Thread(target=check_files)
    thread.start()
    try:
        while is_live:
            pass
    except KeyboardInterrupt:
        is_live = False
        observer.stop()

    observer.join()
    thread.join()