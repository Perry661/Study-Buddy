from save import save_tasks
from add import Add
from delete import Delete
from dueDateFILE import DueDate
from edit import Edit
from finish import Finish
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

def handle_add(tasks: list, path: str) -> None:
    tasks.sort(key=lambda x: x["dueDate"])
    a = Add(tasks)  # NEW OBJECT (class add.Add)
    a.addTask()
    save_tasks(path, tasks)
    print('\n\n')


def delete_check(tasks: list, trash: list, trash_path: str) -> None:
    d = Delete(tasks, trash)  # NEW OBJECT (class delete.Delete)
    changed = d.deleteChecking()    # NEW OBJECT (Boolean)
    if changed:
        save_tasks(trash_path, trash)
    print('\n\n')


def delete_menu() -> str:
    while True:
        print('\nDelete Menu:')
        print('1. Delete \n2. Put back \n3. View having tasks \n4. View deleted tasks')
        opt = input('Enter your option (if end, enter nothing): ')
        if opt == '1' or opt == '2' or opt == '3' or opt == '4' or opt == '':
            return opt
        else:
            print('Option out of range, please re-enter.')


def handle_delete(tasks: list, path: str, trash: list, trash_path: str) -> None:
    tasks.sort(key=lambda x: x["dueDate"])
    d = Delete(tasks, trash)  # NEW OBJECT (class delete.Delete)
    d.deleteTask()
    save_tasks(path, tasks)
    save_tasks(trash_path, trash)
    print('\n\n')


def handle_put_back(tasks: list, path: str, trash: list, trash_path: str):
    tasks.sort(key=lambda x: x["dueDate"])
    d = Delete(tasks, trash)  # NEW OBJECT (class delete.Delete)
    d.putBack()
    save_tasks(path, tasks)
    save_tasks(trash_path, trash)
    print('\n\n')


def handle_edit(tasks: list, path: str) -> None:
    print('\n')
    tasks.sort(key=lambda x: x["dueDate"])
    e = Edit(tasks, path)  # NEW OBJECT (class edit.Edit)

    while True:
        editID, editT = e.editCheck()  # NEW OBJECT (String)
        if editT == '':
            break

        if editT == 'task':
            e.editName(editID)
        else:
            e.editDueDate(editID)

    save_tasks(path, tasks)
    print('\n\n')


def handle_view(tasks: list) -> int:
    print('\n')
    tasks.sort(key=lambda x: x["dueDate"])
    num = 0  # NEW OBJECT (int)
    if not tasks:
        print('\n(Nothing is here)')
    else:
        for i in tasks:
            print(i["name"])
            num += 1
    return num


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
    print('1. Add task(s) \n2. Edit task(s) \n3. Delete or put back task(s) \n4. View task(s) \n5. View due date(s) \n6. Finish task(s)')
    return input('\nEnter your choice here (enter the order number. If end, enter nothing): ')


def show_summary(tasks: list, path: str) -> None:
    tasks.sort(key=lambda x: x["dueDate"])
    save_tasks(path, tasks)
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
    data_path = 'data.json'
    data_finish_path = 'dataFINISHED.json'
    trash_path = 'trash.json'
    # or enter your saving file

    tasks = load_tasks(data_path)   # NEW OBJECT (list)
    taskFINISHED = load_tasks(data_finish_path) # NEW OBJECT (list)
    trash = load_tasks(trash_path)  # NEW OBJECT (list)

    delete_check(tasks, trash, trash_path)

    opts = '0'  # NEW OBJECT (String)
    print('\n\nHello!')

    while True:
        if opts == '1':
            handle_add(tasks, data_path)
            opts = '0'
        elif opts == '2':
            handle_edit(tasks, data_path)
            opts = '0'
        elif opts == '3':
            while True:
                delete_opt = delete_menu()
                if delete_opt == '1':
                    handle_delete(tasks, data_path, trash, trash_path)
                elif delete_opt == '2':
                    handle_put_back(tasks, data_path, trash, trash_path)
                elif delete_opt == '3':
                    handle_view(tasks)
                elif delete_opt == '4':
                    handle_view(trash) 
                else:
                    break
            opts = '0'
        elif opts == '4':
            num = handle_view(tasks)    # NEW OBJECT (int)
            print(f'\nYou have {num} task(s) left.')
            print('\n\n')
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
    show_summary(tasks, data_path)


if __name__ == "__main__": main()
