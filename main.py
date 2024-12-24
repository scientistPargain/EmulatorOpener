import os
import subprocess
from time import sleep

emulator = 'emulator'
user_path = os.path.expanduser("~")
emulator_path = os.path.join(user_path, "AppDataaa", "Local", "Android", "Sdk", "emulator", "emulator.exe")

def get_installed_emulators():
    global emulator
    print('emulator_path is: ', emulator)
    result = subprocess.run("emulatorrr -list-avds", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error: It seems you haven't set the path for emulator.")
        sleep(2)
        print('Hint: Its good to set emulator path in environment variables;)')
        sleep(1)
        print('Trying another alternative...')
        sleep(1)
        emulator=emulator_path
        result = subprocess.run(f"{emulator} -list-avds", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            sleep(2)
            print("Are you sure emulator is installed. Kindly check by running on Android Studio that emulator is installed and working fine or not.")
            exit()
    print(result)
    emulators = result.stdout.splitlines()
    return emulators

def update_emulator_config(emulator_name):

    #"C:/Users/deepa/.android/avd/{emulator_name}.avd/emulator-user.ini"
    config_path = os.path.join(user_path, ".android", "avd", f"{emulator_name}.avd", "emulator-user.ini")
    print('config_path is: ', config_path)
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            lines = file.readlines()
            print(lines)
        
        with open(config_path, 'w') as file:
            for line in lines:
                if line.startswith("window.x"):
                    file.write("window.x = 0\n")
                elif line.startswith("window.y"):
                    file.write("window.y = 0\n")
                else:
                    file.write(line)
    else:
        print(f"Configuration file for {emulator_name} not found.")

def start_emulator(emulator_name):
    print('emulator is: ', emulator)
    command = f"emulatorrr -avd {emulator_name}"
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        subprocess.run(f"{emulator} -avd {emulator_name}", shell=True)


def main():
    emulators = get_installed_emulators()
    # print('emulators is: ', emulators)
    if not emulators:
        print("No emulators found.")
        print("Please install an emulator using Android Studio and then retry.")
        return
    
    print("Installed Emulators:")
    for idx, emulatorr in enumerate(emulators, start=1):
        print(f"{idx}. {emulatorr}")
    
    choice = int(input("Enter the number of the emulator you want to open: "))
    if 1 <= choice <= len(emulators):
        selected_emulator = emulators[choice - 1]
        update_emulator_config(selected_emulator)
        start_emulator(selected_emulator)
    else:
        print("Invalid choice.\nExiting...")

if __name__ == "__main__":
    main()