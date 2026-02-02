import json


class removeTask:

    def __init__(self, tL):
        self.taskList = tL

    def Delete(self):
        while True:
            print('\nBy the way, this is your task list:')
            if not self.taskList:
                print('(Nothing is here)')
                break
            for i in self.taskList:
                print(i["name"], "ID:", i["ID"])

            deleteInput = input('\nEnter the task ID you wanna delete (if end, then enter nothing): ')    # NEW OBJECT (String)

            if deleteInput == '':
                break
            try:
                deleteID = int(deleteInput)
            except ValueError:
                print('\nPlease enter a valid task ID or nothing if end.')
                continue

            for j in self.taskList:
                if j["ID"] == deleteID:
                    self.taskList.remove(j)
                    break

            with open('data.txt', 'w', encoding='utf-8') as f:
                json.dump(self.taskList, f, ensure_ascii=False, indent=2)
