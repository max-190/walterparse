# WalterParse - an easy-to-use command line parser
Converts intuitive command line parameters to a different format.

**NOTE: This project is a work in progress and currently does not support a lot.**

## Usage

Place the bash file and python file in the `~/.local/bin`.
Use `chmod +x wp` to make it an executable.

### Configuring the file 

A file called `wconfig` must be present in the working directory for WalterParse to work.

For the program to function correctly, `wconfig` must be of the following format:

`wconfig`:

````
./<executable>

-<m> <type> <comment>
-<n> ...

> -m <data> -n <data>

=x -<m> <data> -<n> <data>
=y ...
````

Where:
- `./<executable>` is the path to the executable to be called.
- `-<n>` is the flag for data in command line argument
- `<type>` is the expected type of data following flag `-<n>`.
- `<message>` contains information about flag `-<n>`.
- `>` gives a default call.
- `=x` is an optional shortcut allowing for quick access of program.

### Calling the program

WalterParse can be called using `wp ...` if stored in `~/.local/bin/` or `./wp.py ...` if stored in working directory.

WalterParse has several functionalities.

## to be implemented:
- Default values
- Define some flags, rest default
- Shortcut but also define only some flags
- Check for duplicate flags and shortcuts
- Order flags to prevent linear search