import os
import time
import subprocess
import re
import string
import requests
import winreg
from datetime import datetime
from datetime import date


dict_of_commands = {"Public Proxy pac": "//astrazeneca.net/global/Folders/Utils/autoprox.exe http://www.bbc.com http://pac.zscalertwo.net/astrazeneca.com/AZProxy.pac",
                    "Public AZProxy pac": "//astrazeneca.net/global/Folders/Utils/autoprox.exe http://www.bbc.com http://pac.zscalertwo.net/astrazeneca.com/AZProxy.pac",
                    "Private AZProxy pac": "//astrazeneca.net/global/Folders/Utils/autoprox.exe http://vmanage.astrazeneca.com http://pac.zscalertwo.net/astrazeneca.com/AZProxy.pac",
                    "Private proxy pac ": "//astrazeneca.net/global/Folders/Utils/autoprox.exe http://vmanage.astrazeneca.com http://pac.zscalertwo.net/astrazeneca.com/proxy.pac",
                    }
today = date.today()
today1 = today.strftime("%d-%m-%Y")
name = "resultinch-" + str(today1)
filename = name + ".txt"
f = open(filename, "w")
i = 0
for key,value in dict_of_commands.items():

    result = subprocess.run(value, capture_output=True, text=True, shell=True)
    str1 =""
    str1 =str(result.stdout)
    list1 = []
    list2 =[]
    list1= str1.split("\n")
    list2 = value.split(" ")
    print(list1)
    #print("list2:", list2)
    #print("proxy: ", list1[-4])
    proxy = str(list1[-4]).split(";")
    #print(proxy[0])

    b = list1[-4]
    #print(b)
    if i < 2:
        i = i + 1
        x= re.findall(r"\b185.",b)
        y = re.findall(r"\bzengrevip",proxy[0])
        #print(x)
        #print("y", y)
        if x != [] and y !=[]:
            value = "True"
        else:
            value = "False"
        #print("value", value)
        a = str(key) + " " + str(list2[1]) + " " + str(list1[-4]) + str(value) + "\n"
        with open(filename, "a") as f:
            f.write(a)

    else:
        i = i + 1
        y = re.findall(r"\b194.", b)
        #print(x)
        if y != []:
            value = "True"

        else:
            value = "False"
        #print("value", value)
        a = str(key) + " " + str(list2[1]) + " " + str(list1[-4]) + str(value) + "\n"
        with open(filename, "a") as f:
            f.write(a)




list3 = ['set-itemproperty -path "hkcu:Software\Microsoft\Windows\CurrentVersion\Internet Settings" -name AutoConfigURL -value "http://pac.zscalertwo.net/astrazeneca.com/AZProxy.pac" -type string',
         'set-itemproperty -path "hkcu:Software\Microsoft\Windows\CurrentVersion\Internet Settings" -name AutoConfigURL -value "http://pac.zscalertwo.net/astrazeneca.com/proxy.pac" -type string']
for powershell_command in list3: 
# Run the PowerShell command using subprocess
    try:
        result = subprocess.run(["powershell", "-Command", powershell_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Check the return code to see if the command was successful
        if result.returncode == 0:
            if list3.index(powershell_command)==0:
                with open(filename, "a") as f:
                    file = "\n" + "Following output are for AZProxy pac" + "\n"
                    f.write(file)
            else:
                with open(filename, "a") as f:
                    file = "Following output are for proxy pac" + "\n"
                    f.write(file)
                
            print("PowerShell command executed successfully")
            
        else:
            print("PowerShell command failed")
            #print("Error message:")
            
    except Exception as e:
        print("An error occurred:", str(e))


    url_list = ["https://www.bbc.com", "http://nucleus.astrazeneca.com"]
    for url_list_curl in url_list:
        
        urlcommand = f"curl {url_list_curl}"
        result = subprocess.run(["powershell", "-Command", urlcommand], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        a = result.stdout
        print(a[0:25])
        with open(filename, "a") as f:
            file = f"Status code of curl output of {url_list_curl}" + "\n" + a[0:25] + "\n"
            f.write(file)
            
    payload = {}
    headers = {}
    for j in url_list:
        try:
            print(j)
            response = requests.request("GET", j, headers=headers, data=payload)
            print(response.status_code)
            if response.status_code == 200:
                file = f"URL {j} opened successfully with status code {response.status_code}" + "\n"
                print(file)
                with open(filename, "a") as f:
                    #f.write("output for " + i + "\n")
                    f.write(file)
            else:
                file = f"URL {j} returned status code {response.status_code}" + "\n"
                print(file)
                with open(filename, "a") as f:
                    #f.write("output for " + i + "\n")
                    f.write(file)
        except requests.ConnectionError:
            file = f"Failed to connect to URL {j}" + "\n"
            with open(filename, "a") as f:
                #f.write("output for " + i + "\n")
                f.write(file)
        finally:
                f.close()
                
full_path = os.path.abspath(filename)
print(full_path)
destination_path='\\\\SESKWPRGVPN01.emea.astrazeneca.net\D\Sankar\Proxytesting'
powershell_save_command = f"Copy-Item -Path '{full_path}' -Destination '{destination_path}'"
print(powershell_save_command)

# Run the PowerShell command using subprocess
try:
    result = subprocess.run(["powershell", "-Command", powershell_save_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("success")
except:
    print("Not sucess")


