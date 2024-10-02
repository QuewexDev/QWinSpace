import os
import platform
import subprocess
try:
    import psutil
except:
    os.system("python -m pip install -r requirements.txt")
import json
import time

userdir = os.getenv("userprofile")
data = {"spaces": []}

def log(type="INFO", message=any):
    print(f"[{type}] {message}")
    
def add_space(name=str):
    data["spaces"].append(name)
    os.mkdir(userdir + f"\\Spaces\\{name}")

if platform.system() != "Windows":
    print("Sorry! But your system is not supported.")
    time.sleep(5)
    exit(1)

banner = """
   ______          ___                                 
  / __ \ \        / (_)                                
 | |  | \ \  /\  / / _ _ __  ___ _ __   __ _  ___ ___  
 | |  | |\ \/  \/ / | | '_ \/ __| '_ \ / _` |/ __/ _ \ 
 | |__| | \  /\  /  | | | | \__ \ |_) | (_| | (_|  __/ 
  \___\_\  \/  \/   |_|_| |_|___/ .__/ \__,_|\___\___| 
                                | |                    
                                |_|                    
"""

print(banner)
print("Welcome! Loading configuration file...")

os.chdir(userdir)

if not os.path.isdir("Spaces"):
    log(message="Spaces not found! Starting creation...")
    
    os.mkdir("Spaces")
    
    log(message="Starting creation of main space...")
    
    for i in range(4):
        [process.kill() for process in psutil.process_iter() if process.name() == "explorer.exe"]
        
    log(message="Moving main space...")
    
    os.replace(userdir + "\\Desktop", userdir + "\\Spaces\\main")
    
    os.system(f"mklink /J {userdir}\\Desktop {userdir}\\Spaces\\main")
    
    data["spaces"].append("main")
    
    log(message="Done!")
    
    psutil.Popen("C:\\Windows\\explorer.exe")

os.chdir("Spaces")

if not os.path.exists("data.json"):
    log(message="Creating data...")
    
    with open(userdir+"\\Spaces\\data.json", "w+") as file:
        json.dump(data, file)
    
    log(message="Done!")
else:
    log(message="Loading data...")
    with open(userdir+"\\Spaces\\data.json", "r") as file:
        data = json.load(file)
    log(message="Done!")

while True:
    time.sleep(5)
    os.system("cls")
    print(banner+"\n"*2)
    print("1) Switch space    2) Create space\n3) Remove space    4) Exit")
    choice = int(input("> "))
    
    match choice:
        case 1:
            for i in range(len(data["spaces"])):
                print(data['spaces'][i])
            name = str(input("Select space: "))
            
            if name not in data["spaces"]:
                print("Space not found!")
                continue
            
            log(message="Switching space...")
            
            for i in range(4):
                try:
                    [process.kill() for process in psutil.process_iter() if process.name() == "explorer.exe"]
                except:
                    pass
                
            os.remove(userdir+"\\Desktop")
            os.system(f"mklink /J {userdir}\\Desktop {userdir}\\Spaces\\{name}")
            
            time.sleep(5)
            psutil.Popen("C:\\Windows\\explorer.exe")
            
            log(message="Switched!")
        
        case 2:
            name = str(input("Enter new name of space: "))
            
            if name in data["spaces"]:
                print("Space already exists!")
                continue
            
            log(message="Creating new space...")
            
            os.mkdir(userdir+"\\Spaces\\"+name)
            
            data["spaces"].append(name)
            
            with open(userdir+"\\Spaces\\data.json", "w+") as file:
                json.dump(data, file)
            
            log(message="Done!")
        
        case 3:
            name = str(input("Enter name of space to delete: "))
            
            if name not in data["spaces"]:
                print("Space not found!")
                continue
            elif name == "main":
                print("Can't delete main space!")   
                continue
            
            log(message="Deleting space...")
            
            for i in range(4):
                [process.kill() for process in psutil.process_iter() if process.name() == "explorer.exe"]
                
            os.remove(userdir+"\\Desktop")
            os.system(f"mklink /J {userdir}\\Desktop {userdir}\\Spaces\\main")
            os.rmdir(userdir+"\\Spaces\\"+name)
            
            psutil.Popen("C:\\Windows\\explorer.exe")
            
            data["spaces"].remove(name)
            
            with open(userdir+"\\Spaces\\data.json", "w+") as file:
                json.dump(data, file)
            
            log(message="Done!")
        
        case 4:
            log(message="Exiting...")
            time.sleep(3)
            exit()
