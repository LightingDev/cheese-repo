"""
Overlay Maker IDE (Python)
=================================

An extensible, cross‑platform Python application for designing, previewing,
and exporting real‑time graphic overlays (e.g., for livestreaming in OBS,
recorded demos, HUD mockups for games, interactive screen annotations, etc.).

MVP Goals
---------
1. Create & manage overlay *projects* (JSON/YAML project file).
2. Add/edit/re‑order *layers*: Text, Image, Shape, Browser/HTML, System Stats.
3. Visual *Design Canvas* with drag/resize, snap‑to‑grid, guides.
4. Live *Transparent Overlay Preview* window that floats above all apps.
5. Export to formats consumable by OBS (browser source bundle, image sequence),
or as a stand‑alone always‑on‑top window.
6. Basic animation keyframes (opacity, position, scale) with play/loop.
7. Optional remote data bindings (CPU %, Twitch chat count, custom HTTP JSON field).

Design Philosophy
-----------------
- **Modular:** clear separation of *models*, *controllers*, *views*, *services*.
- **Extensible Layer Plug‑ins:** users can drop in Python classes to add new layer types.
- **Data‑Driven Projects:** all design state serializable to disk.
- **Non‑Destructive Editing:** original assets remain untouched; transforms stored in project.
- **Real‑Time Updating:** changes in the IDE immediately reflected in overlay preview.

-----------------------------------------------
Quick Start (Developer)
-----------------------------------------------
```bash
# create and activate a virtual environment first (recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# install core runtime deps
pip install -r requirements.txt

# run the IDE
python -m overlay_ide
```
```

-----------------------------------------------
External Dependencies (Essentials vs Optional)
-----------------------------------------------

**Essential Runtime**
- **PySide6** (or PyQt6) – GUI framework; we use PySide6 for licensing friendliness.
- **Pillow** – image loading/saving & basic compositing.
- **pydantic** – typed config / project schema validation.
- **numpy** – array ops for image transforms & effects.
- **psutil** – system stats data binding (CPU, RAM) demo layer.
- **requests** – HTTP data polling bindings (JSON REST values to text layer fields).
- **watchfiles** (or watchdog) – auto‑reload assets when changed on disk.

**Recommended / Feature Extensions**
- **opencv-python** – advanced image transforms, webcam capture feed layers.
- **mss** – cross‑platform screen capture source layer.
- **websockets** + **obs-websocket-py** – control/update scenes in OBS or receive events.
- **pyperclip** – clipboard import/export of layer settings.
- **sounddevice** or **pyaudio** – audio‑reactive visualizations (VU meters).
- **pywin32** (Windows only) – deep transparent/click‑through window control.
- **pyobjc / pyobjc-framework-Quartz** (macOS) – advanced overlay behavior.
- **python-xlib** (Linux/X11) OR wayland‑protocol libs – deep window flags if needed.

**Dev / Build Tooling**
- **black**, **ruff**, **mypy**, **pytest**, **tox** – quality & testing.
- **pyinstaller** or **briefcase** – building distributables.

See `requirements-*.txt` files below for tiered installs.

-----------------------------------------------
Project Layout
-----------------------------------------------
overlay_maker_ide/
├─ pyproject.toml
├─ requirements.txt                # minimal (essentials)
├─ requirements-full.txt           # all optional goodies
├─ README.md
├─ overlay_ide/                    # package root (import overlay_ide)
│  ├─ __init__.py
│  ├─ __main__.py                  # python -m overlay_ide entrypoint
│  ├─ app.py                       # QApplication bootstrap
│  ├─ models/
│  │   ├─ base.py                  # BaseModel mixins
│  │   ├─ project.py               # ProjectModel + serialization
│  │   ├─ layer_base.py            # AbstractLayer + registry
│  │   ├─ layer_text.py            # TextLayer
│  │   ├─ layer_image.py           # ImageLayer
│  │   ├─ layer_shape.py           # Rect/EllipseLayer
│  │   ├─ layer_browser.py         # HTML/URL layer (QtWebEngine optional)
│  │   ├─ layer_sysstats.py        # CPU/Mem binding demo
│  │   └─ animation.py             # Keyframes & timelines
│  ├─ views/
│  │   ├─ main_window.py           # Main IDE shell
│  │   ├─ canvas_widget.py         # Design canvas (QGraphicsScene)
│  │   ├─ layer_list_widget.py     # Layer stack UI
│  │   ├─ properties_panel.py      # Context inspector
│  │   ├─ timeline_panel.py        # Animation timeline
│  │   ├─ data_binding_panel.py    # Bind external data to props
│  │   └─ overlay_preview_window.py# Transparent always‑on‑top window
│  ├─ controllers/
│  │   ├─ project_controller.py
│  │   ├─ layer_controller.py
│  │   ├─ binding_controller.py
│  │   └─ animation_controller.py
│  ├─ services/
│  │   ├─ assets_manager.py
│  │   ├─ render_engine.py
│  │   ├─ export_manager.py        # Export bundles for OBS / static renders
│  │   ├─ data_sources.py          # HTTP poller, psutil poller, etc.
│  │   ├─ obs_bridge.py            # optional obs-websocket integration
│  │   └─ platform_win_overlay.py  # OS‑specific helpers (win/mac/linux)
│  ├─ utils/
│  │   ├─ logging_config.py
│  │   ├─ paths.py
│  │   └─ qt_helpers.py
│  ├─ resources/
│  │   ├─ icons/
│  │   ├─ qss/
│  │   └─ sample_assets/
│  └─ sample_projects/
│      └─ demo_overlay.json
└─ tests/
   ├─ test_project_io.py
   └─ test_layer_models.py

-----------------------------------------------
Configuration Strategy
-----------------------------------------------
- All projects saved as JSON (default) validated by pydantic models.
- Assets referenced by *relative* path where possible.
- Per‑user settings stored in `~/.overlay_maker_ide/config.json`.

-----------------------------------------------
Minimal Requirements File (requirements.txt)
-----------------------------------------------
```
PySide6>=6.7
Pillow>=10.0
pydantic>=2.0
numpy>=1.25
psutil>=5.9
requests>=2.32
watchfiles>=0.22  # or watchdog>=4.0
```

Full Feature Requirements (requirements-full.txt)
-----------------------------------------------
```
-r requirements.txt
opencv-python>=4.10
mss>=9.0
websockets>=12.0
obs-websocket-py>=1.0
pyperclip>=1.9
sounddevice>=0.5  # OR pyaudio
pywin32>=306; platform_system=="Windows"
pyobjc>=10; platform_system=="Darwin"
pyobjc-framework-Quartz>=10; platform_system=="Darwin"
python-xlib>=0.33; platform_system=="Linux"
```

-----------------------------------------------
Environment Variables (Optional)
-----------------------------------------------
- OVERLAY_IDE_DEBUG=1            # verbose logging
- OVERLAY_IDE_DATA_POLL_MS=1000  # data binding poll frequency
- OVERLAY_IDE_DEFAULT_FONT_PATH  # override default font

-----------------------------------------------
Code Implementation (Initial Skeleton)
-----------------------------------------------
Below is a *single‑file concatenated* source drop showing minimal runnable MVP.
For actual development, split into the module layout above. This gives you a
fast start: copy/paste into file tree and expand.
"""

