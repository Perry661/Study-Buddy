import json
import os


class InputTask:

    def __init__(self, tL):
        self.taskList = tL

    def Add(self):
        if os.path.exists('data.txt'):
            with open('data.txt', 'r', encoding='utf-8') as f:
                id = max(j["ID"] for j in self.taskList) + 1
        else:
            id = 0   # NEW OBJECT (int)

        while True:
            print('This is your task list (for now):')

            if self.taskList == []:
                print('(Nothing is here)')
            else:
                for i in self.taskList:
                    print(i["name"])

            newTask = input('Input your new task (if end, then input "end"): ')    # NEW OBJECT (String)

            if newTask == 'end':
                break

            dueDate = input('Input the due date for the task: ')    # NEW OBJECT (String)

            item = {    # NEW OBJECT (json)
                "ID" : id,
                "name" : 'Task: ' + newTask + ', Due date: ' + dueDate,
                "task": newTask, 
                "dueDate": dueDate
                }
            self.taskList.append(item)

            id += 1

        with open('data.txt', 'w', encoding='utf-8') as f:
            json.dump(self.taskList, f, ensure_ascii=False, indent=2)
