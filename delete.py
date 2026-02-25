from save import data_path, save_tasks


class Delete:

    def __init__(self, tL):
        self.task = tL

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
                if j.get("ID") == deleteID:
                    # check if the id is in the list
                    self.task.remove(j)
                    break
                else:
                    # if not, then print a message, adn continue looping.
                    print('Task ID out of range, please re-enter.')
                    continue

            save_tasks(data_path, self.task)
