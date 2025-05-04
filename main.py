import threading
import sys
import time
from file_manager import FileSystem


class ThreadTask(threading.Thread):
    def __init__(self, thread_number, file_system: FileSystem):
        threading.Thread.__init__(self)
        self.thread_number = thread_number
        self.file_system = file_system
        self.input_file = f"input_thread{thread_number}.txt"
        self.output_file = f"output_thread{thread_number}.txt"

    def run(self):
        with open(self.input_file, "r") as file:
            commands = file.readlines()

        with open(self.output_file, "w") as output:
            for command in commands:
                result = self.execute_command(command.strip())
                print(result)
                output.write(result + "\n")

    def execute_command(self, command):

        parts = []
        if '"' in command:
            text = command.split('"')[1]
            parts.append(command.split()[0])
            parts.append(text)
            parts.append(command.split()[-1])
        else:
            parts = command.split()
        cmd_name = parts[0]

        try:
            if cmd_name == "create":
                return self.file_system.create(parts[1])
            elif cmd_name == "delete":
                return self.file_system.delete(parts[1])
            elif cmd_name == "mkDir":
                return self.file_system.mkDir(parts[1])
            elif cmd_name == "chDir":
                return self.file_system.chDir(parts[1])
            elif cmd_name == "move":
                return self.file_system.move(parts[1], parts[2])
            elif cmd_name == "open":
                return self.file_system.openFile(parts[1], parts[2])
            elif cmd_name == "close":
                return self.file_system.closeFile()
            elif cmd_name == "write":
                return self.file_system.writeFile(parts[1], int(parts[2]))
            elif cmd_name == "read":
                if len(parts) == 2:
                    return self.file_system.readFile(parts[1])
                else:
                    return self.file_system.readFile(
                        parts[1], int(parts[2]), int(parts[3])
                    )
            elif cmd_name == "append":
                return self.file_system.appendFile(parts[1])
            elif cmd_name == "moveFile":
                return self.file_system.moveFile(
                    parts[1], int(parts[2]), int(parts[3]), int(parts[4])
                )
            elif cmd_name == "truncate":
                return self.file_system.truncateFile(parts[1], int(parts[2]))
            elif cmd_name == "list":
                return self.file_system.listDir()
            elif cmd_name == "memory":
                return self.file_system.memoryMap()
            else:
                return "Unknown command"
        except Exception as e:
            print(f"Error executing command: {e}")
            return f"Error {e}"


def main():

    k = int(sys.argv[1])
    fs = FileSystem()

    print(fs.load_from_disk())

    threads = []

    for i in range(1, k + 1):
        thread = ThreadTask(i, fs)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(fs.save_to_disk())

    print("All threads completed")


if __name__ == "__main__":
    main()
