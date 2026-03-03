import json
import os
from datetime import date, datetime
from typing import Optional


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")
FINISHED_FILE = os.path.join(BASE_DIR, "dataFINISHED.json")
TRASH_FILE = os.path.join(BASE_DIR, "trash.json")


def parse_due_date(due_date: str) -> Optional[date]:
    try:
        return datetime.strptime(due_date, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def build_overdue_text(due_date: str) -> str:
    ddl = parse_due_date(due_date)
    if ddl is None:
        return ""
    today = date.today()
    if ddl > today:
        return f"There is {(ddl - today).days} day(s) left."
    if ddl == today:
        return "It's due today!! (HURRY UP!!!)"
    return "[OVERDUE] It's already due... (Mourn...)"


def _load_json(path: str) -> list:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []
    return data if isinstance(data, list) else []


def _save_json(path: str, data: list) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _normalize_task(raw: dict, fallback_id: int) -> dict:
    task_id = raw.get("ID", fallback_id)
    task_text = str(raw.get("task", "")).strip()
    due_date = str(raw.get("dueDate", "")).strip()
    name_text = str(raw.get("name", "")).strip()

    if not task_text and "Task:" in name_text:
        extracted = name_text
        if extracted.startswith("[FINISHED] "):
            extracted = extracted[len("[FINISHED] "):]
        extracted = extracted.replace("Task:", "", 1).strip()
        if ", Due date:" in extracted:
            extracted = extracted.split(", Due date:", 1)[0].strip()
        task_text = extracted

    if not due_date or parse_due_date(due_date) is None:
        due_date = date.today().isoformat()

    due = parse_due_date(due_date) or date.today()
    finish_tag = str(raw.get("finish", "")).strip()
    name = f"Task: {task_text}, Due date: {due_date}"
    if finish_tag == "[FINISHED]":
        name = f"[FINISHED] {name}"

    return {
        "ID": int(task_id),
        "name": name,
        "task": task_text,
        "dueDate": due_date,
        "dueYear": str(due.year),
        "dueMonth": str(due.month),
        "dueDay": str(due.day),
        "overDue": build_overdue_text(due_date),
        "finish": finish_tag,
        "delete": raw.get("delete", ""),
        "deleteDate": raw.get("deleteDate", ""),
    }


class TaskStore:
    def __init__(self) -> None:
        self.tasks: list[dict] = []
        self.finished: list[dict] = []
        self.trash: list[dict] = []

    def load(self) -> None:
        active_raw = _load_json(DATA_FILE)
        finished_raw = _load_json(FINISHED_FILE)
        trash_raw = _load_json(TRASH_FILE)

        self.tasks = [_normalize_task(item, idx) for idx, item in enumerate(active_raw)]
        self.finished = [_normalize_task(item, idx) for idx, item in enumerate(finished_raw)]
        self.trash = [_normalize_task(item, idx) for idx, item in enumerate(trash_raw)]
        self.apply_trash_countdown()
        self.save()

    def save(self) -> None:
        _save_json(DATA_FILE, self.tasks)
        _save_json(FINISHED_FILE, self.finished)
        _save_json(TRASH_FILE, self.trash)

    def next_id(self) -> int:
        items = self.tasks + self.finished + self.trash
        return max((int(i.get("ID", 0)) for i in items), default=-1) + 1

    def find_by_id(self, source: list[dict], task_id: int) -> Optional[dict]:
        return next((i for i in source if i["ID"] == task_id), None)

    def apply_trash_countdown(self) -> None:
        today = date.today()
        kept: list[dict] = []
        for item in self.trash:
            remain = item.get("delete", 30)
            try:
                remain_int = int(remain)
            except (TypeError, ValueError):
                remain_int = 30

            delete_date = item.get("deleteDate", "")
            try:
                last_date = date.fromisoformat(delete_date) if delete_date else today
            except ValueError:
                last_date = today

            passed = (today - last_date).days
            if passed > 0:
                remain_int -= passed

            if remain_int > 0:
                item["delete"] = remain_int
                item["deleteDate"] = today.isoformat()
                kept.append(item)

        self.trash = kept

    def make_task(self, task_text: str, due_date: str) -> dict:
        due = parse_due_date(due_date)
        if due is None:
            raise ValueError("Invalid date format, expected YYYY-MM-DD.")
        item = _normalize_task(
            {
                "ID": self.next_id(),
                "task": task_text,
                "dueDate": due_date,
                "finish": "",
                "delete": "",
                "deleteDate": "",
            },
            fallback_id=self.next_id(),
        )
        return item

    def update_core_fields(self, item: dict, task_text: str, due_date: str) -> None:
        due = parse_due_date(due_date)
        if due is None:
            raise ValueError("Invalid date format, expected YYYY-MM-DD.")
        item["task"] = task_text
        item["dueDate"] = due_date
        item["dueYear"] = str(due.year)
        item["dueMonth"] = str(due.month)
        item["dueDay"] = str(due.day)
        item["overDue"] = build_overdue_text(due_date)
        if item.get("finish") == "[FINISHED]":
            item["name"] = f"[FINISHED] Task: {task_text}, Due date: {due_date}"
        else:
            item["name"] = f"Task: {task_text}, Due date: {due_date}"

