import sys
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.margins import NumberedMargin
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments.lexers.python import PythonLexer
from prompt_toolkit.completion import Completer, Completion
import jedi

# ---------------- File Argument ----------------
if len(sys.argv) > 1:
    filepath = sys.argv[1]
    try:
        with open(filepath, "r") as f:
            initial_text = f.read()
    except FileNotFoundError:
        initial_text = ""
else:
    filepath = None
    initial_text = ""

# ---------------- Jedi Completer ----------------
class JediCompleter(Completer):
    def get_completions(self, document, complete_event):
        code = buffer.text
        try:
            script = jedi.Script(code=code, path=filepath or "temp.py")
            row, col = document.cursor_position_row, document.cursor_position_col
            completions = script.complete(row + 1, col)
            for c in completions:
                yield Completion(c.name, start_position=-len(document.get_word_before_cursor()))
        except Exception:
            return

# ---------------- Buffer ----------------
buffer = Buffer(
    multiline=True,
    completer=JediCompleter(),
    complete_while_typing=True
)
buffer.text = initial_text

# ---------------- Status Bar ----------------
status_bar = Window(
    height=1,
    content=FormattedTextControl(lambda: "Ctrl+S=Save | Ctrl+Q=Exit"),
    style="class:status",
    dont_extend_height=True
)

# ---------------- Key Bindings ----------------
kb = KeyBindings()

@kb.add("c-q")
def exit_(event):
    event.app.exit()

@kb.add("c-s")
def save(event):
    if filepath:
        with open(filepath, "w") as f:
            f.write(buffer.text)
        status_bar.content.text = f"Saved to {filepath}"
    else:
        status_bar.content.text = "No file to save"

# ---------------- Editor Window ----------------
editor_window = Window(
    content=BufferControl(
        buffer=buffer,
        lexer=PygmentsLexer(PythonLexer)
    ),
    left_margins=[NumberedMargin()],
    wrap_lines=False
)

# ---------------- Layout ----------------
root_container = HSplit([
    editor_window,
    status_bar
])
layout = Layout(root_container)

# ---------------- Style ----------------
style = Style.from_dict({
    "line-number": "ansigray",
    "line-number.current": "ansicyan bold",
    "status": "reverse"
})

# ---------------- Application ----------------
app = Application(
    layout=layout,
    key_bindings=kb,
    style=style,
    full_screen=True
)

if __name__ == "__main__":
    app.run()