# ============================================================================
# overlay_ide/__init__.py
# ============================================================================
__all__ = ["run_app", "OverlayApp"]

# ============================================================================
# overlay_ide/app.py
# ============================================================================
import os
import sys
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import QApplication

# Local imports will be resolved after proper package split; stubbed here
# fallback inline imports below to keep single‑file demo self‑contained.


def run_app(project_path: Optional[str] = None) -> int:
    """Entry wrapper used by __main__.py."""
    app = QApplication(sys.argv)
    app.setOrganizationName("OverlayMaker")
    app.setApplicationName("Overlay Maker IDE")

    from overlay_ide.views.main_window import MainWindow  # lazy import

    win = MainWindow(project_path=project_path)
    win.show()
    return app.exec()


class OverlayApp:
    """Convenience class if you want to embed the IDE in another tool."""
    def __init__(self, project_path: Optional[str] = None):
        self._project_path = project_path
        self._app = None
        self._win = None

    def start(self):
        if self._app is None:
            self._app = QApplication(sys.argv)
            self._app.setOrganizationName("OverlayMaker")
            self._app.setApplicationName("Overlay Maker IDE")
            from overlay_ide.views.main_window import MainWindow
            self._win = MainWindow(project_path=self._project_path)
            self._win.show()
        return self._app.exec()


