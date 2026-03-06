import json
import os
from tkinter import filedialog, messagebox

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKGROUND_CONFIG_FILE = os.path.join(BASE_DIR, "background.json")


class BackgroundMixin:
    _ALLOWED_EXT = {".png", ".jpeg", ".jpg", ".gif", ".webp"}

    def init_background_state(self) -> None:
        self.background_source: str = ""
        self._background_image_raw = None
        self._background_image_tk = None
        self._load_saved_background()

    def _draw_background_image(self, target_w: int, target_h: int) -> bool:
        if self._background_image_raw is None or Image is None or ImageTk is None:
            return False

        # Lightweight mode: no crop/resize, just center image and window.
        if self._background_image_tk is None:
            self._background_image_tk = ImageTk.PhotoImage(self._background_image_raw)
        self.bg_canvas.create_image(target_w / 2, target_h / 2, image=self._background_image_tk, anchor="center")
        return True

    def _read_background_config(self) -> str:
        if not os.path.exists(BACKGROUND_CONFIG_FILE):
            return ""
        try:
            with open(BACKGROUND_CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            return ""
        if not isinstance(data, dict):
            return ""
        path = data.get("background_path", "")
        return path if isinstance(path, str) else ""

    def _write_background_config(self, path: str) -> None:
        data = {"background_path": path}
        with open(BACKGROUND_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_background_from_path(self, path: str, show_error: bool) -> bool:
        ext = os.path.splitext(path)[1].lower()
        if ext not in self._ALLOWED_EXT:
            if show_error:
                messagebox.showerror(
                    "Unsupported format",
                    "Only PNG / JPEG / JPG / GIF / WebP are supported.",
                    parent=self,
                )
            return False

        if Image is None or ImageTk is None:
            if show_error:
                messagebox.showerror(
                    "Missing dependency",
                    "Pillow is required for PNG/JPEG/JPG/GIF/WebP upload.\\nRun: pip install pillow",
                    parent=self,
                )
            return False

        try:
            with Image.open(path) as src:
                self._background_image_raw = src.convert("RGBA")
                self._background_image_tk = None
        except Exception as exc:
            if show_error:
                messagebox.showerror("Invalid image", f"Could not load this image:\\n{exc}", parent=self)
            return False

        self.background_source = path
        if hasattr(self, "bg_canvas"):
            self._draw_background()
        return True

    def _load_saved_background(self) -> None:
        saved = self._read_background_config()
        if not saved:
            return
        if not os.path.exists(saved):
            self._write_background_config("")
            return
        loaded = self._load_background_from_path(saved, show_error=False)
        if not loaded:
            self._write_background_config("")

    def change_background(self) -> None:
        preferred_dir = os.path.expanduser("~")
        initial_dir = preferred_dir if os.path.isdir(preferred_dir) else os.path.expanduser("~")
        path = filedialog.askopenfilename(
            parent=self,
            title="Select background from file",
            initialdir=initial_dir,
            filetypes=[
                ("Image files", "*.png *.jpeg *.jpg *.gif *.webp"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpeg *.jpg"),
                ("GIF", "*.gif"),
                ("WebP", "*.webp"),
            ],
        )
        if not path:
            return

        loaded = self._load_background_from_path(path, show_error=True)
        if loaded:
            self._write_background_config(path)
