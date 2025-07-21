from apps import CalculatorApp, NotesApp, EchoApp

class Store:
    def __init__(self):
        self.available_apps = {
            "calc": CalculatorApp,
            "notes": NotesApp,
            "echo": EchoApp,
        }
        self.installed_apps = {}

    def list_store_apps(self):
        print("Available apps in FishyOS Store:")
        for app in self.available_apps:
            status = "Installed" if app in self.installed_apps else "Not installed"
            print(f" - {app} [{status}]")

    def install(self, app_name):
        if app_name in self.installed_apps:
            print(f"'{app_name}' is already installed.")
            return
        if app_name not in self.available_apps:
            print(f"App '{app_name}' not found in the store.")
            return
        self.installed_apps[app_name] = self.available_apps[app_name]()
        print(f"Installed '{app_name}'.")

    def uninstall(self, app_name):
        if app_name not in self.installed_apps:
            print(f"App '{app_name}' is not installed.")
            return
        del self.installed_apps[app_name]
        print(f"Uninstalled '{app_name}'.")

    def list_installed(self):
        if not self.installed_apps:
            print("No apps installed.")
            return
        print("Installed apps:")
        for app in self.installed_apps:
            print(f" - {app}")

    def run_app(self, app_name):
        if app_name not in self.installed_apps:
            print(f"App '{app_name}' is not installed.")
            return
        print(f"Launching '{app_name}'... (type 'exit' to return)")
        self.installed_apps[app_name].run()
