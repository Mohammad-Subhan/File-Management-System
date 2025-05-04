# File Management System (Multithreaded) - User Guide

## Overview
This multithreaded file management system simulates concurrent file operations using a virtual file system stored in sample.dat. It supports simultaneous input through multiple threads, synchronized using semaphores to avoid data races and ensure safe access.

## Getting Started
### Requirements
* Python 3.x
* No external dependencies

### Running the Program
Run the application by executing the following commands
```bash
python main.py <k>
```
Where <k> is the number of threads (e.g., python main.py 3).

Each thread reads from a corresponding file:
* input_thread1.txt
* input_thread2.txt
* ...
* input_thread\<k>.txt

Each thread writes its output to:
* output_thread1.txt
* output_thread2.txt
* ...
* output_thread\<k>.txt

The system persists all changes to sample.dat

## Input File Format
Each input_thread<x>.txt should contain valid commands (one per line) based on the syntax defined below. These commands will be executed sequentially by the corresponding thread

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

### 1. Thread Input Example (input_thread1.txt)
```bash
create log.txt
open log.txt w
write "Log start" 0
append " - More logs"
close
```

## Thread Output
Each command’s output or error is logged into the corresponding output_thread<x>.txt file.

## File Structure
```bash
.
├── sample.dat                # Serialized virtual file system (persistent)
├── main.py                   # Entry point to run threads
├── file_manager.py           # Core logic for file operations
├── input_thread1.txt         # Input for thread 1
├── input_thread2.txt         # Input for thread 2
├── ...                       # More thread inputs
├── output_thread1.txt        # Output from thread 1
├── output_thread2.txt        # Output from thread 2
├── ...                       # More thread outputs
└── guide.md                  # This user guide
```

## Notes
* All threads share the same file system, so file and directory conflicts may occur if not coordinated properly.
* sample.dat is updated after each thread finishes execution.
* Semaphores ensure that concurrent operations do not corrupt file system state.

## Known Limitations
* Commands are assumed to be valid (no deep input validation).
* File names and directory names are case-sensitive