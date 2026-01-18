import inputTask
import delete
import json
import os


if os.path.exists('data.txt'):
    with open('data.txt', 'r', encoding='utf-8') as f:
        tasks = json.load(f)
else:
    tasks = []


print('Hello!')
optInput = input('Wanna input new task? (Y/N)')   # NEW OBJECT (String)

while optInput != 'y' and optInput != 'Y' and optInput != 'n' and optInput != 'N':
    optInput = input('Please re-enter your option (only Y, N, y, or n): ')

if optInput == 'y' or optInput == 'Y':
    AddTask = inputTask.InputTask(tasks)
    AddTask.Add()
# Above: to input the task


optDelete = input('Okay, any task(s) wanna delete? (Y/N)')

while optDelete != 'y' and optDelete != 'Y' and optDelete != 'n' and optDelete != 'N':
    optDelete = input('Please re-enter your option (only Y, N, y, or n): ') # NEW OBJECT (String)

if optDelete == 'y' or optDelete == 'Y':
    DeleteTask = delete.removeTask(tasks)
    DeleteTask.Delete()
# Above: to delete the task

print('Ok! Remember to do them! ')
print("Today's task(s): ")

for i in tasks:
    print(i["name"])
