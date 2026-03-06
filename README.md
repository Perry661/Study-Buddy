# Study-Buddy
A function to list what you are going to do today (kind of like a ToDo list).

***

## Requirements
- Python 3.10+ (recommended: Python 3.12)
- Pillow (required for background image upload: PNG/JPEG/JPG/GIF/WebP)

Install dependency:

```bash
pip3 install pillow
```

## Run (GUI)
```bash
python3 UI.py
```

Core GUI files:
- `UI.py`: Tkinter window + UI actions.
- `ui_data.py`: load/save/normalize task data for GUI.

Data files:
- `data.json`: active tasks
- `dataFINISHED.json`: finished tasks
- `trash.json`: trash tasks

Legacy CLI files were moved to `legacy/` and are not required for GUI runtime.

## UI Run Reminder
- If `UI.py` opens but the window is blank/unresponsive, the most common reason is Python interpreter mismatch.
- In VS Code, the top-left Run button may use a different interpreter than your terminal.
- Recommended launch command:

```bash
python3 UI.py
```

- In VS Code, also set interpreter manually:
  - `Cmd + Shift + P` -> `Python: Select Interpreter`
  - Pick the same Python used by your terminal.