# ============================================================================
# overlay_ide/__main__.py  (makes `python -m overlay_ide` work)
# ============================================================================
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Overlay Maker IDE")
    parser.add_argument("project", nargs="?", help="Path to overlay project JSON")
    args = parser.parse_args()

    sys.exit(run_app(project_path=args.project))


# ============================================================================
# overlay_ide/models/base.py
# ============================================================================
from pydantic import BaseModel, Field


class OMBaseModel(BaseModel):
    class Config:
        extra = "ignore"
        validate_assignment = True
        arbitrary_types_allowed = True


# ============================================================================
# overlay_ide/models/layer_base.py
# ============================================================================
from typing import Dict, Type, Any, ClassVar
from pydantic import BaseModel, Field


_LAYER_REGISTRY: Dict[str, Type["LayerModel"]] = {}


def register_layer(layer_cls: Type["LayerModel"]):
    _LAYER_REGISTRY[layer_cls.layer_type()] = layer_cls
    return layer_cls


class LayerModel(OMBaseModel):
    id: str = Field(..., description="Unique layer id")
    name: str = Field(default="New Layer")
    x: float = 0
    y: float = 0
    width: float = 200
    height: float = 50
    opacity: float = 1.0
    visible: bool = True
    rotation: float = 0.0
    locked: bool = False

    @classmethod
    def layer_type(cls) -> str:  # override
        return "base"

    def to_dict(self) -> Dict[str, Any]:
        d = self.model_dump()
        d["type"] = self.layer_type()
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LayerModel":
        t = data.get("type", "base")
        if t != "base":
            layer_cls = _LAYER_REGISTRY.get(t, cls)
            return layer_cls(**{k: v for k, v in data.items() if k != "type"})
        return cls(**{k: v for k, v in data.items() if k != "type"})


# ============================================================================
# overlay_ide/models/layer_text.py
# ============================================================================
from typing import Optional


@register_layer
class TextLayer(LayerModel):
    text: str = "Sample Text"
    font_family: str = "Arial"
    font_size: int = 32
    color: str = "#FFFFFF"
    outline_color: Optional[str] = None
    outline_width: int = 0
    bold: bool = False
    italic: bool = False
    h_align: str = "left"   # left|center|right
    v_align: str = "top"    # top|middle|bottom
    data_binding: Optional[str] = None  # e.g. "sys.cpu" or URL JSON path

    @classmethod
    def layer_type(cls) -> str:
        return "text"


# ============================================================================
# overlay_ide/models/layer_image.py
# ============================================================================
@register_layer
class ImageLayer(LayerModel):
    source_path: str = ""
    preserve_aspect: bool = True
    tint_color: Optional[str] = None

    @classmethod
    def layer_type(cls) -> str:
        return "image"


# ============================================================================
# overlay_ide/models/layer_shape.py
# ============================================================================
@register_layer
class ShapeLayer(LayerModel):
    shape: str = "rect"  # rect|ellipse
    fill: str = "#00000000"  # RGBA hex; 00 alpha = transparent
    stroke: str = "#FFFFFFFF"
    stroke_width: int = 1

    @classmethod
    def layer_type(cls) -> str:
        return "shape"


# ============================================================================
# overlay_ide/models/project.py
# ============================================================================
from typing import List
from uuid import uuid4


class ProjectModel(OMBaseModel):
    name: str = Field(default="Untitled Overlay")
    canvas_width: int = 1920
    canvas_height: int = 1080
    background_color: str = "#00000000"  # transparent
    layers: List[LayerModel] = Field(default_factory=list)

    @classmethod
    def new(cls, name: str = "Untitled Overlay", size=(1920, 1080)) -> "ProjectModel":
        return cls(name=name, canvas_width=size[0], canvas_height=size[1])

    def add_layer(self, layer: LayerModel):
        if not layer.id:
            layer.id = str(uuid4())
        self.layers.append(layer)

    def remove_layer(self, layer_id: str):
        self.layers = [l for l in self.layers if l.id != layer_id]

    def to_dict(self):
        d = self.model_dump()
        d["layers"] = [l.to_dict() for l in self.layers]
        return d

    @classmethod
    def from_dict(cls, data):
        layers = [LayerModel.from_dict(ld) for ld in data.get("layers", [])]
        return cls(
            name=data.get("name", "Untitled Overlay"),
            canvas_width=data.get("canvas_width", 1920),
            canvas_height=data.get("canvas_height", 1080),
            background_color=data.get("background_color", "#00000000"),
            layers=layers,
        )


