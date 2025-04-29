# File Management System - User Guide

## Overview
This application provides a command-line interface for managing files and directories in a virtual file system. It supports basic file operations, directory navigation, and persistence.

## Getting Started
Run the application by executing the following commands
```bash
python main.py
```

## Command Reference

### File Operations
| Command | Syntax | Description |
|---------|--------|-------------|
| create | `create <filename>` | Creates a new empty file |
| delete | `delete <filename>` | Deletes a file |
| open | `open <filename> <mode>` | Opens a file (modes: 'r'=read, 'w'=write, 'a'=append) |
| close | `close` | Closes the currently open file |
| read | `read <filename>` or `read <filename> <start> <size>` | Reads entire file or specific portion |
| write | `write "<text>" <position>` | Writes text at specified position in the currently opened file |
| append | `append "<text>"` | Appends text to currently opened file |
| moveFile | `moveFile <filename> <start> <size> <target>` | Moves content within file |
| truncate | `truncate <filename> <size>` | Truncates file to specified size |

### Directory Operations
| Command | Syntax | Description |
|---------|--------|-------------|
| mkDir | `mkDir <dirname>` | Creates a new directory |
| chDir | `chDir <dirname>` or `chDir ..` | Changes directory (use `..` for parent) |
| list | `list` | Lists contents of current directory |
| move | `move <oldname> <newname>` | Renames a file or directory |

### System Operations
| Command | Syntax | Description |
|---------|--------|-------------|
| memory | `memory` | Shows memory map of entire file system |
| exit | `exit` | Saves changes and exits the program |

## Examples

### 1. Create and write to a file:
```bash
create report.txt              # create a file "report.txt"
open report.txt w              # open "report.txt" in write mode
write "Annual Report 2023" 0   # write the text at the beginning of the file
append "\nQ1 Results: $1.2M"   # append new text to the end of the file
close                          # close the currently open file
```

### 2. Directory operations:
```bash
mkDir Projects                 # create a directory named "Projects"
chDir Projects                 # change into the "Projects" directory
create README.md               # create a file named "README.md" in "Projects"
open README.md w               # open "README.md" in write mode
write "# Project Documentation" 0  # write a heading at the start of the file
close                          # close the currently open file
chDir ..                       # move back to the parent directory
```

### 3. Advanced file operations:
```bash
open data.txt w                # open "data.txt" in write mode
write "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 0  # write the alphabet at the start
moveFile data.txt 5 10 0       # move 10 characters from position 5 to position 0
read data.txt                  # display the contents of "data.txt"
truncate data.txt 15           # truncate the file to 15 characters
close                          # close the currently open file
```

### 4. System inspection:
```bash
list                           # list files and directories in the current directory
memory                         # show the memory map of the file system
exit                           # save changes and exit the program
```