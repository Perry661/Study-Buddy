import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import date
from typing import Optional

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
        tk.Button(btn, text="Edit by ID", width=12, command=self.edit_by_id).pack(side=tk.LEFT, padx=4)
        tk.Button(btn, text="Finish by ID", width=12, command=self.finish_by_id).pack(side=tk.LEFT, padx=4)
        tk.Button(btn, text="Delete by ID", width=12, command=self.delete_by_id).pack(side=tk.LEFT, padx=4)
        tk.Button(btn, text="Restore by ID", width=12, command=self.restore_by_id).pack(side=tk.LEFT, padx=4)
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

        self.active_text = self._build_text_panel(content)
        self.finished_text = self._build_text_panel(content)
        self.trash_text = self._build_text_panel(content)
        self.active_text.grid(row=1, column=0, sticky="nsew", padx=(0, 6))
        self.finished_text.grid(row=1, column=1, sticky="nsew", padx=6)
        self.trash_text.grid(row=1, column=2, sticky="nsew", padx=(6, 0))

        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self, textvariable=self.status_var, bg="#ececec", anchor="w", padx=12, pady=8).pack(fill=tk.X)

    def _build_text_panel(self, parent: tk.Frame) -> tk.Text:
        panel = tk.Text(parent, wrap="word", bg="white", fg="black", relief=tk.SOLID, borderwidth=1)
        panel.configure(state=tk.DISABLED)
        return panel

    def _render_panel(self, widget: tk.Text, rows: list[str]) -> None:
        widget.configure(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        if not rows:
            widget.insert(tk.END, "(empty)\n")
        else:
            widget.insert(tk.END, "\n".join(rows) + "\n")
        widget.configure(state=tk.DISABLED)

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

        active_rows = [
            f'ID {i["ID"]} | {i["task"]} | due {i["dueDate"]} | {i["overDue"]}'
            for i in sorted(self.store.tasks, key=lambda x: x["dueDate"])
        ]
        finished_rows = [
            f'ID {i["ID"]} | {i["task"]} | due {i["dueDate"]}'
            for i in sorted(self.store.finished, key=lambda x: x["dueDate"])
        ]
        trash_rows = [
            f'ID {i["ID"]} | {i["task"]} | due {i["dueDate"]} | trash left {i.get("delete", "")}'
            for i in sorted(self.store.trash, key=lambda x: x["dueDate"])
        ]

        self._render_panel(self.active_text, active_rows)
        self._render_panel(self.finished_text, finished_rows)
        self._render_panel(self.trash_text, trash_rows)
        self.store.save()

    def _ask_id(self, title: str) -> Optional[int]:
        return simpledialog.askinteger(title, "Enter task ID:", parent=self, minvalue=0)

    def add_task(self) -> None:
        task_text = self.task_entry.get().strip()
        due_date = self.due_entry.get().strip()
        if not task_text:
            messagebox.showerror("Invalid task", "Task text cannot be empty.")
            return
        if parse_due_date(due_date) is None:
            messagebox.showerror("Invalid date", "Due date must be YYYY-MM-DD.")
            return
        item = self.store.make_task(task_text, due_date)
        self.store.tasks.append(item)
        self.task_entry.delete(0, tk.END)
        self.refresh_view()
        self.status_var.set(f"Added task #{item['ID']}")

    def edit_by_id(self) -> None:
        task_id = self._ask_id("Edit task")
        if task_id is None:
            return
        item = self.store.find_by_id(self.store.tasks, task_id)
        if item is None:
            messagebox.showerror("Not found", f"Active task ID {task_id} not found.")
            return
        new_task = simpledialog.askstring("Edit task", "Task text:", initialvalue=item["task"], parent=self)
        if new_task is None:
            return
        new_task = new_task.strip()
        if not new_task:
            messagebox.showerror("Invalid task", "Task text cannot be empty.")
            return
        new_due = simpledialog.askstring("Edit due date", "Due date (YYYY-MM-DD):", initialvalue=item["dueDate"], parent=self)
        if new_due is None:
            return
        new_due = new_due.strip()
        if parse_due_date(new_due) is None:
            messagebox.showerror("Invalid date", "Due date must be YYYY-MM-DD.")
            return
        self.store.update_core_fields(item, new_task, new_due)
        self.refresh_view()
        self.status_var.set(f"Edited task #{task_id}")

    def finish_by_id(self) -> None:
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
