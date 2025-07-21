# ---------------------------------------------------------------------------
# utils.py
# ---------------------------------------------------------------------------
# General helper functions used across FishyOS modules.

# Save as utils.py (separate file) and import in main.py & elsewhere.

import os as _os
import platform as _platform
import ast as _ast
import operator as _op
from typing import Iterable, Sequence


class Utils:
    """Utility helpers for FishyOS.

    Instantiate once (in main.py) and pass around or attach to FishyOS.
    """

    def __init__(self, ansi: bool = False):
        """ansi=True enables ANSI color helpers (off by default for MS‑DOS vibe)."""
        self.ansi = ansi

    # ------------------------------------------------------------------
    def clear_screen(self) -> None:
        # Cross‑platform clear; still prints the classic DOS form when on Windows
        if _platform.system().lower().startswith("win"):
            _os.system("cls")
        else:
            _os.system("clear")

    # ------------------------------------------------------------------
    def color(self, text: str, fg: str = "", bold: bool = False) -> str:
        """Optional ANSI coloring (disabled unless ansi=True)."""
        if not self.ansi or not fg:
            return text
        colors = {
            "red": "31",
            "green": "32",
            "yellow": "33",
            "blue": "34",
            "magenta": "35",
            "cyan": "36",
            "white": "37",
        }
        code = colors.get(fg, "37")
        if bold:
            code = "1;" + code
        return f"\033[{code}m{text}\033[0m"

    # ------------------------------------------------------------------
    def print_table(self, rows: Sequence[Sequence[str]], headers: Sequence[str] | None = None) -> None:
        """Lightweight column table printer."""
        if headers:
            rows = [headers] + list(rows)
        if not rows:
            return
        col_widths = [max(len(str(cell)) for cell in col) for col in zip(*rows)]
        for r_i, row in enumerate(rows):
            line = " ".join(str(cell).ljust(col_widths[c_i]) for c_i, cell in enumerate(row))
            print(line)
            if headers and r_i == 0:
                print("-" * len(line))

    # ------------------------------------------------------------------
    # Safer expression evaluator for calculator (no builtins, limited ops).
    # Use in apps.CalculatorApp by swapping eval() -> utils.safe_eval().
    #
    # Supports: +, -, *, /, //, %, **, parentheses, unary +/-, ints & floats.
    # ------------------------------------------------------------------
    _ALLOWED_BIN_OPS = {
        _ast.Add: _op.add,
        _ast.Sub: _op.sub,
        _ast.Mult: _op.mul,
        _ast.Div: _op.truediv,
        _ast.FloorDiv: _op.floordiv,
        _ast.Mod: _op.mod,
        _ast.Pow: _op.pow,
    }
    _ALLOWED_UNARY_OPS = {
        _ast.UAdd: lambda v: +v,
        _ast.USub: lambda v: -v,
    }

    def safe_eval(self, expr: str) -> float:
        try:
            node = _ast.parse(expr, mode="eval").body
            return self._eval_ast(node)
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")

    def _eval_ast(self, node):  # recursive
        if isinstance(node, _ast.Num):  # Py<3.8 compatibility
            return node.n
        if isinstance(node, _ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, _ast.BinOp):
            op_type = type(node.op)
            if op_type not in self._ALLOWED_BIN_OPS:
                raise ValueError("Operator not allowed")
            left = self._eval_ast(node.left)
            right = self._eval_ast(node.right)
            return self._ALLOWED_BIN_OPS[op_type](left, right)
        if isinstance(node, _ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in self._ALLOWED_UNARY_OPS:
                raise ValueError("Unary operator not allowed")
            val = self._eval_ast(node.operand)
            return self._ALLOWED_UNARY_OPS[op_type](val)
        raise ValueError("Unsupported expression")


# ---------------------------------------------------------------------------
# main.py (UPDATED SNIPPET showing commands + utils wiring)
# ---------------------------------------------------------------------------
# NOTE: Only the relevant parts are shown; merge into your existing main.py.

# main.py
"""FishyOS main launcher (wire up CommandRegistry + Utils)."""

from store import Store
from commands import CommandRegistry, register_builtin_commands
from utils import Utils


class FishyOS:
    version = "0.1"  # bump as you like

    def __init__(self, ansi: bool = False):
        self.store = Store()
        self.utils = Utils(ansi=ansi)
        self.commands = CommandRegistry(self)
        register_builtin_commands(self.commands)

    # --- startup ------------------------------------------------------
    def start(self) -> None:
        self.print_welcome()
        while True:
            try:
                line = input("C:\\FishyOS> ")
            except (KeyboardInterrupt, EOFError):
                print()  # newline after ^C/^D
                line = "exit"
            self.commands.execute(line)

    def print_welcome(self) -> None:
        print("Welcome to FishyOS v" + self.version)
        print("Type 'help' for a list of commands.\n")


if __name__ == "__main__":
    FishyOS().start()

