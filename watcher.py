from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import PIPE

import threading, os, time, subprocess, argparse

VERSION = 'v1.0.0'

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_FOLDER = "."
FILE_LIST_PATH = "files.txt"
COMMAND_FILE_PATH = "command.sh"
TERMINAL = 'bash'
TRACKED_FILES = []

is_live = False
changed_files = set()

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

    os.chdir(PARENT_FOLDER)

    result = subprocess.run(['bash', "-c", command], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    if (result.returncode == 0):
        print("[Watcher] Command Executed Successfully")
    else:
        print(result.returncode)

    os.chdir(CURRENT_DIR)

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path in TRACKED_FILES and not event.is_directory:
            changed_files.add(event.src_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Watcher",
                            description="Watches a bunch of files to execute commands after the files have changes.",
                            epilog="Note: The process is invoked after at least one of the files has changed.")
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {VERSION}')
    parser.add_argument('-p', '--parent_folder', default='.', help="The parent folder where the files are located. Default is the current folder.")
    parser.add_argument('-f', '--file_list', nargs='+', help="The list of files to watch. Default is the files in the files.txt", default=[])
    parser.add_argument('-c', '--command_file', default='command.sh', help="The file containing the command to execute. Default is command.sh")
    parser.add_argument('-t', '--terminal', default='bash', help="The terminal to use to execute the command. Default is bash.")
    parser.add_argument('-r', '--recursive', action='store_true', help="Watch the files recursively. Default is False.")

    args = parser.parse_args()
    PARENT_FOLDER = args.parent_folder
    TRACKED_FILES = args.file_list
    TRACKED_FILES = [os.path.join(PARENT_FOLDER, x) for x in TRACKED_FILES]
    COMMAND_FILE_PATH = args.command_file
    TERMINAL = args.terminal

    recursive_watch = args.recursive

    FILE_LIST_PATH = os.path.join(PARENT_FOLDER, FILE_LIST_PATH)
    COMMAND_FILE_PATH = os.path.join(PARENT_FOLDER, COMMAND_FILE_PATH)

    print("PARENT_FOLDER: ", PARENT_FOLDER)
    if args.file_list != []:
        print("FILE_LIST_PATH: ", FILE_LIST_PATH)
    print("COMMAND_FILE_PATH: ", COMMAND_FILE_PATH)

    def check_file_found(file):
        if not os.path.exists(file):
            print("Failed to find: ", file)
            exit(1)

    if TRACKED_FILES == []:
        check_file_found(FILE_LIST_PATH)
        with open(FILE_LIST_PATH, "r") as f:
            s = f.read()
            TRACKED_FILES = s.split("\n")
            TRACKED_FILES = [os.path.join(PARENT_FOLDER, x) for x in TRACKED_FILES]
    check_file_found(COMMAND_FILE_PATH)

    print("[Watcher] Watching Files: ", TRACKED_FILES)

    observer = Observer()
    event_handler = MyHandler()
    observer.schedule(event_handler, path=PARENT_FOLDER, recursive=recursive_watch)
    observer.start()

    # start the thread
    thread = threading.Thread(target=check_files)
    thread.start()
    is_live = True
    try:
        while is_live:
            pass
    except KeyboardInterrupt:
        is_live = False
        observer.stop()

    observer.join()
    thread.join()
