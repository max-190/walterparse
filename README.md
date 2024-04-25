# WalterParse - an easy-to-use command line parser
Converts intuitive command line parameters to a specified format.

## Installing

To use WalterParse anywhere, place the `wp` file in `~/.local/bin` or any other directory that is in your `$PATH` environment table. Make sure to do `chmod +x wp` to give WalterParse execution rights.

## Configuring the file 

A file called `wconfig` must be present in the working directory for WalterParse to work.

An example of a correct `wconfig` file should be included with the Git repository. The file should maintain the following structure:

`wconfig`:

````
./<executable>

mode = <mode>

-<m> <m_type> <m_comment>
-<n> <n_type> <n_comment>
-<o> ...

> -<m> <m_data> -<n> <n_data>

=x -<m> <m_data> -<n> <n_data>
=y ...
````

The definition of each part of the `wconfig` file is described below.

### `./<executable>`
The executable that is called when WalterParse is used.

### `mode = <mode>`
The format WalterParse maintains when calling the executable. There are two different modes:
- `strict`: 
    - Only the data of the flags will be passed to the executable. The data is ordered in the same order as the flags are defined in `wconfig`. For example, the default call when using the `wconfig` file included with this repository is:  
    `./test "Hi there!" 1`
    - The default call in the `wconfig` file must assign a value for every defined flag.
    - Every flag must come with a value, that is, no flag can take `None` as a value.
- `lax`:
    - The flags including the data will be passed to the executable. The data is ordered in the same order as the flags are defined in `wconfig`. For example, the default call when using the `wconfig` file included with this repository is:  
    `./test -m "Hi there!" -n 1`
    - The default call in the `wconfig` file may contain less flags than the total number of flags defined.
    - `None`-flags are supported: you can pass flags to the executable that do not bring data with it.

### `-<m> <m_type> <m_comment>`
Definition of the flags. The flags must be of the following form:
- `-<m>`: Name of the flag. Must start with a `-`, followed by one or more characters. Using two dashes before a multi-character flag is optional.
- `<m_type>`: Type of data expected to come with the flag. Supported types are:
    - Integers. Use `int` or `integer`.
    - Floats. Use `float` or `double`.
    - Strings, must be enclosed in quotation marks. Use `str` or `string`.
    - None, for flags that do not come with any data. Use `none` or `None`.
- `<m_comment>`: Information about the flag. Must be enclosed in quotation marks. Not adding a comment will result in an exception; use `""` if no comment is desired.

### `> -<m> <m_data> -<n> <n_data>`
Default values when calling the executable. When `mode = strict`, default call must contain data for every defined flag. When `mode = lax`, zero or more flags may be defined.

When WalterParse is called with no parameters, the default call is passed to the executable.

When WalterParse is called with one or more flags, these overwrite those defined in the default call.

For example, running  
`wp -n 5`  
when using the `wconfig` file included with this repository, the resulting call will use the string `"Hi there!"` as defined in the default call since this has not been overwritten, and this message will be repeated five times, since the `-n 5` overwrites the `-n 1` defined in the default call.

Note that a default call can only be defined once.

### `=x -<m> <m_data> -<n> <n_data>`
Shortcut call. When WalterParse is called followed by a shortcut (for example, `=x`), the flag values given in the shortcut definition overwrite those of the default call.

Additionally, when WalterParse is called with a shortcut and one or more flag values, these overwrite the shortcut values, which in turn overwrite the default values.

For example, running  
`wp =hw -m "What is up?"`  
when using the `wconfig` file included with this repository, the resulting call will use the string `"What is up?"` since it overwrites the string defined in the shortcut definition, and it will be repeated five times, as defined in the same definition.

You can define multiple shortcuts, but if multiple shortcuts have the same name, only the first one will be used.

## Additional functionalities
When running the command  
`wp ?`  
the program will display some information about the program that it gathered from the `wconfig` file.