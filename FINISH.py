import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import Optional


class FinishTaskMixin:
    def finish_selected(self) -> None:
        if self.selected_task_id is None:
            messagebox.showinfo("Info", "Please click a task first.")
            return
        item = self.store.find_by_id(self.store.tasks, self.selected_task_id)
        if item is None:
            messagebox.showerror("Error", "Selected task not found.")
            return
        self.store.tasks.remove(item)
        item["finish"] = "[FINISHED]"
        item["name"] = f"[FINISHED] Task: {item['task']}, Due date: {item['dueDate']}"
        self.store.finished.append(item)
        self.selected_task_id = None
        self.refresh_view()

    def open_finished_window(self) -> None:
        win = tk.Toplevel(self)
        win.title("Finished Tasks")
        win.geometry("820x460")
        win.configure(bg="#f4f4f4")
        win.transient(self)

        tk.Label(win, text="Finished tasks", bg="#f4f4f4", font=("Times New Roman", 24, "bold")).pack(
            anchor="w", padx=16, pady=(12, 8)
        )

        listbox = tk.Listbox(win, font=("Times New Roman", 15), activestyle="none", selectmode=tk.SINGLE)
        listbox.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        finished_items = sorted(self.store.finished, key=lambda x: x["dueDate"])
        for item in finished_items:
            listbox.insert(tk.END, f'ID {item["ID"]} | {item["task"]} | due {item["dueDate"]}')

        def republish() -> None:
            selected: Optional[dict] = None
            cur = listbox.curselection()
            if cur:
                idx = cur[0]
                if 0 <= idx < len(finished_items):
                    selected = finished_items[idx]

            if selected is None:
                input_id = simpledialog.askinteger(
                    "Republish task",
                    "No task selected.\nEnter finished task ID to republish (Cancel to stop):",
                    parent=win,
                    minvalue=0,
                )
                if input_id is None:
                    return
                selected = self.store.find_by_id(self.store.finished, input_id)
                if selected is None:
                    messagebox.showerror("Error", f"Finished task ID {input_id} not found.", parent=win)
                    return

            new_item = self.store.make_task(selected["task"], selected["dueDate"])
            self.store.tasks.append(new_item)
            self.selected_task_id = int(new_item["ID"])
            self.refresh_view()
            messagebox.showinfo("Republished", f"Republished as active task ID {new_item['ID']}.", parent=win)

        tk.Button(win, text="Republish Task", font=("Times New Roman", 16, "bold"), command=republish).pack(
            pady=(0, 18)
        )
