from datetime import date


class Delete:

    def __init__(self, tL, trash):
        self.task = tL
        self.trash = trash

    def deleteTask(self):
        while True:
            print('\nBy the way, this is your task list:')
            if not self.task:
                print('(Nothing is here)')
                break
            for i in self.task:
                print(f'{i["name"]}\t"ID:", {i["ID"]}')

            deleteInput = input('\nEnter the task ID you wanna delete (if end, then enter nothing): ')    # NEW OBJECT (String)

            if deleteInput == '':
                break
            try:
                deleteID = int(deleteInput) # NEW OBJECT(int)
            except ValueError:
                print('\nPlease enter a valid task ID or nothing if end.')
                continue

            for j in self.task:
                # check if the id is in the list
                if j.get("ID") == deleteID:
                    j['delete'] = 30
                    j['deleteDate'] = date.today().isoformat()
                    self.trash.append(j)
                    self.task.remove(j)
                    break
                else:
                    # if not, then print a message, adn continue looping.
                    print('Task ID out of range, please re-enter.')


    def deleteChecking(self):
        today = date.today()    # NEW OBJECT (date)
        changed = False # NEW OBJECT (Boolean)
        keptTrash = []  # NEW OBJECT (list)

        for i in self.trash:
            remainDays = i.get('delete', 0)   # NEW OBJECT (any)
            # get "delete" value in the list. If no, then use 0.
            try:
                remainingInt = int(remainDays)
            except (TypeError, ValueError):
                remainingInt = 0    # NEW OBJECT (int)

            deleteDate = i.get('deleteDate')   # NEW OBJECT (date)
            if isinstance(deleteDate, str) and deleteDate:
            # check if deleteDate is str type
                try:
                    last_date = date.fromisoformat(deleteDate)    # NEW OBJECT (date)
                    # change deleteDate to date form
                except ValueError:
                    last_date = today
            elif isinstance(deleteDate, date):
                last_date = deleteDate
            else:
                last_date = today

            days_passed = (today - last_date).days  # NEW OBJECT (int)
            if days_passed > 0:
                remainingInt -= days_passed
                changed = True

            if remainingInt > 0:
                if i.get('delete') != remainingInt:
                    i['delete'] = remainingInt
                    changed = True
                todayStr = today.isoformat()   # NEW OBJECT (str)
                # change today to str type
                if i.get('deleteDate') != todayStr:
                    i['deleteDate'] = todayStr
                    changed = True
                keptTrash.append(i)
            else:
                changed = True

        if len(keptTrash) != len(self.trash):
            self.trash[:] = keptTrash
        
        return changed
    
    def putBack(self):
        while True:
            print('\nBy the way, this is your task list:')
            if not self.trash:
                print('(Nothing is here)')
                break
            for i in self.trash:
                print(f'{i["name"]}\t"ID:", {i["ID"]}')

            putBackID = input('\nEnter the task ID you wanna put back (if end, then enter nothing): ')    # NEW OBJECT (String)

            if putBackID == '':
                break
            try:
                IDint = int(putBackID) # NEW OBJECT(int)
            except ValueError:
                print('\nPlease enter a valid task ID or nothing if end.')
                continue

            for t in self.trash:
                if t['ID'] == IDint:
                    self.task.append(t)
                    self.trash.remove(t)
                    break
                else:
                    # if not, then print a message, adn continue looping.
                    print('Task ID out of range, please re-enter.')
