class CalculatorApp:
    def run(self):
        print("Simple Calculator - type 'exit' to quit")
        while True:
            expr = input("calc> ").strip()
            if expr.lower() == "exit":
                print("Exiting calculator.")
                break
            try:
                result = eval(expr, {"__builtins__": None}, {})
                print(f"= {result}")
            except Exception as e:
                print(f"Error: {e}")

class NotesApp:
    def __init__(self):
        self.notes_storage = []

    def run(self):
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

class EchoApp:
    def run(self):
        print("Echo app - type something and it will repeat it. Type 'exit' to quit.")
        while True:
            line = input("echo> ").strip()
            if line.lower() == "exit":
                print("Exiting echo.")
                break
            print(line)
