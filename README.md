# Watcher

Simple file watcher that uses watchdog library and subprocess to help with random development projects I have.

I normally use it to compile c/c++ files quickly and test them fast by simply saving the source file.

## Example

I have added a simple example in [the example](./example) directory.

You will find that you need to add 2 files:

1. files.txt -> Contains all the files that you want the watcher to watch for modifications
2. command.sh -> Contains the first command to do once the modification happens.

### Usage

```
usage: Watcher [-h] [-v] [-p PARENT_FOLDER] [-f FILE_LIST [FILE_LIST ...]] [-c COMMAND_FILE] [-t TERMINAL] [-r]

Watches a bunch of files to execute commands after the files have changes.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -p PARENT_FOLDER, --parent_folder PARENT_FOLDER
                        The parent folder where the files are located. Default is the current folder.
  -f FILE_LIST [FILE_LIST ...], --file_list FILE_LIST [FILE_LIST ...]
                        The list of files to watch. Default is the files in the files.txt
  -c COMMAND_FILE, --command_file COMMAND_FILE
                        The file containing the command to execute. Default is command.sh
  -t TERMINAL, --terminal TERMINAL
                        The terminal to use to execute the command. Default is bash.
  -r, --recursive       Watch the files recursively. Default is False.

Note: The process is invoked after at least one of the files has changed.
```
