class InputTask:

    def __init__(self, tL):
        self.taskList = tL

    def Add(self):
        while True:
            print('By the way, this is your task list:', self.taskList)
            newTask = input('Input your new task (if end, then input "end"): ')    # NEW OBJECT (String)

            if newTask == 'end':
                break

            dueDate = input('Input the due date for the task: ')    # NEW OBJECT (String)
            self.taskList.append(newTask + '_' + dueDate)
