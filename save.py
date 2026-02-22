import json

data_path = 'data.txt'  # or enter your saving file

def save_tasks(path: str, t: list) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(t, f, ensure_ascii=False, indent=2)
