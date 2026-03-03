import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import date
from typing import Optional
import re

from ui_data import TaskStore, build_overdue_text, parse_due_date


class StudyBuddyUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Study Buddy")
        self.geometry("1200x760")
        self.minsize(1000, 620)
        self.configure(bg="#ececec")

        self.store = TaskStore()
        self._build_widgets()
        self.reload_from_disk()

    def _build_widgets(self) -> None:
        top = tk.Frame(self, bg="#ececec", padx=12, pady=10)
        top.pack(fill=tk.X)

        tk.Label(top, text="Task:", bg="#ececec", fg="black").grid(row=0, column=0, sticky="w")
        self.task_entry = tk.Entry(top, width=60)
        self.task_entry.grid(row=0, column=1, sticky="ew", padx=(6, 10))

        tk.Label(top, text="Due (YYYY-MM-DD):", bg="#ececec", fg="black").grid(row=0, column=2, sticky="w")
        self.due_entry = tk.Entry(top, width=14)
        self.due_entry.grid(row=0, column=3, sticky="w", padx=(6, 0))
        self.due_entry.insert(0, date.today().isoformat())
        top.grid_columnconfigure(1, weight=1)

        btn = tk.Frame(self, bg="#ececec", padx=12, pady=0)
        btn.pack(fill=tk.X, pady=(0, 8))
        tk.Button(btn, text="Add", width=12, command=self.add_task).pack(side=tk.LEFT, padx=4)
        tk.Button(btn, text="Edit Selected", width=12, command=self.edit_by_id).pack(side=tk.LEFT, padx=4)
        tk.Button(btn, text="Finish Selected", width=12, command=self.finish_by_id).pack(side=tk.LEFT, padx=4)
        tk.Button(btn, text="Delete Selected", width=12, command=self.delete_by_id).pack(side=tk.LEFT, padx=4)
        tk.Button(btn, text="Restore Selected", width=12, command=self.restore_by_id).pack(side=tk.LEFT, padx=4)
        tk.Button(btn, text="Reload", width=12, command=self.reload_from_disk).pack(side=tk.LEFT, padx=4)

        content = tk.Frame(self, bg="#ececec", padx=12, pady=8)
        content.pack(fill=tk.BOTH, expand=True)
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.columnconfigure(2, weight=1)
        content.rowconfigure(1, weight=1)

        tk.Label(content, text="Active", bg="#ececec", fg="black").grid(row=0, column=0, sticky="w")
        tk.Label(content, text="Finished", bg="#ececec", fg="black").grid(row=0, column=1, sticky="w")
        tk.Label(content, text="Trash", bg="#ececec", fg="black").grid(row=0, column=2, sticky="w")

        active_wrap, self.active_list = self._build_list_panel(content)
        finished_wrap, self.finished_list = self._build_list_panel(content)
        trash_wrap, self.trash_list = self._build_list_panel(content)
        active_wrap.grid(row=1, column=0, sticky="nsew", padx=(0, 6))
        finished_wrap.grid(row=1, column=1, sticky="nsew", padx=6)
        trash_wrap.grid(row=1, column=2, sticky="nsew", padx=(6, 0))
        self.active_list.bind("<Double-Button-1>", lambda _event: self.edit_by_id())
        self.trash_list.bind("<Double-Button-1>", lambda _event: self.restore_by_id())

        self.active_ids: list[int] = []
        self.finished_ids: list[int] = []
        self.trash_ids: list[int] = []

        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self, textvariable=self.status_var, bg="#ececec", anchor="w", padx=12, pady=8).pack(fill=tk.X)

    def _build_list_panel(self, parent: tk.Frame) -> tuple[tk.Frame, tk.Listbox]:
        wrapper = tk.Frame(parent, bg="#ececec")
        wrapper.grid_rowconfigure(0, weight=1)
        wrapper.grid_columnconfigure(0, weight=1)
        listbox = tk.Listbox(
            wrapper,
            bg="white",
            fg="black",
            relief=tk.SOLID,
            borderwidth=1,
            selectmode=tk.SINGLE,
            activestyle="none",
            exportselection=False,
            width=40,
            height=20,
        )
        scrollbar = tk.Scrollbar(wrapper, orient=tk.VERTICAL, command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)
        listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        return wrapper, listbox

    def _render_panel(self, widget: tk.Listbox, rows: list[str]) -> None:
        widget.delete(0, tk.END)
        if not rows:
            widget.insert(tk.END, "(empty)")
        else:
            for row in rows:
                widget.insert(tk.END, row)

    def reload_from_disk(self) -> None:
        self.store.load()
        print(
            f"[UI] loaded from disk: active={len(self.store.tasks)}, "
            f"finished={len(self.store.finished)}, trash={len(self.store.trash)}"
        )
        self.refresh_view()
        self.status_var.set(
            f"Reloaded: active {len(self.store.tasks)}, finished {len(self.store.finished)}, trash {len(self.store.trash)}"
        )

    def refresh_view(self) -> None:
        for item in self.store.tasks:
            item["overDue"] = build_overdue_text(item["dueDate"])

        active_items = sorted(self.store.tasks, key=lambda x: x["dueDate"])
        finished_items = sorted(self.store.finished, key=lambda x: x["dueDate"])
        trash_items = sorted(self.store.trash, key=lambda x: x["dueDate"])

        active_rows = [f'ID {i["ID"]} | {i["task"]} | due {i["dueDate"]} | {i["overDue"]}' for i in active_items]
        finished_rows = [f'ID {i["ID"]} | {i["task"]} | due {i["dueDate"]}' for i in finished_items]
        trash_rows = [
            f'ID {i["ID"]} | {i["task"]} | due {i["dueDate"]} | trash left {i.get("delete", "")}'
            for i in trash_items
        ]

        self.active_ids = [int(i["ID"]) for i in active_items]
        self.finished_ids = [int(i["ID"]) for i in finished_items]
        self.trash_ids = [int(i["ID"]) for i in trash_items]

        self._render_panel(self.active_list, active_rows)
        self._render_panel(self.finished_list, finished_rows)
        self._render_panel(self.trash_list, trash_rows)
        self.store.save()

    def _ask_id(self, title: str) -> Optional[int]:
        return simpledialog.askinteger(title, "Enter task ID:", parent=self, minvalue=0)

    def _selected_id(self, source: str) -> Optional[int]:
        if source == "active":
            box, ids = self.active_list, self.active_ids
        elif source == "trash":
            box, ids = self.trash_list, self.trash_ids
        else:
            return None

        selected = box.curselection()
        if not selected:
            return None
        idx = selected[0]
        if idx < 0 or idx >= len(ids):
            return None
        return ids[idx]

    def _normalize_due_input(self, raw: str) -> Optional[str]:
        text = raw.strip()
        if not text:
            return None

        # Accept common variants like 2026-3-4 / 2026/3/4 / 2026.3.4 and normalize.
        m = re.match(r"^(\d{4})\D(\d{1,2})\D(\d{1,2})$", text)
        if m:
            year, month, day = m.groups()
            normalized = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
            return normalized if parse_due_date(normalized) is not None else None

        # Accept compact numeric date like 20260304.
        if re.match(r"^\d{8}$", text):
            normalized = f"{text[0:4]}-{text[4:6]}-{text[6:8]}"
            return normalized if parse_due_date(normalized) is not None else None

        return None

    def add_task(self) -> None:
        task_text = self.task_entry.get().strip()
        due_date = self._normalize_due_input(self.due_entry.get())
        if not task_text:
            messagebox.showerror("Invalid task", "Task text cannot be empty.")
            return
        if due_date is None:
            messagebox.showerror("Invalid date", "Invalid date. Use a real date like 2026-03-04.")
            return
        self.due_entry.delete(0, tk.END)
        self.due_entry.insert(0, due_date)
        item = self.store.make_task(task_text, due_date)
        self.store.tasks.append(item)
        self.task_entry.delete(0, tk.END)
        self.refresh_view()
        self.status_var.set(f"Added task #{item['ID']}")

    def edit_by_id(self) -> None:
        task_id = self._selected_id("active")
        if task_id is None:
            task_id = self._ask_id("Edit task")
        if task_id is None:
            return
        item = self.store.find_by_id(self.store.tasks, task_id)
        if item is None:
            messagebox.showerror("Not found", f"Active task ID {task_id} not found.")
            return

        opt = simpledialog.askstring(
            "Edit task",
            "What do you want to edit?\n1. Name\n2. Due date",
            parent=self,
        )
        if opt is None:
            return
        opt = opt.strip()

        if opt == "1":
            new_task = simpledialog.askstring("Edit task name", "Task text:", initialvalue=item["task"], parent=self)
            if new_task is None:
                return
            new_task = new_task.strip()
            if not new_task:
                messagebox.showerror("Invalid task", "Task text cannot be empty.")
                return
            self.store.update_core_fields(item, new_task, item["dueDate"])
            self.refresh_view()
            self.status_var.set(f"Edited task name #{task_id}")
            return

        if opt == "2":
            new_due_raw = simpledialog.askstring(
                "Edit due date",
                "Due date (YYYY-MM-DD):",
                initialvalue=item["dueDate"],
                parent=self,
            )
            if new_due_raw is None:
                return
            new_due = self._normalize_due_input(new_due_raw)
            if new_due is None:
                messagebox.showerror("Invalid date", "Invalid date. Use a real date like 2026-03-04.")
                return
            self.store.update_core_fields(item, item["task"], new_due)
            self.refresh_view()
            self.status_var.set(f"Edited due date #{task_id}")
            return

        messagebox.showerror("Invalid option", "Please enter 1 (Name) or 2 (Due date).")

    def finish_by_id(self) -> None:
        task_id = self._selected_id("active")
        if task_id is None:
            task_id = self._ask_id("Finish task")
        if task_id is None:
            return
        item = self.store.find_by_id(self.store.tasks, task_id)
        if item is None:
            messagebox.showerror("Not found", f"Active task ID {task_id} not found.")
            return
        self.store.tasks.remove(item)
        item["finish"] = "[FINISHED]"
        item["name"] = f"[FINISHED] Task: {item['task']}, Due date: {item['dueDate']}"
        self.store.finished.append(item)
        self.refresh_view()
        self.status_var.set(f"Finished task #{task_id}")

    def delete_by_id(self) -> None:
        from datetime import date

        task_id = self._selected_id("active")
        if task_id is None:
            task_id = self._ask_id("Delete task")
        if task_id is None:
            return
        item = self.store.find_by_id(self.store.tasks, task_id)
        if item is None:
            messagebox.showerror("Not found", f"Active task ID {task_id} not found.")
            return
        self.store.tasks.remove(item)
        item["delete"] = 30
        item["deleteDate"] = date.today().isoformat()
        self.store.trash.append(item)
        self.refresh_view()
        self.status_var.set(f"Moved task #{task_id} to trash")

    def restore_by_id(self) -> None:
        task_id = self._selected_id("trash")
        if task_id is None:
            task_id = self._ask_id("Restore task")
        if task_id is None:
            return
        item = self.store.find_by_id(self.store.trash, task_id)
        if item is None:
            messagebox.showerror("Not found", f"Trash task ID {task_id} not found.")
            return
        self.store.trash.remove(item)
        item["delete"] = ""
        item["deleteDate"] = ""
        self.store.tasks.append(item)
        self.refresh_view()
        self.status_var.set(f"Restored task #{task_id}")


if __name__ == "__main__":
    app = StudyBuddyUI()
    app.mainloop()
