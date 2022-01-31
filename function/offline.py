import os
import subprocess as sp
import datetime

paths = {
    'notepad': "C:\\Windows\\notepad.exe",
    'calculator': "C:\\Windows\\System32\\calc.exe"
}

def report_time():
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    return current_time
    
def open_notepad():
    os.startfile(paths['notepad'])

def open_tidur(): 
    os.system("shutdown /h")

def open_cmd():
    os.system('start cmd')


def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)


def open_calculator():
    sp.Popen(paths['calculator'])