import inputTask
import delete
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
print('Hello!')

while True:
    if opts == '1':
        AddTask = inputTask.InputTask(tasks)    # NEW OBJECT (class inputTask.InputTask)
        AddTask.Add()
        opts = '0'
    elif opts == '2':
        DeleteTask = delete.removeTask(tasks)   # NEW OBJECT (class delete.removeTask)
        DeleteTask.Delete()
        opts = '0'
    elif opts == '3':
        if not tasks:
            print('(Nothing is here)')
        else:
            for i in tasks:
                print(i["name"])
        opts = '0'
    elif opts == 'end':
        break
    else:
        # menu starts
        print('What do you wanna do today?')
        print('1. Add task(s) \n2. Delete task(s) \n3. View task(s)')   # TODO 第三项先空着，回头加日期排序功能的时候别忘了这儿
        opts = input('\nEnter your choice here (enter the order number. If end, enter "end"): ')
        # menu ends


print('Ok! Remember to do them! ')
print("Today's task(s): ")

for i in tasks:
    print(i["name"])
