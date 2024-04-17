# WalterParse - an easy-to-use command line parser
Converts intuitive command line parameters to a different format.

**NOTE: This project is a work in progress and currently does not support a lot.**

## Usage

Placing the bash file and python file in the `bin/` folder allows for usage in any folder. 

### Configuring the file 

A file called `wconfig` must be present in the working directory for WalterParse to work.

For the program to function correctly, `wconfig` must be of the following format:

`wconfig`:

````
./<executable>

-<m> <type> <comment>
-<n> ...

=x -<m> <data> -<n> <data>
=y ...
````

Where:
- `./<executable>` is the path to the executable to be called.
- `-<n>` is the flag for data in command line argument
- `<type>` is the expected type of data following flag `-<n>`.
- `<message>` contains information about flag `-<n>`.
- `=x` is an optional shortcut allowing for quick access of program.

### Calling the program

WalterParse can be called using `wp ...` if stored in `bin/` or `./wp.py ...` if stored in working directory. If called using only `wp`, all flags are printed with information.

When calling with command line parameters, it must be of the form `wp -m <data_m> -n <data_n>`, where the data belonging to the flag must be of the correct type and immediately following the flag.

When calling with a shortcut, it must be of the form `wp =x`.

## to be implemented:
- Default values
- Define some flags, rest default
- Shortcut but also define only some flags
- Check for duplicate flags and shortcuts
- Order flags to prevent linear search