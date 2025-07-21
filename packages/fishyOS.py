import sys

class FishyOS:
    def __init__(self):
        self.installed_apps = {}
        self.available_apps = {
            "calc": self.calc_app,
            "notes": self.notes_app,
            "echo": self.echo_app,
        }
        self.notes_storage = []

    def start(self):
        self.print_welcome()
        while True:
            try:
                cmd = input("C:\\FishyOS> ").strip().lower()
                if not cmd:
                    continue
                self.handle_command(cmd)
            except (KeyboardInterrupt, EOFError):
                print("\nExiting FishyOS...")
                sys.exit()

    def print_welcome(self):
        print("Welcome to FishyOS v0.1")
        print("Type 'help' for a list of commands.\n")

    def handle_command(self, cmd):
        parts = cmd.split()
        command = parts[0]

        if command == "help":
            self.cmd_help()
        elif command == "apps":
            self.cmd_apps()
        elif command == "store":
            self.cmd_store()
        elif command == "install":
            if len(parts) < 2:
                print("Usage: install <appname>")
            else:
                self.cmd_install(parts[1])
        elif command == "uninstall":
            if len(parts) < 2:
                print("Usage: uninstall <appname>")
            else:
                self.cmd_uninstall(parts[1])
        elif command == "run":
            if len(parts) < 2:
                print("Usage: run <appname>")
            else:
                self.cmd_run(parts[1])
        elif command == "exit":
            print("Goodbye!")
            sys.exit()
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

    def cmd_apps(self):
        if not self.installed_apps:
            print("No apps installed.")
            return
        print("Installed apps:")
        for app in self.installed_apps:
            print(f" - {app}")

    def cmd_store(self):
        print("Available apps in FishyOS Store:")
        for app in self.available_apps:
            status = "Installed" if app in self.installed_apps else "Not installed"
            print(f" - {app} [{status}]")

    def cmd_install(self, app):
        if app in self.installed_apps:
            print(f"'{app}' is already installed.")
            return
        if app not in self.available_apps:
            print(f"App '{app}' not found in the store.")
            return
        self.installed_apps[app] = self.available_apps[app]
        print(f"Installed '{app}'.")

    def cmd_uninstall(self, app):
        if app not in self.installed_apps:
            print(f"App '{app}' is not installed.")
            return
        del self.installed_apps[app]
        print(f"Uninstalled '{app}'.")

    def cmd_run(self, app):
        if app not in self.installed_apps:
            print(f"App '{app}' is not installed.")
            return
        print(f"Launching '{app}'... (type 'exit' to return)")
        self.installed_apps[app]()

    # --- Sample apps below ---

    def calc_app(self):
        print("Simple Calculator - type 'exit' to quit")
        while True:
            expr = input("calc> ").strip()
            if expr.lower() == "exit":
                print("Exiting calculator.")
                break
            try:
                # WARNING: using eval is insecure but fine for demo
                result = eval(expr, {"__builtins__": None}, {})
                print(f"= {result}")
            except Exception as e:
                print(f"Error: {e}")

    def notes_app(self):
        print("Simple Notes - type 'help' for commands, 'exit' to quit")
        while True:
            cmd = input("notes> ").strip()
            if cmd == "exit":
                print("Exiting notes.")
                break
            elif cmd == "help":
                print("Commands: add <text>, list, clear, exit")
            elif cmd.startswith("add "):
                note = cmd[4:].strip()
                self.notes_storage.append(note)
                print("Note added.")
            elif cmd == "list":
                if not self.notes_storage:
                    print("No notes.")
                else:
                    print("Notes:")
                    for i, n in enumerate(self.notes_storage, 1):
                        print(f"{i}. {n}")
            elif cmd == "clear":
                self.notes_storage.clear()
                print("All notes cleared.")
            else:
                print("Unknown notes command. Type 'help'.")

    def echo_app(self):
        print("Echo app - type something and it will repeat it. Type 'exit' to quit.")
        while True:
            line = input("echo> ").strip()
            if line.lower() == "exit":
                print("Exiting echo.")
                break
            print(line)


if __name__ == "__main__":
    os_sim = FishyOS()
    os_sim.start()
