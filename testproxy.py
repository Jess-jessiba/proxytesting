import time
import subprocess
import pyautogui
import win32gui
import os
import webbrowser
import pyperclip
import getpass
# -*- coding: utf-8 -*-
def login_and_run_command(rdp_file_path, username, password, command,test):
    try:
        pyautogui.hotkey('win', 'r')
        time.sleep(2)
        pyautogui.typewrite('mstsc')
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.typewrite(command)
        pyautogui.press('enter')
        time.sleep(30)
        pyautogui.typewrite(username)
        pyautogui.press('enter')
        time.sleep(5)

        pyautogui.typewrite(password)
        pyautogui.press('enter')


        time.sleep(15)
        pyautogui.press('enter')


        pyautogui.press('enter')
        pyautogui.hotkey('win', 'r')
        time.sleep(1)
        pyautogui.typewrite('powershell')
        pyautogui.press("enter")
        time.sleep(2)


        pyautogui.click
        pyautogui.typewrite("cd C:\\Users/Public/proxyscript")
        pyautogui.press("enter")

        if test == 1:
            pyautogui.typewrite("python proxytesting.py")
            pyautogui.press("enter")
        else:
            pyautogui.typewrite("python proxysplittrail.py")
            pyautogui.press("enter")
        time.sleep(2)

        time.sleep(10)




    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":

    rdp_file_path = "C:/Windows/system32/mstsc.exe"
    username = input("enter your PRID: ")
    server_username = username + "@astrazeneca.net"
    server_password = getpass.getpass('Password: ')
    test = int(input("Enter 1 if its for prod or enter 2 if its for splittrail pac change: "))
    rdpserver_list = ["INCHXS515D770C3.astrazeneca.net"]
    '''"UKCMXS4065EB5D2.astrazeneca.net","UKCMXS4065EB5D2.astrazeneca.net", "UKLIXS512B9B016.astrazeneca.net","USGBXS30E077052.astrazeneca.net"]
    '''
    for server in rdpserver_list:
        command_to_run = server
        login_and_run_command(rdp_file_path, server_username, server_password, command_to_run,test)
