import pickle
import threading


class FileObject:
    def __init__(self, name):
        self.name = name
        self.size = 0
        self.content = ""

    def open(self, mode):
        if mode not in ["r", "w", "a"]:
            raise ValueError("Mode must be 'r', 'w', or 'a'.")
        self.mode = mode
        return self

    def close(self):
        self.mode = None
        return self

    def append_to_file(self, text):
        if self.mode != "a":
            raise PermissionError("File must be opened in append mode.")
        self.content += text
        self.size = len(self.content)

    def write_to_file(self, text, write_at):
        if self.mode != "w":
            raise PermissionError("File must be opened in write mode.")
        self.content = self.content[:write_at] + text + self.content[write_at:]
        self.size = len(self.content)

    def read_from_file(self, start=0, size=None):
        if self.mode != "r":
            raise PermissionError("File must be opened in read mode.")
        if size is None:
            return self.content[start:]
        return self.content[start : start + size]

    def move_within_file(self, start, size, target):
        if self.mode != "w":
            raise PermissionError("File must be opened in write mode.")
        content_to_move = self.content[start : start + size]
        self.content = (
            self.content[:start] + self.content[start + size :] + content_to_move
            if target > len(self.content)
            else self.content[:target] + content_to_move + self.content[target:]
        )

    def truncate_file(self, size):
        if self.mode != "w":
            raise PermissionError("File must be opened in write mode.")
        self.content = self.content[:size]
        self.size = len(self.content)


class FileSystem:
    def __init__(self):
        self.root = {}
        self.current_dir = self.root
        self.current_path = "/"
        self.open_file: FileObject = None
        self.lock = threading.RLock()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["lock"]  # Remove lock from state
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = threading.RLock()  # Recreate lock after loading

    def _acquire_lock(self):
        self.lock.acquire()

    def _release_lock(self):
        self.lock.release()

    def openFile(self, fname, mode):
        with self.lock:
            if fname not in self.current_dir:
                raise FileNotFoundError(f"File {fname} not found")
            self.open_file = self.current_dir[fname].open(mode)
            return f"File {fname} opened successfully in {mode} mode"

    def closeFile(self):
        with self.lock:
            if self.open_file is None:
                raise PermissionError("No file is open.")
            name = self.open_file.name
            self.open_file = None
            return f"File {name} closed successfully"

    def readFile(self, fname, start=0, size=None):
        with self.lock:
            if fname not in self.current_dir:
                raise FileNotFoundError(f"File {fname} not found")
            self.open_file = self.current_dir[fname].open("r")
            print("Reading file:")
            content = self.open_file.read_from_file(start, size)
            print(content)
            self.closeFile()
            return f"Content from {fname}: {content}"

    def writeFile(self, text, write_at):
        with self.lock:
            if self.open_file is None:
                raise PermissionError("No file is open.")
            self.open_file.write_to_file(text, write_at)
            return f"File {self.open_file.name} written successfully at {write_at}"

    def appendFile(self, text):
        with self.lock:
            if self.open_file is None:
                raise PermissionError("No file is open.")
            self.open_file.append_to_file(text)
            return f"File {self.open_file.name} appended successfully"

    def moveFile(self, fname, start, size, target):
        with self.lock:
            if fname not in self.current_dir:
                raise FileNotFoundError(f"File {fname} not found")
            self.open_file = self.current_dir[fname].open("w")
            self.open_file.move_within_file(start, size, target)
            self.closeFile()
            return f"File {fname} moved successfully within the file"

    def truncateFile(self, fname, size):
        with self.lock:
            if fname not in self.current_dir:
                raise FileNotFoundError(f"File {fname} not found")
            self.open_file = self.current_dir[fname].open("w")
            self.open_file.truncate_file(size)
            self.closeFile()
            return f"File {fname} truncated successfully to {size} bytes"

    def create(self, fname):
        with self.lock:
            if fname in self.current_dir:
                raise FileExistsError(f"File {fname} already exists")
            self.current_dir[fname] = FileObject(fname)
            return f"File {fname} created successfully"

    def delete(self, fname):
        with self.lock:
            if fname not in self.current_dir:
                raise FileNotFoundError(f"File {fname} not found")
            del self.current_dir[fname]
            return f"File {fname} deleted successfully"

    def mkDir(self, dir_name):
        with self.lock:
            if dir_name in self.current_dir:
                raise FileExistsError(f"Directory {dir_name} already exists")
            self.current_dir[dir_name] = {}
            return f"Directory {dir_name} created successfully"

    def chDir(self, dir_name):
        with self.lock:
            if dir_name == "..":
                if self.current_path != "/":
                    self.current_path = "/".join(
                        self.current_path.strip("/").split("/")[:-1]
                    )
                if self.current_path == "":
                    self.current_path = "/"
                    self.current_dir = self.root
                else:
                    self.current_dir = self._getDirFromPath(self.current_path)

            elif dir_name in self.current_dir and isinstance(
                self.current_dir[dir_name], dict
            ):
                self.current_dir = self.current_dir[dir_name]
                self.current_path += dir_name + "/"
            else:
                return "Directory not found."
            return f"Directory {dir_name} changed successfully"

    def show_memory_map(self):
        with self.lock:
            print("\nMemory Map:")
            self._printMemoryMap(self.root, "")
            return "Memory map printed successfully"

    def _getDirFromPath(self, path):
        current_dir = self.root
        for dir_name in path.strip("/").split("/"):
            current_dir = current_dir[dir_name]
        return current_dir

    def listDir(self):
        with self.lock:
            print("\nCurrent Directory:")
            for name, obj in self.current_dir.items():
                if isinstance(obj, FileObject):
                    print(f"- {name} ({obj.size} bytes)")
                else:
                    print(f"- {name}/")
            return "Directory list printed successfully"

    def move(self, source, destination):
        with self.lock:
            if source not in self.current_dir.keys():
                raise FileNotFoundError(f"File {source} not found")
            if destination in self.current_dir.keys():
                raise FileExistsError(f"File {destination} already exists")
            self.current_dir[destination] = self.current_dir[source]
            del self.current_dir[source]
            return f"File {source} moved to {destination} successfully"

    def memoryMap(self):
        with self.lock:
            print("\nMemory Map:")
            self._printMemoryMap(self.root, "")
            return "Memory map printed successfully"

    def save_to_disk(self, filename="sample.dat"):
        with open(filename, "wb") as f:
            pickle.dump(self, f)
        return f"File system saved to {filename}"

    def load_from_disk(self, filename="sample.dat"):
        try:
            with open(filename, "rb") as f:
                loaded_fs = pickle.load(f)
                self.root = loaded_fs.root
                self.current_dir = loaded_fs.current_dir
                self.current_path = loaded_fs.current_path
                self.open_file = loaded_fs.open_file
            return f"File system loaded from {filename}"
        except FileNotFoundError:
            return f"File {filename} not found. Starting with a new file system."

    def _printMemoryMap(self, directory=None, indent=""):
        for name, obj in directory.items():
            if isinstance(obj, FileObject):
                print(f"{indent}- {name} ({obj.size} bytes)")
            else:
                print(f"{indent}- {name}/")
                self._printMemoryMap(obj, indent + "    ")
