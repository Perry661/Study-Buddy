from save import data_path, save_tasks
from dueDateFILE import DueDate


class Add:

    def __init__(self, tL):
        self.task = tL

    def addTask(self):
        if self.task:
            id = max(j["ID"] for j in self.task) + 1
        else:
            id = 0   # NEW OBJECT (int)

        while True:
            # ADD NEW TASK(S)
            print('\nThis is your task list (for now):')

            if self.task == []:
                print('(Nothing is here)')
            else:
                for i in self.task:
                    print(i["name"])

            newTask = input('\nEnter your new task (if end, then enter nothing): ')    # NEW OBJECT (String)

            if newTask == '':
                break
            # Above is to add new task(s).

            # ADD DUE DATE
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
            self.task.append(item)

            id += 1

        save_tasks(data_path, self.task)
