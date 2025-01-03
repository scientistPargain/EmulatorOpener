import os
"""
This script is designed to open and manage Android emulators using the command line.
Modules:
    os: Provides a way of using operating system dependent functionality.
    subprocess: Allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
    time: Provides various time-related functions.
    argparse: Makes it easy to write user-friendly command-line interfaces.
Command-line Arguments:
    --emulator-path: Path to the emulator executable.
    -f: Run in god mode (i.e., super fast).
    -n: Number of the emulator to open(Directly open emulator with its respective number).
Usage:
    Run the script from the command line with optional arguments to specify the emulator path, trigger a specific action, or select an emulator by number.

    example:
     1. python main.py
     2. python main.py --emulator-path "C:/Users/username/AppData/Local/Android/Sdk/emulator/emulator.exe"
     3. python main.py -f
     4. python main.py -n 1  #(Directly open emulator NO.1)

    Note: If you don't provide the emulator path, the script will try to find the emulator executable in the default location.

    All these flags can be combined as well. Happy Coding!
"""
import subprocess
from time import sleep
import argparse

emulator = 'emulator'
user_path = os.path.expanduser("~")

parser = argparse.ArgumentParser(description="Emulator Opener Script")
parser.add_argument('--emulator-path', type=str, help='Path to the emulator executable')
parser.add_argument('-f', action='store_true', help='Flag to trigger a specific action')
parser.add_argument('-n', type=int, help='Number of the emulator you want to open');
args = parser.parse_args()

if args.emulator_path:
    emulator_path = args.emulator_path
else:
    emulator_path = os.path.join(user_path, "AppDataaa", "Local", "Android", "Sdk", "emulator", "emulator.exe")

def get_installed_emulators():
    global emulator
    result = subprocess.run(f"{emulator} -list-avds", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error: It seems you haven't set the path for emulator.")
        sleep(0 if args.f else 2)
        print('Hint: Its good to set emulator path in environment variables;)')
        sleep(0 if args.f else 1)
        print('Trying another alternative...')
        sleep(0 if args.f else 1)
        emulator=emulator_path
        result = subprocess.run(f"{emulator} -list-avds", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            sleep(0 if args.f else 2)
            print("\nAre you sure emulator is installed. Kindly check by running on Android Studio that emulator is installed and working fine or not.")
            print("\n\n If you are sure that emulator is installed, then try adding path to emulator.exe file using '--emulator-path' while runnig the script.")
            exit()
    # print(result)
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
    command = f"{emulator} -avd {emulator_name}"
    subprocess.run(command, shell=True)


def main():
    emulators = get_installed_emulators()
    if not emulators:
        print("No emulators found.")
        print("Please install an emulator using Android Studio and then retry.")
        return
    
    if args.f:
        print("Nice job geek! Running at full speed...")
        sleep(1)

    if args.n is not None:
        if 0 <= args.n < len(emulators):
            print(f"Running emulator number {args.n}: {emulators[args.n-1]}")
            start_emulator(emulators[args.n-1])
        else:
            print(f"Invalid emulator number: {args.n}. Available emulators are:")
            for i, emulator in enumerate(emulators, start=1):
                print(f"{i}: {emulator}")
    else:
        print("Available Emulators:")
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