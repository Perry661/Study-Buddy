class removeTask:

    def __init__(self, tL):
        self.taskList = tL

    def Delete(self):
        while True:
            print('By the way, this is your task list:')
            for i in self.taskList:
                print(i["name"], "ID:", i["ID"])

            deleteID = int(input('Input the task ID you wanna delete (if end, then input "end"): '))    # NEW OBJECT (String)

            if deleteID == 'end':
                break

            for j in self.taskList:
                if j["ID"] == deleteID:
                    self.taskList.remove(j)
                    break

            print(self.taskList)
