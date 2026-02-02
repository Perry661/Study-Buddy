from inputTask import InputTask
from delete import removeTask
from dueDateFILE import DueDate
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
        AddTask = InputTask(tasks)    # NEW OBJECT (class inputTask.InputTask)
        AddTask.Add()

        opts = '0'
        print('\n\n')

    elif opts == '2':
        DeleteTask = removeTask(tasks)   # NEW OBJECT (class delete.removeTask)
        DeleteTask.Delete()

        opts = '0'
        print('\n\n')

    elif opts == '3':
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

    elif opts == '4':
        print('\n')
        if not tasks:
            print('(Nothing is here)')
        else:
            d = DueDate()   # NEW OBJECT (class dueDateFILE.DueDate)
            for j in tasks:
                j['overDue'] = d.overDue(int(j['dueYear']), int(j['dueMonth']), int(j['dueDay']))
                print(j["name"] + ', ' + j["overDue"])

            with open('data.txt', 'w', encoding='utf-8') as f:
                json.dump(tasks, f, ensure_ascii=False, indent=2)

        print('\n')

        opts = '0'
        print('\n\n')

    elif opts == 'end':
        break

    else:
        # menu starts
        print('What do you wanna do today?')
        print('1. Add task(s) \n2. Delete task(s) \n3. View task(s) \n4. View due date(s)')
        # TODO 第三项先空着，回头加日期排序功能的时候别忘了这儿
        opts = input('\nEnter your choice here (enter the order number. If end, enter "end"): ')
        # menu ends


print('Ok! Remember to do them! ')
print("Today's task(s): ")

for i in tasks:
    print(i["name"])
