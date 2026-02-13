from inputTask import InputTask
from delete import removeTask
from dueDateFILE import DueDate
import json
import os

class editTask:

    def __init__(self, t):
        self.task = t

    def editCheck(self):
        for i in self.task:
            print(i["name"] + f'\tID: {i["ID"]}')

        if not self.task:
            print('(Nothing is here)')
            return '',''
        
        while True:
            editID = input('Enter the task ID you want to edit (if end, then enter nothing): ')   # NEW OBJECT (String)
            if editID == '':
                # check if there's nothing enter
                return '', ''
            try:
                editIDInt = int(editID)    # NEW OBJECT (int)
                # check if enter a number
            except ValueError:
                # if not, then print a message, and continue looping.
                print('Please enter a number.')
                continue
            # 检查id是否处于列表中
            for j in self.task:
                if j.get("ID") == editIDInt:
                    # check if the id is in the list
                    break   # break the for looop
                else:
                    # if not, then print a message, adn continue looping.
                    print('Task ID out of range, please re-enter.')
                    continue
            break   # break the while loop

        while True:
            for t in self.task:
                if t['ID'] == editIDInt:
                    print(t['name'])

            editObj = input('Enter the object you want to edit: ')   # NEW OBJECT (String)
            # TODO 检查obj是否处于任务中
            if editObj.lower() == 'task' or editObj.lower() == 'due date':
                return editIDInt, editObj.lower()
            else:
                print('Object not exist or wrong spelling. \n')

    def editName(self, id):
        newName = input('\nEnter your new name for the task: ') # NEW OBJECT (String)

        # Add the new name of the task with a same ID and due date.
        for t in self.task:
            if t.get("ID") == id:
                t["task"] = newName
                t["name"] = f'Task: {newName}, Due date: {t["dueDate"]}'
                break
        
        with open('data.txt', 'w', encoding='utf-8') as f:
            json.dump(self.task, f, ensure_ascii=False, indent=2)
    
    def editDueDate(self, id):
        d = DueDate()   # NEW OBJECT (class dueDateFILE.DueDate)
        newDY = d.yyyy()  # NEW OBJECT (String)
        newDM = d.mm()   # NEW OBJECT (String)
        newDD = d.dd() # NEW OBJECT (String)

        year = int(newDY) if newDY != '' else None
        month = int(newDM)
        day = int(newDD)

        newDueDate = f'{year:04d}-{month:02d}-{day:02d}'   # NEW OBJECT (String)

        # Add the new due date of the task with a same ID and name.
        for t in self.task:
            if t.get("ID") == self.task:
                t["dueYear"] = newDY
                t["dueMonth"] = newDM
                t["dueDay"] = newDD
                t["dueDate"] = newDueDate
                t["name"] = f'Task: {t["task"]}, Due date: {newDueDate}'
                break
        
        with open('data.txt', 'w', encoding='utf-8') as f:
            json.dump(self.task, f, ensure_ascii=False, indent=2)
