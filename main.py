from add import Add
from delete import Delete
from dueDateFILE import DueDate
from edit import Edit
import json
import os


if os.path.exists('data.txt'):
    with open('data.txt', 'r', encoding='utf-8') as f:
        try:
            tasks = json.load(f)
        except json.JSONDecodeError:
            tasks = []
else:
    tasks = []  # NEW OBJECT (list)


opts = '0'    # NEW OBJECT (String)
print('\n\nHello!')

while True:
    if opts == '1':
        a = Add(tasks)    # NEW OBJECT (class add.Add)
        a.addTask()

        opts = '0'
        print('\n\n')

    elif opts == '2':
        d = Delete(tasks)   # NEW OBJECT (class delete.Delete)
        d.deleteTask()

        opts = '0'
        print('\n\n')

    elif opts == '3':
        print('\n')

        e = Edit(tasks) # NEW OBJECT (class edit.Edit)

        while True:
            editID, editT = e.editCheck()   # NEW OBJECT (String)

            if editT == '':
                opts = '0'
                print('\n\n')
                break

            if editT == 'task':
                e.editName(editID)
            else:
                e.editDueDate(editID)

        opts = '0'
        print('\n\n')

    elif opts == '4':
        if not tasks:
            print('\n(Nothing is here)')
        else:
            print('\n')
            num = 0 # NEW OBJECT (int)

            for i in tasks:
                print(i["name"])
                num += 1
            
            print(f'\nYou have {num} task(s) left.')

        opts = '0'
        print('\n\n')

    elif opts == '5':
        print('\n')
        if not tasks:
            print('(Nothing is here)')
        else:
            d = DueDate()   # NEW OBJECT (class dueDateFILE.DueDate)
            for j in tasks:
                j['overDue'] = d.overDue(int(j['dueYear']), int(j['dueMonth']), int(j['dueDay']))
                print(f'{j["name"]}\t{j["overDue"]}')
                    
            with open('data.txt', 'w', encoding='utf-8') as f:
                json.dump(tasks, f, ensure_ascii=False, indent=2)


        opts = '0'
        print('\n\n')

    elif opts == '':
        break

    else:
        # menu starts
        print('What do you wanna do today?')
        print('1. Add task(s) \n2. Delete task(s) \n3. Edit task(s) \n4. View task(s) \n5. View due date(s)')

        opts = input('\nEnter your choice here (enter the order number. If end, enter nothing): ')
        # menu ends

tasks.sort(key = lambda x: x["dueDate"])

with open('data.txt', 'w', encoding='utf-8') as f:
    json.dump(tasks, f, ensure_ascii=False, indent=2)

print('\n')

print('Remember to do them! ')
print("Today's task(s): ")

if not tasks:
    print("(Looks like there's no tasks today…)")
else:
    for i in tasks:
        print(i["name"])

print('\n')
