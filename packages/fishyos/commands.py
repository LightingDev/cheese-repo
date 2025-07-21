# ---------------------------------------------------------------------------
# commands.py
# ---------------------------------------------------------------------------
# Central registry for FishyOS shell commands. Keeps main.py clean and lets you
# add/override commands without editing the main loop.

# Usage in main.py:
#   from commands import CommandRegistry, register_builtin_commands
#   self.commands = CommandRegistry(self)
#   register_builtin_commands(self.commands)
#   ... later in loop ...
#   self.commands.execute(user_line)

from __future__ import annotations
from typing import Callable, Dict, List, Optional, Tuple, Any


class CommandRegistry:
    """Register and dispatch FishyOS shell commands.

    Each command handler is a callable that accepts `(args: List[str])`.
    The handler can access the FishyOS instance via `self.os`.
    """

    def __init__(self, os_ref: Any):
        self.os = os_ref  # back‑reference to FishyOS instance
        self._commands: Dict[str, Callable[[List[str]], None]] = {}
        self._help: Dict[str, str] = {}
        self._primary_name: Dict[Callable, str] = {}

    # ------------------------------------------------------------------
    def register(
        self,
        name: str,
        func: Callable[[List[str]], None],
        help_text: Optional[str] = None,
        aliases: Optional[List[str]] = None,
    ) -> None:
        name = name.lower()
        self._commands[name] = func
        if help_text is not None:
            self._help[name] = help_text
        self._primary_name[func] = name
        if aliases:
            for a in aliases:
                self._commands[a.lower()] = func

    # ------------------------------------------------------------------
    def unregister(self, name: str) -> None:
        name = name.lower()
        self._commands.pop(name, None)
        self._help.pop(name, None)

    # ------------------------------------------------------------------
    def execute(self, line: str) -> None:
        if not line.strip():
            return
        parts = line.split()
        cmd_name = parts[0].lower()
        args = parts[1:]
        func = self._commands.get(cmd_name)
        if func is None:
            print(f"Unknown command: {cmd_name}. Type 'help' for a list.")
            return
        try:
            func(args)
        except SystemExit:  # allow handlers to raise exit() cleanly
            raise
        except Exception as e:  # catch so shell doesn't crash
            print(f"Command '{cmd_name}' failed: {e}")

    # ------------------------------------------------------------------
    def iter_help(self) -> List[Tuple[str, str]]:
        # Return sorted help lines by command name (primary names only)
        seen = set()
        lines: List[Tuple[str, str]] = []
        for name, func in self._commands.items():
            # Only include each func once (primary name) in help.
            if func in seen:
                continue
            seen.add(func)
            primary = self._primary_name.get(func, name)
            desc = self._help.get(primary, "")
            lines.append((primary, desc))
        lines.sort(key=lambda x: x[0])
        return lines


# ---------------------------------------------------------------------------
# Built‑in command implementations (registered via helper below)
# ---------------------------------------------------------------------------

def register_builtin_commands(reg: CommandRegistry) -> None:
    os_ref = reg.os  # convenience handle
    store = os_ref.store
    utils = os_ref.utils

    # --- help ---------------------------------------------------------
    def _cmd_help(args: List[str]) -> None:
        print("Available commands:")
        for name, desc in reg.iter_help():
            # show aligned 12‑wide names; tweak as needed
            print(f" {name:<12} - {desc}")

    reg.register("help", _cmd_help, "Show this help message", aliases=["?", "h"])

    # --- apps ---------------------------------------------------------
    def _cmd_apps(args: List[str]) -> None:
        store.list_installed()

    reg.register("apps", _cmd_apps, "List installed apps")

    # --- store --------------------------------------------------------
    def _cmd_store(args: List[str]) -> None:
        store.list_store_apps()

    reg.register("store", _cmd_store, "Show available apps in App Store")

    # --- install ------------------------------------------------------
    def _cmd_install(args: List[str]) -> None:
        if not args:
            print("Usage: install <appname>")
            return
        store.install(args[0])

    reg.register("install", _cmd_install, "Install an app from App Store")

    # --- uninstall ----------------------------------------------------
    def _cmd_uninstall(args: List[str]) -> None:
        if not args:
            print("Usage: uninstall <appname>")
            return
        store.uninstall(args[0])

    reg.register("uninstall", _cmd_uninstall, "Uninstall an installed app")

    # --- run ----------------------------------------------------------
    def _cmd_run(args: List[str]) -> None:
        if not args:
            print("Usage: run <appname>")
            return
        store.run_app(args[0])

    reg.register("run", _cmd_run, "Run an installed app")

    # --- cls / clear --------------------------------------------------
    def _cmd_cls(args: List[str]) -> None:
        utils.clear_screen()

    reg.register("cls", _cmd_cls, "Clear the screen", aliases=["clear"])

    # --- ver ----------------------------------------------------------
    def _cmd_ver(args: List[str]) -> None:
        # Version info from FishyOS instance
        print(f"FishyOS version {os_ref.version}")
        print("MS‑DOS style Python shell simulator.")

    reg.register("ver", _cmd_ver, "Show FishyOS version info")

    # --- about --------------------------------------------------------
    def _cmd_about(args: List[str]) -> None:
        print("FishyOS – a playful MS‑DOS style shell written in Python.")
        print("Created by Yixuan (and a helpful AI sidekick).")
        print("Type 'store' to see installable apps.")

    reg.register("about", _cmd_about, "About FishyOS")

    # --- exit ---------------------------------------------------------
    def _cmd_exit(args: List[str]) -> None:
        print("Goodbye!")
        raise SystemExit(0)

    reg.register("exit", _cmd_exit, "Exit FishyOS", aliases=["quit", "q"])

    # ------------------------------------------------------------------
    # You can register *more* commands below. Example skeleton:
    #
    # def _cmd_ping(args):
    #     print("PONG", args)
    # reg.register("ping", _cmd_ping, "Test command")
    #
    # That's it!
    # ------------------------------------------------------------------
