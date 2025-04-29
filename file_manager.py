import pickle


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
        self.open_file = None

    def openFile(self, fname, mode):
        if fname not in self.current_dir:
            raise FileNotFoundError(f"File {fname} not found")
        self.open_file = self.current_dir[fname].open(mode)

    def closeFile(self):
        if self.open_file is None:
            raise PermissionError("No file is open.")
        self.open_file = None

    def readFile(self, fname, start=0, size=None):
        if fname not in self.current_dir:
            raise FileNotFoundError(f"File {fname} not found")
        self.open_file = self.current_dir[fname].open("r")
        print("Reading file:")
        print(self.open_file.read_from_file(start, size))
        self.closeFile()

    def writeFile(self, text, write_at):
        if self.open_file is None:
            raise PermissionError("No file is open.")
        self.open_file.write_to_file(text, write_at)

    def appendFile(self, text):
        if self.open_file is None:
            raise PermissionError("No file is open.")
        self.open_file.append_to_file(text)

    def moveFile(self, fname, start, size, target):
        if fname not in self.current_dir:
            raise FileNotFoundError(f"File {fname} not found")
        self.open_file = self.current_dir[fname].open("w")
        self.open_file.move_within_file(start, size, target)
        self.closeFile()

    def truncateFile(self, fname, size):
        if fname not in self.current_dir:
            raise FileNotFoundError(f"File {fname} not found")
        self.open_file = self.current_dir[fname].open("w")
        self.open_file.truncate_file(size)
        self.closeFile()

    def create(self, fname):
        if fname in self.current_dir:
            raise FileExistsError(f"File {fname} already exists")
        self.current_dir[fname] = FileObject(fname)
        print(f"File {fname} created successfully")

    def delete(self, fname):
        if fname not in self.current_dir:
            raise FileNotFoundError(f"File {fname} not found")
        del self.current_dir[fname]
        print(f"File {fname} deleted successfully")

    def mkDir(self, dir_name):
        if dir_name in self.current_dir:
            raise FileExistsError(f"Directory {dir_name} already exists")
        self.current_dir[dir_name] = {}
        print(f"Directory {dir_name} created successfully")

    def chDir(self, dir_name):
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
            print("Directory not found.")

    def show_memory_map(self):
        print("\nMemory Map:")
        self._printMemoryMap(self.root, "")

    def _getDirFromPath(self, path):
        current_dir = self.root
        for dir_name in path.strip("/").split("/"):
            current_dir = current_dir[dir_name]
        return current_dir

    def listDir(self):
        print("\nCurrent Directory:")
        for name, obj in self.current_dir.items():
            if isinstance(obj, FileObject):
                print(f"- {name} ({obj.size} bytes)")
            else:
                print(f"- {name}/")

    def move(self, source, destination):
        if source not in self.current_dir.keys():
            raise FileNotFoundError(f"File {source} not found")
        if destination in self.current_dir.keys():
            raise FileExistsError(f"File {destination} already exists")
        self.current_dir[destination] = self.current_dir[source]
        del self.current_dir[source]
        print(f"File {source} moved to {destination} successfully")

    def memoryMap(self):
        print("\nMemory Map:")
        self._printMemoryMap(self.root, "")

    def save_to_disk(self, filename="sample.dat"):
        """Saves the current file structure to a .dat file using pickle."""
        with open(filename, "wb") as f:
            pickle.dump(self, f)
        print(f"File system saved to {filename}")

    def load_from_disk(self, filename="sample.dat"):
        """Loads the file structure from a .dat file using pickle."""
        try:
            with open(filename, "rb") as f:
                loaded_fs = pickle.load(f)
                self.root = loaded_fs.root
                self.current_dir = loaded_fs.current_dir
                self.current_path = loaded_fs.current_path
                self.open_file = loaded_fs.open_file
            print(f"File system loaded from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with a new file system.")

    def _printMemoryMap(self, directory=None, indent=""):
        for name, obj in directory.items():
            if isinstance(obj, FileObject):
                print(f"{indent}- {name} ({obj.size} bytes)")
            else:
                print(f"{indent}- {name}/")
                self._printMemoryMap(obj, indent + "    ")
