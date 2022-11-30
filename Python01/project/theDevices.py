"""
DEVICE MANAGEMENT SYSTEM (AML-1214 Project - Fall 2022)
Submitted by:
- Auradee Castro
- Olivia Deguit
- Bhumika Rajendra Babu
"""
import pickle
import re
from enum import Enum
from colorama import Fore as fg, Back as bg, Style as ef, init

init(autoreset=True)

DEVICE_FILENAME = "devices.txt"

class Command(Enum):
    View = "1"
    Add = "2"
    Delete = "3"
    Update = "4"
    Search = "5"
    Exit = "6"

def main():
    """
    The function that starts the applications
    """
    is_login_account = loginAccount()

    if is_login_account:
        startDeviceManagement()
    else:
        print(f"{bg.RED} Exiting application... ")

def loginAccount():
    """
    The function that prompts authorized users to log into the application
    """
    print(f"{fg.CYAN}+++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f"{fg.CYAN}+             Login to Your Account             +")
    print(f"{fg.CYAN}+++++++++++++++++++++++++++++++++++++++++++++++++")

    login_attempt = 0
    is_login_account = False
    account_filename = "accounts"

    account_list = readFile(account_filename)

    # If there are no errors reading the account file
    if account_list is not None:

        while login_attempt != 3:
            username = input("Enter username: ")
            password = input("Enter password: ")

            for account in account_list:
                if username == account[0] and password == account[1]:
                    is_login_account = True
                    break
            else:
# Replaced by code below                print(f"{fg.RED}{ef.BRIGHT}Invalid username and/or password\n")
# Added
                if login_attempt <= 1:
                    invalid_login = int(2 - login_attempt)
                    print(f"{fg.RED}{ef.BRIGHT}Invalid username and/or password. You have {invalid_login} login attempt left.\n")
                else:
                    print(f"{fg.RED}{ef.BRIGHT}Invalid username and/or password\n")
# End of additional command

            if is_login_account:
                print(f"{fg.GREEN}{ef.BRIGHT}Log In Successful\n")
                break

            login_attempt += 1
        else:
            print(f"{fg.RED}{ef.BRIGHT}You have exceeded three login attempts")

    return is_login_account

def startDeviceManagement():
    """
    The function that displays the application menu
    """
    print(f"{fg.CYAN}+++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f"{fg.CYAN}+    Welcome to the Device Management System    +")
    print(f"{fg.CYAN}+++++++++++++++++++++++++++++++++++++++++++++++++")

    command = None
    while command != Command.Exit.value:
        print()
        print("1. View all devices")
        print("2. Add a device")
        print("3. Delete a device")
        print("4. Update a device")
        print("5. Search for a device")
        print("6. Exit the program")

        command = input(f"\n{ef.BRIGHT}Select one option from the list (1, 2, 3, 4, 5 or 6): ").strip()

        if command not in [item.value for item in Command]:
            print("Invalid selection. Try again.")
        elif command == Command.Exit.value:
            print(f"\n{bg.GREEN}{ef.BRIGHT} Thank you for using the application! ")
        else:
            device_list = readFile(DEVICE_FILENAME)

            # If there is an error reading the device file
            if device_list is None:
                print(f"{bg.RED} Exiting application...") #print(f"{bg.RED}{ef.BOLD} Exiting application...")
                break

            if command == Command.View.value:
                viewDeviceList(device_list)

            elif command == Command.Add.value:
                print(f"{bg.YELLOW}{ef.BRIGHT} Note: Device code should consist of 7 numbers and 2 characters ")
                device_details = input(f"{ef.BRIGHT}Add device, format [device code] [device name]: ").split(" ", 1)

                # delete from the list all empty string elements after removing leading and trailing whitespaces
                device_details = list(filter(None, [device.strip() for device in device_details]))

                if len(device_details) == 0:
                    print(f"{fg.RED}Device code and device name cannot be empty")
                elif len(device_details) == 1:
                    print(f"{fg.RED}Missing device name. Format [device code] [device name]")
                elif not isValidDeviceCode(device_details[0]):
                    print(f"{fg.RED}Invalid device code pattern")
                else:
                    addDevice(device_details, device_list)

            elif command == Command.Delete.value:
                device_code = input("Enter code to delete device: ").strip()

                if len(device_code) == 0:
                    print(f"{fg.RED}Device code cannot be empty")
                else:
                    deleteDevice(device_code, device_list)

            elif command == Command.Update.value:
                device_code = input("Enter code to update device: ").strip()

                if len(device_code) == 0:
                    print(f"{fg.RED}Device code cannot be empty")
                else:
                    updateDevice(device_code, device_list)

            elif command == Command.Search.value:
                keyword = input("Enter keyword to search for device: ")
                searchDevice(keyword, device_list)

            is_continue = ""
            while is_continue != "n" and is_continue != "y":
                is_continue = input(f"\n{ef.BRIGHT}Do you want to continue? [y/n]: ").strip().lower()
                if is_continue != "n" and is_continue != "y":
                    print(f"{fg.RED}Invalid input. Type 'y' for yes or 'n' for no.")
            else:
                if is_continue == "n":
                    print(f"\n{bg.GREEN}{ef.BRIGHT} Thank you for using the application! ")
                    break

def viewDeviceList(device_list):
    """
    The function that displays device records
    """
    if len(device_list) > 0:
        print("List of all devices:")
        for device in device_list:
            print(f"- {device[0]} {device[1]}")
    else:
        print(f"{fg.RED}No device found")

def addDevice(device_details, device_list):
    """
    The function that adds a device record
    """
    is_continue = ""
    if isDuplicateDevice(device_details[0], device_details[1], device_list):
        while is_continue != "n" and is_continue != "y":
            is_continue = input(f"{fg.RED}Record already exists. Do you want to continue? [y/n]: ").strip().lower()
            if is_continue != "n" and is_continue != "y":
                print(f"{fg.RED}Invalid input. Type 'y' for yes or 'n' for no.")
    else:
        is_continue = "y"

    if is_continue == "y":
        device_list.append(device_details)
        is_device_added = writeFile(device_list, DEVICE_FILENAME)
        if is_device_added:
            print(f"{fg.GREEN}{device_details[0]} {device_details[1]} is added")
    else:
        print(f"{device_details[0]} {device_details[1]} is not added")

def deleteDevice(device_code, device_list):
    """
    The function that deletes device name(s) of the specified device code
    """
    device_name_list = getDeviceName(device_code, device_list)

    if len(device_name_list) == 0:
        print(f"{fg.RED}Device code {device_code} is not found")
    else:
        if len(device_name_list) == 1:
            device_num_list = "1"  # only 1 record found
        else:
            device_num_list = input("Enter number to delete device name (comma separated): ").split(",")
            # delete from the list all empty string elements after removing leading and trailing whitespaces
            device_num_list = list(filter(None, [device_num.strip() for device_num in device_num_list]))

        del_ctr = 0
        for device_num in device_num_list:
            device_num_ctr = 0

            for idx, device_name in enumerate(device_name_list):
                if device_num == str(device_name[0]):
                    orig_device_idx = device_name_list[idx][1] - del_ctr
                    deleted_device = device_list.pop(orig_device_idx)

                    device_num_ctr += 1
                    del_ctr += 1

                    is_device_deleted = writeFile(device_list, DEVICE_FILENAME)
                    if is_device_deleted:
                        print(f"{fg.GREEN}{deleted_device[0]} {deleted_device[1]} is deleted")
                    break

            if device_num_ctr == 0:
                print(f"{fg.RED}Invalid device name number {device_num}. Skipped..")

def updateDevice(device_code, device_list):
    """
    The function that updates device name(s) of the specified device code
    """
    device_name_list = getDeviceName(device_code, device_list)

    if len(device_name_list) == 0:
        print(f"{fg.RED}Device code {device_code} is not found")
    else:
        if len(device_name_list) == 1:
            device_num_list = "1"  # only 1 record found
        else:
            device_num_list = input("Enter number to update device name (comma separated): ").split(",")
            # delete from the list all empty string elements after removing leading and trailing whitespaces
            device_num_list = list(filter(None, [device_num.strip() for device_num in device_num_list]))

        for device_num in device_num_list:
            device_num_ctr = 0

            for idx, device_name in enumerate(device_name_list):
                if device_num == str(device_name[0]):
                    print(f"Old device name: {device_name_list[idx][2]}")
                    new_device_name = input("New device name: ")

                    orig_device_idx = device_name_list[idx][1]
                    device_list[orig_device_idx][1] = new_device_name
                    device_num_ctr += 1

                    is_device_updated = writeFile(device_list, DEVICE_FILENAME)
                    if is_device_updated:
                        print(f"{fg.GREEN}Device name is updated")
                    break

            if device_num_ctr == 0:
                print(f"{fg.RED}Invalid device name number {device_num}. Skipped..")

def searchDevice(keyword, device_list):
    """
    The function that searches for all devices that matches with the keyword
    """
    keyword_ctr = 0
    for idx, device in enumerate(device_list):
        if keyword.lower() in "".join(device).lower():
            print(f"- {device_list[idx][0]} {device_list[idx][1]}")
            keyword_ctr += 1

    if keyword_ctr == 0:
        print(f"{fg.RED}Keyword {keyword} is not found")

def getDeviceName(device_code, device_list):
    """
    The function that gets all device names using the specified device code
    """
    new_device_name_list = []
    device_ctr = 1
    # get all device names using the specified device code
    device_name_list = [[idx, device_list[idx][1]] for idx, device in enumerate(device_list)
                        if device_list[idx][0] == device_code]

    if len(device_name_list) > 1:
        print(f"Device names using code {device_code}")

    for idx, device_name in enumerate(device_name_list):
        if len(device_name_list) > 1:
            print(str(device_ctr) + ".", device_name[1])
        # list contains: [0] temp ID of device name [1] index from original list [2] device name
        new_device_name_list.append([device_ctr, device_name[0], device_name[1]])
        device_ctr += 1

    return new_device_name_list

def isValidDeviceCode(device_code):
    """
    The function that checks if a device code matches with the pattern
    """
    device_code_pattern = re.compile(r"[0-9]{7}[a-zA-Z]{2}")
    result = device_code_pattern.fullmatch(device_code)
    return True if result is not None else False

def isDuplicateDevice(device_code, device_name, device_list):
    """
    The function that checks if a device record already exists
    """
    has_duplicate = False
    for device in device_list:
        if device_code == device[0] and device_name == device[1]:
            has_duplicate = True
            break
    return has_duplicate

def readFile(filename):
    """
    The function that reads content from a file
    """
    try:
        with open(filename, "rb") as file:
            content_list = pickle.load(file)
    except EOFError:
        content_list = []
    except Exception as err:
        print(f"{fg.RED}Unexpected error: {err}")
        content_list = None

    return content_list

def writeFile(content_list, filename):
    """
    The function that writes content to a file
    """
    try:
        with open(filename, "wb") as file:
            pickle.dump(content_list, file)
    except Exception as err:
        print(f"{fg.RED}Unexpected error: {err}")
        return False

    return True

main()
