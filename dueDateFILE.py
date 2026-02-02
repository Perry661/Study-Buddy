from datetime import date

class DueDate:
    
    def __init__(self):
        pass

    def yyyy(self):
        while True:
            print('\nEnter the due year if needed (if no, then enter nothing)')
            dueYear = input('(By the way, if no due year provides, then will be defaulted as this year): ') # NEW OBJECT (String)
            if dueYear == '':
                today = date.today()    # NEW OBJECT (int)
                dueYear = str(today.year)    # NEW OBJECT (String)
                break
            try:
                break
            except ValueError:
                print('\nError, enter the due year as a number or enter nothing.')
        return dueYear
    
    def mm(self):
        while True:
            dueMonth = input("Enter the due month (1-12): ")    # NEW OBJECT (String)
            try:
                if 1 <= int(dueMonth) <= 12:
                    break
                else:
                    print("\nMonth must be between 1 and 12.")
            except ValueError:
                print("\nPlease enter a number.")
        return dueMonth

    def dd(self):
        while True:
            dueDay = input('Enter the due day (1-31): ')    # NEW OBJECT (String)
            try:
                if 1 <= int(dueDay) <= 31:
                    break
                else:
                    print("\nDay must be between 1 and 31.")
            except ValueError:
                print("\nPlease enter a number.")
        return dueDay
    
    def overDue(self, y, m, d):
        ddl = date(y, m, d)
        today = date.today()

        if ddl > today:
            daysLeft = (ddl - today).days
            return f'There is {daysLeft} day(s) left.'
        elif ddl == today:
            return "It's due today!! (HURRY UP!!!)"
        else:
            return "[OVERDUE] It's already due… (Mourn…)"
