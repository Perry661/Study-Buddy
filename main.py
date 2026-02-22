from save import data_path, save_tasks
from add import Add
from delete import Delete
from dueDateFILE import DueDate
from edit import Edit
import os
import json


def load_tasks(path: str) -> list:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []  # NEW OBJECT (list)

def handle_add(tasks: list) -> None:
    a = Add(tasks)  # NEW OBJECT (class add.Add)
    a.addTask()
    print('\n\n')


def handle_delete(tasks: list) -> None:
    d = Delete(tasks)  # NEW OBJECT (class delete.Delete)
    d.deleteTask()
    print('\n\n')


def handle_edit(tasks: list) -> None:
    print('\n')
    e = Edit(tasks)  # NEW OBJECT (class edit.Edit)

    while True:
        editID, editT = e.editCheck()  # NEW OBJECT (String)
        if editT == '':
            print('\n\n')
            break

        if editT == 'task':
            e.editName(editID)
        else:
            e.editDueDate(editID)

    print('\n\n')


def handle_view(tasks: list) -> None:
    if not tasks:
        print('\n(Nothing is here)')
    else:
        print('\n')
        num = 0  # NEW OBJECT (int)
        for i in tasks:
            print(i["name"])
            num += 1
        print(f'\nYou have {num} task(s) left.')
    print('\n\n')


def handle_due_dates(tasks: list, path: str) -> None:
    print('\n')
    if not tasks:
        print('(Nothing is here)')
    else:
        d = DueDate()  # NEW OBJECT (class dueDateFILE.DueDate)
        for j in tasks:
            j['overDue'] = d.overDue(int(j['dueYear']), int(j['dueMonth']), int(j['dueDay']))
            print(f'{j["name"]}\t{j["overDue"]}')
        save_tasks(path, tasks)
    print('\n\n')


def prompt_menu() -> str:
    print('What do you wanna do today?')
    print('1. Add task(s) \n2. Delete task(s) \n3. Edit task(s) \n4. View task(s) \n5. View due date(s)')
    return input('\nEnter your choice here (enter the order number. If end, enter nothing): ')


def show_summary(tasks: list) -> None:
    tasks.sort(key=lambda x: x["dueDate"])
    print('\n')
    print('Remember to do them! ')
    print("Today's task(s): ")
    if not tasks:
        print("(Looks like there's no tasks today…)")
    else:
        for i in tasks:
            print(i["name"])
    print('\n')


def main() -> None:
    tasks = load_tasks(data_path)

    opts = '0'  # NEW OBJECT (String)
    print('\n\nHello!')

    while True:
        if opts == '1':
            handle_add(tasks)
            opts = '0'
        elif opts == '2':
            handle_delete(tasks)
            opts = '0'
        elif opts == '3':
            handle_edit(tasks)
            opts = '0'
        elif opts == '4':
            handle_view(tasks)
            opts = '0'
        elif opts == '5':
            handle_due_dates(tasks, data_path)
            opts = '0'
        elif opts == '':
            break
        else:
            # menu starts
            opts = prompt_menu()
            # menu ends

    save_tasks(data_path, tasks)
    show_summary(tasks)


main()
