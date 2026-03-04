from dueDateFILE import DueDate


class Add:

    def __init__(self, tL, trash):
        self.task = tL
        self.trash = trash

    def addTask(self):
        if self.task and self.trash:
            id_task = max(j["ID"] for j in self.task) + 1
            id_trash = max(j["ID"] for j in self.trash) + 1
            id = max(id_task, id_trash)
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
                "name": f"Task: {newTask}, Due date: {dueDate}",
                "task": newTask, 
                "dueDate": dueDate,
                "dueYear": dueYear,
                "dueMonth": dueMonth,
                "dueDay": dueDay,
                "overDue": "",
                "finish": "",
                "delete": "",
                "deleteDate": ""
                }
            self.task.append(item)

            id += 1
