# Watcher

Simple file watcher that uses watchdog library and subprocess to help with random development projects I have.

I normally use it to compile c/c++ files quickly and test them fast by simply saving the source file.

## Example

I have added a simple example in [the example](./example) directory.

You will find that you need to add 3 files:

1. files.txt -> Contains all the files that you want the watcher to watch for modifications
2. command.sh -> Contains the first command to do once the modification happens.
3. post_command.sh -> A secondary command to do after the first command.sh is executed (It's almost compleletly redundant since you can append it to the first file 🤷‍♂️)
