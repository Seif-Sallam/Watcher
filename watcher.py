from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import PIPE

import threading, os, time, subprocess, argparse

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_FOLDER = "."
FILE_LIST_PATH = "files.txt"
COMMAND_FILE_PATH = "command.sh"
POST_COMMAND_FILE_PATH = "post_command.sh"

changed_files = set()
is_live = True
all_files = []

# This function sleeps for 100ms and checks if the file has been modified
def check_files():
    global is_live, changed_files
    while is_live:
        time.sleep(0.1)
        if len(changed_files) > 0:
            print("[Watcher] Files Modified: ", changed_files)
            execute()
            changed_files.clear()

def execute():
    command = ""
    with open(COMMAND_FILE_PATH, "r") as f:
        command = f.read()
    print("[Watcher] Command:", command)

    post_command = ""
    with open(POST_COMMAND_FILE_PATH, "r") as f:
        post_command = f.read()
    print("[Watcher] Post Command:", post_command)

    os.chdir(PARENT_FOLDER)

    result = subprocess.run(['bash', "-c", command], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    if (result.returncode == 0):
        print("[Watcher] Command Executed Successfully")
        code_output = subprocess.run(['bash', '-c', post_command], universal_newlines=True)
        if code_output.returncode == 0:
            print("\n[Watcher] Exited Successfully")
        else:
            print(f"\n[Watcher] BAD EXIT: {code_output.returncode}")
    else:
        print(result.returncode)

    os.chdir(CURRENT_DIR)

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path in all_files and not event.is_directory:
            changed_files.add(event.src_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Watcher",
                            description="Watchs a bunch of files to execute commands after the files have changes.",
                            epilog="Note: The prorcess is invoked after at least one of the files has changed.")
    parser.add_argument('-p', '--parent_folder', default='.', help="The parent folder where the files are located. Default is the current folder.")

    args = parser.parse_args()
    PARENT_FOLDER = args.parent_folder

    FILE_LIST_PATH = os.path.join(PARENT_FOLDER, FILE_LIST_PATH)
    COMMAND_FILE_PATH = os.path.join(PARENT_FOLDER, COMMAND_FILE_PATH)
    POST_COMMAND_FILE_PATH = os.path.join(PARENT_FOLDER, POST_COMMAND_FILE_PATH)

    print("PARENT_FOLDER: ", PARENT_FOLDER)
    print("FILE_LIST_PATH: ", FILE_LIST_PATH)
    print("COMMAND_FILE_PATH: ", COMMAND_FILE_PATH)
    print("POST_COMMAND_FILE_PATH: ", POST_COMMAND_FILE_PATH)

    def check_file_found(file):
        if not os.path.exists(file):
            print("Failed to find: ", file)
            exit(1)

    check_file_found(FILE_LIST_PATH)
    check_file_found(COMMAND_FILE_PATH)
    check_file_found(POST_COMMAND_FILE_PATH)

    with open(FILE_LIST_PATH, "r") as f:
        s = f.read()
        all_files = s.split("\n")
        all_files = [os.path.join(PARENT_FOLDER, x) for x in all_files]

    print("[Watcher] Watching Files: ", all_files)

    observer = Observer()
    event_handler = MyHandler()
    observer.schedule(event_handler, path=PARENT_FOLDER, recursive=False)
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
