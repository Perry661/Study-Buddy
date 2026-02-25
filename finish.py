class Finish:
    def __init__(self, t):
        self.task = t


    def finishCheck(self):
        if not self.task:
            print('(Nothing is here)')
            return None
        else:
            for i in self.task:
                print(f'{i["name"]}\tID: {i["ID"]}')

        while True:
            finishID = input('Enter the task ID you finished (if end, then enter nothing): ')   # NEW OBJECT (String)
            if finishID == '':
                return None
            try:
                finishIDInt = int(finishID)    # NEW OBJECT (int)
            except ValueError:
                print('Please enter a number.')
                continue

            if any(j.get("ID") == finishIDInt for j in self.task):
                return finishIDInt

            print('Task ID out of range, please re-enter.')


    def finishTask(self, id, taskFinish):
        for i in self.task:
            if i.get('ID') == id:
                i['finish'] = '[FINISHED]'
                i['name'] = f"{i['finish']} {i['name']}"
                taskFinish.append(i)
                # save the finish task into taskFINISH
                self.task.remove(i)
                # remove the finish task from tasks
