from save import data_path, data_finish_path, save_tasks
from add import Add
from delete import Delete
from dueDateFILE import DueDate
from edit import Edit
from finish import Finish
import os
import json
from datetime import date


data_path = 'data.json'
data_finish_path = 'dataFINISHED.json'
trash_path = 'trash.json'
# or enter your saving file


def load_tasks(path: str) -> list:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []  # NEW OBJECT (list)

def handle_add(tasks: list, path: str) -> None:
    tasks.sort(key=lambda x: x["dueDate"])
    a = Add(tasks)  # NEW OBJECT (class add.Add)
    a.addTask()
    save_tasks(path, tasks)
    print('\n\n')


def handle_delete(tasks: list, path: str, trash: list, trash_path: str) -> None:
    tasks.sort(key=lambda x: x["dueDate"])
    d = Delete(tasks)  # NEW OBJECT (class delete.Delete)
    d.deleteTask(trash, trash_path)
    save_tasks(path, tasks)
    save_tasks(trash_path, trash)
    print('\n\n')


def delete_check(trash: list, trash_path: str) -> None:
    today = date.today()    # NEW OBJECT (date)
    changed = False # NEW OBJECT (Boolean)
    keptTrash = []  # NEW OBJECT (list)

    for i in trash:
        remainDays = i.get('delete', 0)   # NEW OBJECT (any)
        # get "delete" value in the list. If no, then use 0.
        try:
            remainingInt = int(remainDays)
        except (TypeError, ValueError):
            remainingInt = 0    # NEW OBJECT (int)

        deleteDate = i.get('deleteDate')   # NEW OBJECT (date)
        if isinstance(deleteDate, str) and deleteDate:
        # check if deleteDate is str type
            try:
                last_date = date.fromisoformat(deleteDate)    # NEW OBJECT (date)
                # change deleteDate to date form
            except ValueError:
                last_date = today
        elif isinstance(deleteDate, date):
            last_date = deleteDate
        else:
            last_date = today

        days_passed = (today - last_date).days  # NEW OBJECT (int)
        if days_passed > 0:
            remainingInt -= days_passed
            changed = True

        if remainingInt > 0:
            if i.get('delete') != remainingInt:
                i['delete'] = remainingInt
                changed = True
            todayStr = today.isoformat()   # NEW OBJECT (str)
            # change today to str type
            if i.get('deleteDate') != todayStr:
                i['deleteDate'] = todayStr
                changed = True
            keptTrash.append(i)
        else:
            changed = True

    if len(keptTrash) != len(trash):
        trash[:] = keptTrash

    if changed:
        save_tasks(trash_path, trash)


def handle_edit(tasks: list) -> None:
    print('\n')
    tasks.sort(key=lambda x: x["dueDate"])
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

    save_tasks(data_path, tasks)

    print('\n\n')


def handle_view(tasks: list) -> None:
    print('\n')
    tasks.sort(key=lambda x: x["dueDate"])
    if not tasks:
        print('\n(Nothing is here)')
    else:
        num = 0  # NEW OBJECT (int)
        for i in tasks:
            print(i["name"])
            num += 1
        print(f'\nYou have {num} task(s) left.')
    print('\n\n')


def handle_due_dates(tasks: list, path: str) -> None:
    print('\n')
    tasks.sort(key=lambda x: x["dueDate"])
    if not tasks:
        print('(Nothing is here)')
    else:
        d = DueDate()  # NEW OBJECT (class dueDateFILE.DueDate)
        for j in tasks:
            j['overDue'] = d.overDue(int(j['dueYear']), int(j['dueMonth']), int(j['dueDay']))
            print(f'{j["name"]}\t{j["overDue"]}')
        save_tasks(path, tasks)
    print('\n\n')


def handle_finish_task(tasks: list, path: str, taskFINISH: list, pathFINISH: str) -> None:
    print('\n')
    if not tasks:
        print('(Nothing is here)')
    else:
        while True:
            f = Finish(tasks)   # NEW OBJECT (class finish.Finish)
            finishID = f.finishCheck()  # NEW OBJECT (int | None)
            if finishID is not None:
                f.finishTask(finishID, taskFINISH)
            else:
                break
        save_tasks(path, tasks)
        save_tasks(pathFINISH, taskFINISH)
        print('\n\n')


def prompt_menu() -> str:
    print('What do you wanna do today?')
    print('1. Add task(s) \n2. Delete task(s) \n3. Edit task(s) \n4. View task(s) \n5. View due date(s) \n6. Finish task(s)')
    return input('\nEnter your choice here (enter the order number. If end, enter nothing): ')


def show_summary(tasks: list) -> None:
    tasks.sort(key=lambda x: x["dueDate"])
    save_tasks(data_path, tasks)
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
    tasks = load_tasks(data_path)   # NEW OBJECT (list)
    taskFINISHED = load_tasks(data_finish_path) # NEW OBJECT (list)
    trash = load_tasks(trash_path)  # NEW OBJECT (list)

    delete_check(trash, trash_path)

    opts = '0'  # NEW OBJECT (String)
    print('\n\nHello!')

    while True:
        if opts == '1':
            handle_add(tasks, data_path)
            opts = '0'
        elif opts == '2':
            handle_delete(tasks, data_path, trash, trash_path)
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
        elif opts == '6':
            handle_finish_task(tasks, data_path, taskFINISHED, data_finish_path)
            opts = '0'
        elif opts == '':
            break
        else:
            opts = prompt_menu()

    save_tasks(data_path, tasks)
    show_summary(tasks)


main()