# ============================================================================
# overlay_ide/utils/paths.py
# ============================================================================
APP_DIR = Path.home() / ".overlay_maker_ide"
APP_DIR.mkdir(exist_ok=True)

CONFIG_PATH = APP_DIR / "config.json"
RECENTS_PATH = APP_DIR / "recent.json"


# ============================================================================
# overlay_ide/utils/logging_config.py
# ============================================================================
import logging


def setup_logging(debug: bool = False):
    lvl = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=lvl, format="%(levelname)s %(name)s: %(message)s")


# ============================================================================
# overlay_ide/services/assets_manager.py
# ============================================================================
from typing import Dict


class AssetsManager:
    """Simple cache for loaded image assets (expand later)."""
    def __init__(self):
        self._image_cache: Dict[str, "QImage"] = {}

    def get_image(self, path: str):
        from PySide6.QtGui import QImage
        if path in self._image_cache:
            return self._image_cache[path]
        img = QImage(path)
        if not img.isNull():
            self._image_cache[path] = img
        return img


ASSETS = AssetsManager()


# ============================================================================
# overlay_ide/views/canvas_widget.py
# ============================================================================
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPen, QBrush, QColor, QFont
from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsRectItem,
    QGraphicsTextItem,
    QGraphicsPixmapItem,
    QStyleOptionGraphicsItem,
    QWidget,
)
from PySide6.QtGui import QPixmap


