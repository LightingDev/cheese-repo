from store import Store

class FishyOS:
    def __init__(self):
        self.store = Store()

    def start(self):
        self.print_welcome()
        while True:
            cmd = input("C:\\FishyOS> ").strip().lower()
            if not cmd:
                continue
            self.handle_command(cmd)

    def print_welcome(self):
        print("Welcome to FishyOS v0.1")
        print("Type 'help' for a list of commands.\n")

    def handle_command(self, cmd):
        parts = cmd.split()
        command = parts[0]

        if command == "help":
            self.cmd_help()
        elif command == "apps":
            self.store.list_installed()
        elif command == "store":
            self.store.list_store_apps()
        elif command == "install":
            if len(parts) < 2:
                print("Usage: install <appname>")
            else:
                self.store.install(parts[1])
        elif command == "uninstall":
            if len(parts) < 2:
                print("Usage: uninstall <appname>")
            else:
                self.store.uninstall(parts[1])
        elif command == "run":
            if len(parts) < 2:
                print("Usage: run <appname>")
            else:
                self.store.run_app(parts[1])
        elif command == "exit":
            print("Goodbye!")
            exit()
        else:
            print(f"Unknown command: {command}")

    def cmd_help(self):
        print("Available commands:")
        print(" help          - Show this help message")
        print(" apps          - List installed apps")
        print(" store         - Show available apps in App Store")
        print(" install <app> - Install an app from App Store")
        print(" uninstall <app> - Uninstall an installed app")
        print(" run <app>     - Run an installed app")
        print(" exit          - Exit FishyOS")


if __name__ == "__main__":
    FishyOS().start()
