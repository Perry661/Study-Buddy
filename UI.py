import tkinter as tk
from datetime import date, datetime
from typing import Optional

from ADD import AddTaskMixin
from backgroud import BackgroundMixin
from DELETE import DeleteTaskMixin
from FINISH import FinishTaskMixin
from more import MoreMenuMixin
from ui_data import TaskStore, parse_due_date


class StudyBuddyUI(BackgroundMixin, AddTaskMixin, DeleteTaskMixin, FinishTaskMixin, MoreMenuMixin, tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Study Buddy")
        self.geometry("838x781")
        self.minsize(644, 600)
        self.configure(bg="#b9f0da")

        self.store = TaskStore()
        self.active_items: list[dict] = []
        self.selected_task_id: Optional[int] = None
        self._single_click_after_id: Optional[str] = None
        self.init_background_state()

        self._build_ui()
        self.reload_from_disk()
        self._tick_clock()

    def _build_ui(self) -> None:
        self.bg_canvas = tk.Canvas(self, highlightthickness=0, bd=0, bg="#b9f0da")
        self.bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bind("<Configure>", self._on_resize)
        self._draw_background()

        self.time_label = tk.Label(
            self,
            text="",
            fg="black",
            bg="#f7f7f7",
            font=("Times New Roman", 24, "bold"),
            justify="left",
        )
        self.time_label.place(relx=0.82, rely=0.04, anchor="nw")
        self.more_btn = self._make_circle_button(
            self, "...", self.open_more_menu, size=78, text_size=26, canvas_bg="#f7f7f7"
        )
        self.more_btn.place(relx=0.05, rely=0.07, anchor="center")

        self.list_border = tk.Frame(self, bg="black")
        self.list_border.place(relx=0.10, rely=0.29, relwidth=0.78, relheight=0.34)

        self.list_holder = tk.Frame(self.list_border, bg="#f4f4f4")
        self.list_holder.place(relx=0.005, rely=0.007, relwidth=0.99, relheight=0.986)

        self.list_canvas = tk.Canvas(self.list_holder, bg="#f4f4f4", highlightthickness=0, bd=0)
        self.list_scroll = tk.Scrollbar(self.list_holder, orient="vertical", command=self.list_canvas.yview)
        self.list_canvas.configure(yscrollcommand=self.list_scroll.set)
        self.list_canvas.pack(side="left", fill="both", expand=True)
        self.list_scroll.pack(side="right", fill="y")

        self.task_container = tk.Frame(self.list_canvas, bg="#f4f4f4")
        self.task_window = self.list_canvas.create_window((0, 0), window=self.task_container, anchor="nw")
        self.task_container.bind("<Configure>", self._on_task_container_configure)
        self.list_canvas.bind("<Configure>", self._on_list_canvas_configure)
        self.list_canvas.bind("<MouseWheel>", self._on_mousewheel)

        self.bottom_bar = tk.Frame(self, bg="#f7f7f7")
        self.bottom_bar.place(relx=0.03, rely=0.72, relwidth=0.92, relheight=0.20)

        self.trash_btn = self._make_circle_button(
            self.bottom_bar, "🗑️", self.open_trash_window, text_font=("Apple Color Emoji", 34)
        )
        self.add_btn = self._make_circle_button(
            self.bottom_bar, "➕", self.open_add_window, text_font=("Apple Color Emoji", 34)
        )
        self.finish_btn = self._make_circle_button(
            self.bottom_bar, "✅", self.finish_selected, text_font=("Apple Color Emoji", 34)
        )

        # Keep round buttons visually in place while lifting the square bar.
        self.trash_btn.place(relx=0.12, rely=0.45, anchor="center")
        self.add_btn.place(relx=0.50, rely=0.45, anchor="center")
        self.finish_btn.place(relx=0.88, rely=0.45, anchor="center")

    def _draw_background(self) -> None:
        self.bg_canvas.delete("all")
        w = max(self.winfo_width(), 838)
        h = max(self.winfo_height(), 781)

        if self._draw_background_image(w, h):
            return

        self.bg_canvas.create_rectangle(0, 0, w, h, fill="#aeeacf", outline="")

        self._draw_cloud(120, 110, 0.95)
        self._draw_cloud(w - 220, 110, 0.95)
        self._draw_cloud(330, 250, 0.85)
        self._draw_cloud(w - 140, 210, 0.75)

        self.bg_canvas.create_polygon(
            0,
            h * 0.56,
            w,
            h * 0.49,
            w,
            h * 0.72,
            0,
            h * 0.61,
            fill="#b8d98a",
            outline="",
        )
        self.bg_canvas.create_polygon(
            0,
            h * 0.61,
            w,
            h * 0.75,
            w,
            h * 0.86,
            0,
            h * 0.74,
            fill="#80bb62",
            outline="",
        )
        self.bg_canvas.create_polygon(
            0,
            h * 0.74,
            w * 0.78,
            h * 0.79,
            w,
            h * 0.83,
            w,
            h,
            0,
            h,
            fill="#5ba34d",
            outline="",
        )
        self.bg_canvas.create_polygon(
            0,
            h,
            w,
            h,
            w,
            h * 0.83,
            fill="#3f8241",
            outline="",
        )

        self._draw_scribble(w * 0.18, h * 0.70)
        self._draw_scribble(w * 0.78, h * 0.73)
        self._draw_scribble(w * 0.62, h * 0.81)
        self._draw_tiny_tree(w * 0.50, h * 0.75)
        self._draw_tiny_tree(w * 0.72, h * 0.65)

    def _draw_cloud(self, x: float, y: float, scale: float) -> None:
        c = "#f1f1f1"
        self.bg_canvas.create_oval(x - 95 * scale, y - 35 * scale, x + 40 * scale, y + 35 * scale, fill=c, outline="")
        self.bg_canvas.create_oval(x - 20 * scale, y - 30 * scale, x + 80 * scale, y + 30 * scale, fill=c, outline="")
        self.bg_canvas.create_oval(x + 45 * scale, y - 18 * scale, x + 120 * scale, y + 30 * scale, fill=c, outline="")
        self.bg_canvas.create_rectangle(x - 100 * scale, y, x + 120 * scale, y + 22 * scale, fill=c, outline="")

    def _draw_scribble(self, x: float, y: float) -> None:
        points = [
            x - 40,
            y,
            x - 25,
            y - 10,
            x - 8,
            y + 4,
            x + 8,
            y - 9,
            x + 24,
            y + 3,
            x + 40,
            y - 6,
        ]
        self.bg_canvas.create_line(points, fill="black", width=3, smooth=True)

    def _draw_tiny_tree(self, x: float, y: float) -> None:
        self.bg_canvas.create_line(x, y, x, y + 55, fill="black", width=3)
        self.bg_canvas.create_oval(x - 24, y - 22, x + 20, y + 14, outline="black", width=3)
        self.bg_canvas.create_oval(x - 10, y - 30, x + 30, y + 10, outline="black", width=3)

    def _on_resize(self, _event: tk.Event) -> None:
        self._draw_background()

    def _on_task_container_configure(self, _event: tk.Event) -> None:
        self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all"))

    def _on_list_canvas_configure(self, event: tk.Event) -> None:
        self.list_canvas.itemconfigure(self.task_window, width=event.width)

    def _on_mousewheel(self, event: tk.Event) -> None:
        self.list_canvas.yview_scroll(int(-event.delta / 120), "units")

    def _make_circle_button(
        self,
        parent: tk.Widget,
        text: str,
        command,
        size: int = 120,
        text_size: int = 34,
        text_font: Optional[tuple[str, int] | tuple[str, int, str]] = None,
        canvas_bg: Optional[str] = None,
    ) -> tk.Canvas:
        parent_bg = str(parent.cget("bg")) if "bg" in parent.keys() else "#f7f7f7"
        c = tk.Canvas(parent, width=size, height=size, highlightthickness=0, bd=0, bg=canvas_bg or parent_bg)
        margin = max(6, int(size * 0.07))
        c.create_oval(margin, margin, size - margin, size - margin, width=3, outline="black", fill="#f8f8f8")
        font_spec = text_font if text_font is not None else ("Times New Roman", text_size, "bold")
        c.create_text(size / 2, size / 2, text=text, fill="black", font=font_spec)
        c.bind("<Button-1>", lambda _e: command())
        return c

    def _tick_clock(self) -> None:
        now = datetime.now()
        self.time_label.configure(text=f"{now.strftime('%Y-%m-%d')}\n{now.strftime('%H:%M')}")
        self.after(1000, self._tick_clock)

    def _due_hint(self, due: str) -> str:
        parsed = parse_due_date(due)
        if parsed is None:
            return "Due date: invalid"
        days = (parsed - date.today()).days
        if days > 0:
            return f"due {due} | {days} day(s) left"
        if days == 0:
            return f"due {due} | due today"
        return f"due {due} | overdue {-days} day(s)"

    def reload_from_disk(self) -> None:
        self.store.load()
        self.refresh_view()

    def refresh_view(self) -> None:
        for w in self.task_container.winfo_children():
            w.destroy()

        self.active_items = sorted(self.store.tasks, key=lambda x: x["dueDate"])
        if not self.active_items:
            tk.Label(
                self.task_container,
                text="(No tasks)",
                bg="#f4f4f4",
                fg="black",
                font=("SimSun", 24, "bold"),
                anchor="w",
                padx=18,
                pady=20,
            ).pack(fill="x")
        else:
            for idx, item in enumerate(self.active_items):
                self._build_task_row(idx, item)

        self.store.save()

    def _build_task_row(self, idx: int, item: dict) -> None:
        selected = self.selected_task_id == int(item["ID"])
        row_bg = "#eaf4ff" if selected else "#f4f4f4"
        row = tk.Frame(self.task_container, bg=row_bg, height=84)
        row.pack(fill="x")
        row.pack_propagate(False)

        if idx > 0:
            tk.Frame(row, bg="black", height=2).pack(fill="x", side="top")

        body = tk.Frame(row, bg=row_bg, padx=20, pady=12)
        body.pack(fill="both", expand=True)

        task_name = tk.Label(
            body,
            text=item["task"],
            bg=row_bg,
            fg="black",
            font=("SimSun", 35 if len(item["task"]) <= 4 else 25, "bold"),
            anchor="w",
        )
        task_name.pack(side="left", fill="x", expand=True)
        due_hint = tk.Label(
            body,
            text=self._due_hint(item["dueDate"]),
            bg=row_bg,
            fg="black",
            font=("Times New Roman", 15, "bold"),
            anchor="e",
        )
        due_hint.pack(side="right", padx=(15, 10))

        task_id = int(item["ID"])
        widgets = (row, body, task_name, due_hint)
        for widget in widgets:
            widget.bind("<Button-1>", lambda _e, tid=task_id: self._on_task_single_click(tid))
            widget.bind("<Button-2>", lambda _e, tid=task_id: self._on_task_two_finger_click(tid))
            widget.bind("<Button-3>", lambda _e, tid=task_id: self._on_task_two_finger_click(tid))
            
            # Old behavior kept for reference: quick double-click to open detail.
            # widget.bind("<Double-Button-1>", lambda _e, tid=task_id: self._on_task_double_click(tid))
            # widget.bind("<Double-Button-2>", lambda _e, tid=task_id: self._on_task_double_click(tid))
            # widget.bind("<Double-Button-3>", lambda _e, tid=task_id: self._on_task_double_click(tid))

    def _on_task_single_click(self, task_id: int) -> None:
        # Delay single-click action so it can be canceled by a double-click.
        if self._single_click_after_id is not None:
            self.after_cancel(self._single_click_after_id)
        self._single_click_after_id = self.after(220, lambda: self.select_task(task_id))

    def _on_task_double_click(self, task_id: int) -> None:
        if self._single_click_after_id is not None:
            self.after_cancel(self._single_click_after_id)
            self._single_click_after_id = None
        self.open_task_detail(task_id, select=False)

    def _on_task_two_finger_click(self, task_id: int) -> None:
        if self._single_click_after_id is not None:
            self.after_cancel(self._single_click_after_id)
            self._single_click_after_id = None
        self.open_task_detail(task_id, select=False)

    def select_task(self, task_id: int) -> None:
        item = self.store.find_by_id(self.store.tasks, task_id)
        if item is None:
            return
        self._single_click_after_id = None
        self.selected_task_id = task_id
        self.refresh_view()

    def open_task_detail(self, task_id: int, select: bool = True) -> None:
        item = self.store.find_by_id(self.store.tasks, task_id)
        if item is None:
            return
        if select:
            self.selected_task_id = task_id
            self.refresh_view()

        win = tk.Toplevel(self)
        win.title(f"Task Detail #{task_id}")
        win.geometry("560x400")
        win.configure(bg="#f4f4f4")
        win.transient(self)

        wrap = tk.Frame(win, bg="black")
        wrap.place(relx=0.06, rely=0.08, relwidth=0.88, relheight=0.84)
        body = tk.Frame(wrap, bg="#f4f4f4")
        body.place(relx=0.004, rely=0.006, relwidth=0.992, relheight=0.988)

        tk.Label(
            body,
            text=f"Due: {item['dueDate']}",
            bg="#f4f4f4",
            fg="black",
            font=("Times New Roman", 24, "bold"),
            anchor="w",
        ).pack(fill="x", padx=18, pady=(16, 8))
        tk.Label(
            body,
            text=self._due_hint(item["dueDate"]),
            bg="#f4f4f4",
            fg="black",
            font=("SimSun", 18),
            anchor="w",
        ).pack(fill="x", padx=18, pady=(0, 14))

        tk.Frame(body, bg="black", height=2).pack(fill="x")

        tk.Button(
            body,
            text="Edit task",
            bg="#f4f4f4",
            fg="black",
            activebackground="#ebebeb",
            relief="flat",
            font=("SimSun", 24, "bold"),
            anchor="w",
            command=lambda: self.open_edit_window(item, win),
        ).pack(fill="x", padx=16, pady=(14, 14))

        tk.Frame(body, bg="black", height=2).pack(fill="x")

        tk.Button(
            body,
            text="Delete task (red)",
            bg="#f4f4f4",
            fg="#d93131",
            activebackground="#ebebeb",
            relief="flat",
            font=("SimSun", 24, "bold"),
            anchor="w",
            command=lambda: self.delete_task(item["ID"], win),
        ).pack(fill="x", padx=16, pady=(14, 8))


if __name__ == "__main__":
    app = StudyBuddyUI()
    app.mainloop()
