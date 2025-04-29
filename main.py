from file_manager import FileSystem


def main():
    fs = FileSystem()
    fs.load_from_disk()

    while True:
        print(f"\nCurrent Path: {fs.current_path}")
        print(f"Current opened file: {fs.open_file.name}") if fs.open_file else None
        command = input("Enter command: ").strip()
        if command == "exit":
            fs.save_to_disk()
            break

        args = []

        # get the text between ""
        if '"' in command:
            text = command.split('"')[1]
            args.append(command.split()[0])
            args.append(text)
            args.append(command.split()[-1])
        else:
            args = command.split()

        try:
            if args[0] == "create":
                fs.create(args[1])
            elif args[0] == "delete":
                fs.delete(args[1])
            elif args[0] == "mkDir":
                fs.mkDir(args[1])
            elif args[0] == "chDir":
                fs.chDir(args[1])
            elif args[0] == "list":
                fs.listDir()
            elif args[0] == "move":
                fs.move(args[1], args[2])
            elif args[0] == "open":
                fs.openFile(args[1], args[2])
            elif args[0] == "close":
                fs.closeFile()
            elif args[0] == "read":
                if len(args) == 2:
                    fs.readFile(args[1])
                else:
                    fs.readFile(args[1], int(args[2]), int(args[3]))
            elif args[0] == "write":
                fs.writeFile(args[1], int(args[2]))
            elif args[0] == "append":
                fs.appendFile(args[1])
            elif args[0] == "moveFile":
                fs.moveFile(args[1], int(args[2]), int(args[3]), int(args[4]))
            elif args[0] == "truncate":
                fs.truncateFile(args[1], int(args[2]))
            elif args[0] == "memory":
                fs.memoryMap()
            else:
                print("Invalid command")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
