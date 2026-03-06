import re
import tkinter as tk
from datetime import date
from tkinter import messagebox
from typing import Optional

from ui_data import parse_due_date


class AddTaskMixin:
    def _normalize_due_input(self, raw: str) -> Optional[str]:
        text = raw.strip()
        if not text:
            return None

        m = re.match(r"^(\d{4})\D(\d{1,2})\D(\d{1,2})$", text)
        if m:
            year, month, day = m.groups()
            normalized = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
            return normalized if parse_due_date(normalized) is not None else None

        if re.match(r"^\d{8}$", text):
            normalized = f"{text[0:4]}-{text[4:6]}-{text[6:8]}"
            return normalized if parse_due_date(normalized) is not None else None

        return None

    def open_add_window(self) -> None:
        win = tk.Toplevel(self)
        win.title("Add Task")
        win.geometry("500x260")
        win.configure(bg="#f4f4f4")
        win.transient(self)
        win.grab_set()

        tk.Label(win, text="Task", bg="#f4f4f4", font=("SimSun", 18, "bold")).pack(anchor="w", padx=24, pady=(24, 6))
        task_entry = tk.Entry(win, font=("SimSun", 18))
        task_entry.pack(fill="x", padx=24)

        tk.Label(win, text="Due date (YYYY-MM-DD)", bg="#f4f4f4", font=("Times New Roman", 16, "bold")).pack(
            anchor="w", padx=24, pady=(16, 6)
        )
        due_entry = tk.Entry(win, font=("Times New Roman", 16))
        due_entry.insert(0, date.today().isoformat())
        due_entry.pack(fill="x", padx=24)

        def submit() -> None:
            task_text = task_entry.get().strip()
            due_date = self._normalize_due_input(due_entry.get())
            if not task_text:
                messagebox.showerror("Error", "Task text cannot be empty.", parent=win)
                return
            if due_date is None:
                messagebox.showerror("Error", "Invalid date. Use YYYY-MM-DD.", parent=win)
                return

            # Keep legacy ID behavior: use max ID across active + trash + finished.
            self.store.tasks.append(self.store.make_task(task_text, due_date))
            self.selected_task_id = None
            self.refresh_view()
            win.destroy()

        tk.Button(win, text="Add", font=("SimSun", 16, "bold"), command=submit).pack(pady=22)

    def open_edit_window(self, item: dict, parent: tk.Toplevel) -> None:
        win = tk.Toplevel(parent)
        win.title("Edit Task")
        win.geometry("520x280")
        win.configure(bg="#f4f4f4")
        win.transient(parent)
        win.grab_set()

        tk.Label(win, text="Task", bg="#f4f4f4", font=("SimSun", 18, "bold")).pack(anchor="w", padx=24, pady=(24, 6))
        task_entry = tk.Entry(win, font=("SimSun", 18))
        task_entry.insert(0, item["task"])
        task_entry.pack(fill="x", padx=24)

        tk.Label(win, text="Due date (YYYY-MM-DD)", bg="#f4f4f4", font=("Times New Roman", 16, "bold")).pack(
            anchor="w", padx=24, pady=(16, 6)
        )
        due_entry = tk.Entry(win, font=("Times New Roman", 16))
        due_entry.insert(0, item["dueDate"])
        due_entry.pack(fill="x", padx=24)

        def submit() -> None:
            task_text = task_entry.get().strip()
            due_date = self._normalize_due_input(due_entry.get())
            if not task_text:
                messagebox.showerror("Error", "Task text cannot be empty.", parent=win)
                return
            if due_date is None:
                messagebox.showerror("Error", "Invalid date. Use YYYY-MM-DD.", parent=win)
                return
            self.store.update_core_fields(item, task_text, due_date)
            self.refresh_view()
            win.destroy()

        tk.Button(win, text="Save", font=("SimSun", 16, "bold"), command=submit).pack(pady=22)
