class removeTask:

    def __init__(self, tL):
        self.taskList = tL

    def Delete(self):
        while True:
            print('By the way, this is your task list:', self.taskList)
            deleteTask = input('Input the task you wanna delete (if end, then input "end"): ')    # NEW OBJECT (String)

            if deleteTask == 'end':
                break

            self.taskList.remove(deleteTask)

            print(self.taskList)
