import json
import os
from dueDateFILE import DueDate


class InputTask:

    def __init__(self, tL):
        self.taskList = tL

    def Add(self):
        if self.taskList:
            id = max(j["ID"] for j in self.taskList) + 1
        else:
            id = 0   # NEW OBJECT (int)

        while True:
            print('\nThis is your task list (for now):')

            if self.taskList == []:
                print('(Nothing is here)')
            else:
                for i in self.taskList:
                    print(i["name"])

            newTask = input('\nEnter your new task (if end, then enter nothing): ')    # NEW OBJECT (String)

            if newTask == '':
                break
            # Above is to add new task(s).

            d = DueDate()   # NEW OBJECT (class dueDateFILE.DueDate)
            dueYear = d.yyyy()  # NEW OBJECT (String)
            dueMonth = d.mm()   # NEW OBJECT (String)
            dueDay = d.dd() # NEW OBJECT (String)

            year = int(dueYear) if dueYear != '' else None
            month = int(dueMonth)
            day = int(dueDay)

            dueDate = f'{year:04d}-{month:02d}-{day:02d}'   # NEW OBJECT (String)
            # Above is to add due date.

            item = {    # NEW OBJECT (json)
                "ID": id,
                "name": 'Task: ' + newTask + ', Due date: ' + dueDate,
                "task": newTask, 
                "dueDate": dueDate,
                "dueYear": dueYear,
                "dueMonth": dueMonth,
                "dueDay": dueDay,
                "overDue": ''
                }
            self.taskList.append(item)

            id += 1

        with open('data.txt', 'w', encoding='utf-8') as f:
            json.dump(self.taskList, f, ensure_ascii=False, indent=2)