class CanvasView(QGraphicsView):
    """Main design surface."""
    def __init__(self, project_model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setScene(QGraphicsScene())
        self.project_model = project_model
        self._layer_items = {}
        self.setRenderHints(self.renderHints() | self.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.refresh_from_model()

    def refresh_from_model(self):
        self.scene().clear()
        self._layer_items.clear()
        # Background rect (visual only)
        bg_color = QColor(self.project_model.background_color)
        bg_item = QGraphicsRectItem(0, 0, self.project_model.canvas_width, self.project_model.canvas_height)
        bg_item.setBrush(QBrush(bg_color))
        bg_item.setPen(Qt.NoPen)
        self.scene().addItem(bg_item)
        for layer in self.project_model.layers:
            if not layer.visible:
                continue
            item = self._create_item_for_layer(layer)
            if item:
                self.scene().addItem(item)
                self._layer_items[layer.id] = item
        self.setSceneRect(QRectF(0, 0, self.project_model.canvas_width, self.project_model.canvas_height))

    def _create_item_for_layer(self, layer):
        t = layer.__class__.layer_type()
        if t == "text":
            item = QGraphicsTextItem(layer.text)
            font = QFont(layer.font_family, layer.font_size)
            font.setBold(layer.bold)
            font.setItalic(layer.italic)
            item.setFont(font)
            item.setDefaultTextColor(QColor(layer.color))
            item.setPos(layer.x, layer.y)
            return item
        elif t == "image":
            from overlay_ide.services.assets_manager import ASSETS
            img = ASSETS.get_image(layer.source_path)
            if img.isNull():
                return None
            pm = QPixmap.fromImage(img)
            item = QGraphicsPixmapItem(pm.scaled(layer.width, layer.height, Qt.KeepAspectRatio if layer.preserve_aspect else Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
            item.setPos(layer.x, layer.y)
            return item
        elif t == "shape":
            rect = QGraphicsRectItem(0, 0, layer.width, layer.height)
            rect.setPos(layer.x, layer.y)
            rect.setPen(QPen(QColor(layer.stroke), layer.stroke_width))
            rect.setBrush(QBrush(QColor(layer.fill)))
            return rect
        else:
            return None


# ============================================================================
# overlay_ide/views/overlay_preview_window.py
# ============================================================================
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget


class OverlayPreviewWindow(QWidget):
    """Frameless transparent top‑most window that mirrors current project."""
    def __init__(self, project_model, parent=None):
        super().__init__(parent)
        self.project_model = project_model
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
            | Qt.FramelessWindowHint
            | Qt.Tool  # prevents taskbar icon on some OSes
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.resize(self.project_model.canvas_width, self.project_model.canvas_height)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        # Iterate visible layers and paint directly.
        for layer in self.project_model.layers:
            if not layer.visible:
                continue
            self._paint_layer(painter, layer)

    def _paint_layer(self, p, layer):
        t = layer.__class__.layer_type()
        if t == "text":
            from PySide6.QtGui import QColor, QFont
            p.setOpacity(layer.opacity)
            p.setPen(QColor(layer.color))
            font = QFont(layer.font_family, layer.font_size)
            font.setBold(layer.bold)
            font.setItalic(layer.italic)
            p.setFont(font)
            p.drawText(layer.x, layer.y + layer.font_size, layer.text)
        elif t == "image":
            from overlay_ide.services.assets_manager import ASSETS
            img = ASSETS.get_image(layer.source_path)
            if img.isNull():
                return
            from PySide6.QtGui import QPixmap
            pm = QPixmap.fromImage(img)
            if layer.preserve_aspect:
                pm = pm.scaled(layer.width, layer.height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            else:
                pm = pm.scaled(layer.width, layer.height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            p.setOpacity(layer.opacity)
            p.drawPixmap(layer.x, layer.y, pm)
        elif t == "shape":
            from PySide6.QtGui import QColor, QPen, QBrush
            p.setOpacity(layer.opacity)
            p.setPen(QPen(QColor(layer.stroke), layer.stroke_width))
            p.setBrush(QBrush(QColor(layer.fill)))
            p.drawRect(layer.x, layer.y, layer.width, layer.height)


# ============================================================================
# overlay_ide/views/layer_list_widget.py
# ============================================================================
from PySide6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QPushButton, QListWidgetItem


class LayerListWidget(QWidget):
    """Shows stack of layers; supports add/remove/reorder (MVP)."""
    def __init__(self, project_model, on_layer_selected=None, parent=None):
        super().__init__(parent)
        self.project_model = project_model
        self.on_layer_selected = on_layer_selected
        self.list = QListWidget()
        self.btn_add_text = QPushButton("+ Text")
        self.btn_add_image = QPushButton("+ Image")
        self.btn_add_shape = QPushButton("+ Shape")
        lay = QVBoxLayout(self)
        lay.addWidget(self.list)
        lay.addWidget(self.btn_add_text)
        lay.addWidget(self.btn_add_image)
        lay.addWidget(self.btn_add_shape)
        self._connect()
        self.refresh()

    def _connect(self):
        self.list.currentItemChanged.connect(self._layer_selected)
        self.btn_add_text.clicked.connect(self._add_text)
        self.btn_add_image.clicked.connect(self._add_image)
        self.btn_add_shape.clicked.connect(self._add_shape)

    def refresh(self):
        self.list.clear()
        for layer in reversed(self.project_model.layers):  # topmost first
            item = QListWidgetItem(f"{layer.__class__.layer_type()}: {layer.name}")
            item.setData(32, layer.id)
            self.list.addItem(item)

    def _layer_selected(self, cur, prev):
        if not cur:
            return
        layer_id = cur.data(32)
        if self.on_layer_selected:
            self.on_layer_selected(layer_id)

    def _add_text(self):
        from overlay_ide.models.layer_text import TextLayer
        self.project_model.add_layer(TextLayer(id="", name="Text", text="Hello Overlay!", x=50, y=50))
        self.refresh()

    def _add_image(self):
        from overlay_ide.models.layer_image import ImageLayer
        self.project_model.add_layer(ImageLayer(id="", name="Image", source_path="", width=300, height=200))
        self.refresh()

    def _add_shape(self):
        from overlay_ide.models.layer_shape import ShapeLayer
        self.project_model.add_layer(ShapeLayer(id="", name="Shape", width=200, height=100, fill="#5500FF80"))
        self.refresh()


# ============================================================================
# overlay_ide/views/properties_panel.py
# ============================================================================
from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
    QColorDialog,
    QPushButton,
)
from PySide6.QtCore import Qt


class PropertiesPanel(QWidget):
    """Edits common layer properties (MVP)."""
    def __init__(self, project_model, parent=None):
        super().__init__(parent)
        self.project_model = project_model
        self._layer = None
        self.form = QFormLayout(self)
        # Controls
        self.ed_name = QLineEdit()
        self.sp_x = QDoubleSpinBox(); self.sp_x.setRange(-99999, 99999)
        self.sp_y = QDoubleSpinBox(); self.sp_y.setRange(-99999, 99999)
        self.sp_w = QDoubleSpinBox(); self.sp_w.setRange(0, 99999)
        self.sp_h = QDoubleSpinBox(); self.sp_h.setRange(0, 99999)
        self.sp_op = QDoubleSpinBox(); self.sp_op.setRange(0, 1); self.sp_op.setSingleStep(0.05)
        self.btn_color = QPushButton("Color…")
        # Add to form
        self.form.addRow("Name", self.ed_name)
        self.form.addRow("X", self.sp_x)
        self.form.addRow("Y", self.sp_y)
        self.form.addRow("Width", self.sp_w)
        self.form.addRow("Height", self.sp_h)
        self.form.addRow("Opacity", self.sp_op)
        self.form.addRow("Color", self.btn_color)
        self._connect()
        self.setDisabled(True)

    def _connect(self):
        self.ed_name.editingFinished.connect(self._apply)
        self.sp_x.valueChanged.connect(self._apply)
        self.sp_y.valueChanged.connect(self._apply)
        self.sp_w.valueChanged.connect(self._apply)
        self.sp_h.valueChanged.connect(self._apply)
        self.sp_op.valueChanged.connect(self._apply)
        self.btn_color.clicked.connect(self._pick_color)

    def _pick_color(self):
        if not self._layer:
            return
        from PySide6.QtGui import QColor
        col = QColorDialog.getColor(QColor(getattr(self._layer, "color", "#FFFFFF")), self)
        if col.isValid():
            if hasattr(self._layer, "color"):
                self._layer.color = col.name(QColor.HexArgb)
            self._apply(refresh=False)

    def load_layer(self, layer):
        self._layer = layer
        if not layer:
            self.setDisabled(True)
            return
        self.setDisabled(False)
        self.ed_name.setText(layer.name)
        self.sp_x.setValue(layer.x)
        self.sp_y.setValue(layer.y)
        self.sp_w.setValue(layer.width)
        self.sp_h.setValue(layer.height)
        self.sp_op.setValue(layer.opacity)

    def _apply(self, refresh=True):
        if not self._layer:
            return
        self._layer.name = self.ed_name.text()
        self._layer.x = self.sp_x.value()
        self._layer.y = self.sp_y.value()
        self._layer.width = self.sp_w.value()
        self._layer.height = self.sp_h.value()
        self._layer.opacity = self.sp_op.value()
        if refresh:
            self.parent().parent().refresh_canvas()


# ============================================================================
# overlay_ide/views/main_window.py
# ============================================================================
from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QWidget,
    QHBoxLayout,
    QMessageBox,
    QAction,
    QSplitter,
)
import json


class MainWindow(QMainWindow):
    def __init__(self, project_path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Overlay Maker IDE")
        # Load project (new if none)
        if project_path and Path(project_path).exists():
            self.project_model = self._load_project(project_path)
            self._project_path = Path(project_path)
        else:
            self.project_model = ProjectModel.new()
            self._project_path = None
        # UI parts
        self.canvas = CanvasView(self.project_model)
        self.layer_list = LayerListWidget(self.project_model, on_layer_selected=self._on_layer_selected)
        self.props_panel = PropertiesPanel(self.project_model)
        self.preview_win = OverlayPreviewWindow(self.project_model)
        # Layout
        central = QWidget()
        self.setCentralWidget(central)
        split = QSplitter()
        split.addWidget(self.layer_list)
        split.addWidget(self.canvas)
        split.addWidget(self.props_panel)
        lay = QHBoxLayout(central)
        lay.addWidget(split)
        # Menus
        self._build_menu()
        # Show preview by default
        self.preview_win.show()

    # ---------------- Menu -----------------
    def _build_menu(self):
        m_file = self.menuBar().addMenu("File")
        act_new = QAction("New", self); act_new.triggered.connect(self.new_project)
        act_open = QAction("Open…", self); act_open.triggered.connect(self.open_project)
        act_save = QAction("Save", self); act_save.triggered.connect(self.save_project)
        act_save_as = QAction("Save As…", self); act_save_as.triggered.connect(self.save_project_as)
        m_file.addAction(act_new)
        m_file.addAction(act_open)
        m_file.addAction(act_save)
        m_file.addAction(act_save_as)

        m_view = self.menuBar().addMenu("View")
        act_toggle_preview = QAction("Toggle Overlay Preview", self, checkable=True, checked=True)
        act_toggle_preview.triggered.connect(self._toggle_preview)
        m_view.addAction(act_toggle_preview)

    # ---------------- Project lifecycle -----------------
    def new_project(self):
        self.project_model = ProjectModel.new()
        self._project_path = None
        self.layer_list.project_model = self.project_model
        self.props_panel.project_model = self.project_model
        self.canvas.project_model = self.project_model
        self.preview_win.project_model = self.project_model
        self.refresh_canvas()
        self.layer_list.refresh()

    def open_project(self):
        p, _ = QFileDialog.getOpenFileName(self, "Open Overlay Project", str(Path.home()), "Overlay JSON (*.json)")
        if not p:
            return
        self.project_model = self._load_project(p)
        self._project_path = Path(p)
        self.layer_list.project_model = self.project_model
        self.props_panel.project_model = self.project_model
        self.canvas.project_model = self.project_model
        self.preview_win.project_model = self.project_model
        self.refresh_canvas()
        self.layer_list.refresh()

    def save_project(self):
        if not self._project_path:
            return self.save_project_as()
        self._write_project(self._project_path)

    def save_project_as(self):
        p, _ = QFileDialog.getSaveFileName(self, "Save Overlay Project", str(Path.home() / "overlay.json"), "Overlay JSON (*.json)")
        if not p:
            return
        self._project_path = Path(p)
        self._write_project(self._project_path)

    def _write_project(self, path: Path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.project_model.to_dict(), f, indent=2)
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))

    def _load_project(self, path: str) -> ProjectModel:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return ProjectModel.from_dict(data)
        except Exception as e:
            QMessageBox.critical(self, "Load Error", str(e))
            return ProjectModel.new()

    # ---------------- Layer selection -----------------
    def _on_layer_selected(self, layer_id: str):
        lyr = next((l for l in self.project_model.layers if l.id == layer_id), None)
        self.props_panel.load_layer(lyr)

    # ---------------- Overlay preview -----------------
    def _toggle_preview(self, checked: bool):
        if checked:
            self.preview_win.show()
        else:
            self.preview_win.hide()

    # ---------------- Refresh -----------------
    def refresh_canvas(self):
        self.canvas.refresh_from_model()
        self.preview_win.update()  # triggers paintEvent


# ============================================================================
# SAMPLE PROJECT JSON (overlay_ide/sample_projects/demo_overlay.json)
# ============================================================================
# Provided below as an inline sample for reference only.
SAMPLE_PROJECT_JSON = {
    "name": "Demo Overlay",
    "canvas_width": 1280,
    "canvas_height": 720,
    "background_color": "#00000000",
    "layers": [
        {
            "type": "text",
            "id": "txt1",
            "name": "Title",
            "text": "Welcome!",
            "font_family": "Arial",
            "font_size": 48,
            "color": "#FFFFFFFF",
            "x": 100,
            "y": 100,
            "width": 500,
            "height": 100,
            "opacity": 1,
            "visible": True,
        },
        {
            "type": "shape",
            "id": "box1",
            "name": "LowerThirdBG",
            "shape": "rect",
            "fill": "#55000080",
            "stroke": "#FFFFFFFF",
            "stroke_width": 2,
            "x": 50,
            "y": 600,
            "width": 1180,
            "height": 80,
            "opacity": 0.8,
            "visible": True,
        }
    ]
}


# ============================================================================
# README.md (inline quick doc)
# ============================================================================
README_MD = r"""
# Overlay Maker IDE

A Python desktop application for building live graphic overlays for streaming,
video production, and UI prototyping. Built with PySide6.

## Features (MVP)
- Create overlay projects of arbitrary resolution.
- Add Text / Image / Shape layers.
- Drag & drop editing canvas.
- Property inspector to edit position, size, opacity, color.
- Transparent preview window always‑on‑top for live testing.
- Save & open project JSON.

## Planned / Stretch
- Data bindings (system stats, HTTP JSON, OBS events).
- Keyframe animation timeline.
- Browser/HTML & WebSocket reactive layers.
- Export overlay to OBS Browser Source bundle.
- Color themes / custom QSS skins.
- Plugin system for custom layer types.

## Install
```bash
pip install -r requirements.txt
python -m overlay_ide
```

## Dev Notes
- Uses pydantic models for project schema.
- Rendering inside preview window is immediate mode paint; production build
  should use cached pixmaps for performance.
- For high‑refresh overlays, consider a QTimer or frame clock.

"""
