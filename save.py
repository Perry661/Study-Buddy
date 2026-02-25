import json

data_path = 'data.json'
data_finish_path = 'dataFINISHED.json'
# or enter your saving file

def save_tasks(path: str, t: list) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(t, f, ensure_ascii=False, indent=2)


def save_finish_tasks(path: str, t: list):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(t, f, ensure_ascii=False, indent=2)