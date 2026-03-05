import tkinter as tk
from datetime import date
from tkinter import messagebox
from typing import Optional


class DeleteTaskMixin:
    def delete_task(self, task_id: int, detail_window: Optional[tk.Toplevel] = None) -> None:
        item = self.store.find_by_id(self.store.tasks, task_id)
        if item is None:
            messagebox.showerror("Error", "Task not found.")
            return
        if not messagebox.askyesno("Confirm Delete", f"Delete task '{item['task']}'?", parent=self):
            return
        self.store.tasks.remove(item)
        item["delete"] = 30
        item["deleteDate"] = date.today().isoformat()
        self.store.trash.append(item)
        self.selected_task_id = None
        self.refresh_view()
        if detail_window is not None:
            detail_window.destroy()

    def open_trash_window(self) -> None:
        self.store.apply_trash_countdown()
        win = tk.Toplevel(self)
        win.title("Trash")
        win.geometry("760x420")
        win.configure(bg="#f4f4f4")
        win.transient(self)

        tk.Label(win, text="Trash (restore / delete forever)", bg="#f4f4f4", font=("SimSun", 20, "bold")).pack(
            anchor="w", padx=16, pady=(12, 8)
        )

        listbox = tk.Listbox(win, font=("Times New Roman", 15), activestyle="none", selectmode=tk.SINGLE)
        listbox.pack(fill="both", expand=True, padx=16, pady=8)

        trash_items = sorted(self.store.trash, key=lambda x: x["dueDate"])
        for t in trash_items:
            listbox.insert(tk.END, f'ID {t["ID"]} | {t["task"]} | due {t["dueDate"]} | {t.get("delete", "")} day(s) left')

        def selected_item() -> Optional[dict]:
            cur = listbox.curselection()
            if not cur:
                return None
            idx = cur[0]
            if idx < 0 or idx >= len(trash_items):
                return None
            return trash_items[idx]

        buttons = tk.Frame(win, bg="#f4f4f4")
        buttons.pack(fill="x", padx=16, pady=(0, 16))

        def restore() -> None:
            item = selected_item()
            if item is None:
                messagebox.showinfo("Info", "Please select a task first.", parent=win)
                return
            self.store.trash.remove(item)
            item["delete"] = ""
            item["deleteDate"] = ""
            self.store.tasks.append(item)
            self.refresh_view()
            win.destroy()

        def delete_forever() -> None:
            item = selected_item()
            if item is None:
                messagebox.showinfo("Info", "Please select a task first.", parent=win)
                return
            if not messagebox.askyesno("Confirm Permanent Delete", f"Delete '{item['task']}' permanently?", parent=win):
                return
            self.store.trash.remove(item)
            self.refresh_view()
            win.destroy()

        tk.Button(buttons, text="Restore", font=("SimSun", 14, "bold"), command=restore).pack(side="left")
        tk.Button(buttons, text="Delete Forever", fg="#d93131", font=("SimSun", 14, "bold"), command=delete_forever).pack(
            side="left", padx=14
        )
