"""
AML-1214 Project - Fall 2022
Submitted by:
- Auradee Castro
- Bhumika Rajendra Babu
- Olivia Deguit
"""
import pickle
from enum import Enum

devices_filename = "devices.txt"
accounts_filename = "accounts"


class Command(Enum):
    View = "1"
    Add = "2"
    Delete = "3"
    Update = "4"
    Search = "5"
    Exit = "6"


def main():
    is_login_account = loginAccount()

    if is_login_account:
        startDeviceManagement()
    else:
        print("Exiting application...")


def loginAccount():
    print("+++++++++++++++++++++++++++++++++++++++++++++++++")
    print("+             Login to Your Account             +")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++")

    account_list = readFile(accounts_filename)

    login_ctr = 0
    is_login_account = False
    while login_ctr != 3:
        username = input("Enter username: ")
        password = input("Enter password: ")

        for account in account_list:
            if username in account and password in account:
                is_login_account = True
                break
        else:
            print("Invalid username and/or password\n")

        if is_login_account:
            print("Log In Successful\n")
            break

        login_ctr += 1
    else:
        print("You have exceeded three attempts to login")

    return is_login_account


def startDeviceManagement():

    print("+++++++++++++++++++++++++++++++++++++++++++++++++")
    print("+    Welcome to the Device Management System    +")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++")
    print("1. View all device")
    print("2. Add a device")
    print("3. Delete a device")
    print("4. Update a device")
    print("5. Search for a device")
    print("6. Exit the program")

    command = None
    while command != Command.Exit.value:
        command = input("\nSelect one option from the list (1, 2, 3, 4 or 5): ")

        if command not in [item.value for item in Command]:
            print("Invalid selection. Try again.")
        elif command == Command.Exit.value:
            print("Thank you for using the application!")
        else:
            device_list = readFile(devices_filename)

            if command == Command.View.value:
                viewDeviceList(device_list)
            elif command == Command.Add.value:
                addDevice(device_list)
            elif command == Command.Delete.value:
                deleteDevice(device_list)
            elif command == Command.Update.value:
                updateDevice(device_list)
            elif command == Command.Search.value:
                searchDevice(device_list)

            is_continue = ""
            while is_continue.lower() != "n" and is_continue.lower() != "y":
                is_continue = input("\nDo you want to continue? (y/n): ")
                if is_continue.lower() != "n" and is_continue.lower() != "y":
                    print("Invalid selection. Try again.")
            else:
                if is_continue.lower() == "n":
                    print("Thank you for using the application!")
                    break


def viewDeviceList(device_list):
    if len(device_list) > 0:
        for device in device_list:
            print(device[0], device[1])
    else:
        print("No device found")


def addDevice(device_list):
    add_device = input("Add device, format [code] [device name]: ").split(" ", 1)

    if len(add_device) > 1:
        device_list.append(add_device)

        is_device_added = writeFile(device_list, devices_filename)
        if is_device_added:
            print(add_device[0], add_device[1], "is added")
    else:
        print("Invalid input. Format: [code] [device name]")

    # pending: validation of the code (for confirmation)


def deleteDevice(device_list):
    device_code = input("Enter code to delete device: ")

    for idx, device in enumerate(device_list):
        if device_code in device:
            deleted_device = device_list.pop(idx)

            is_device_deleted = writeFile(device_list, devices_filename)
            if is_device_deleted:
                print(deleted_device[0], deleted_device[1], "is deleted")
            break
    else:
        print("Device code", device_code, "is not found")


def updateDevice(device_list):
    device_code = input("Enter code to update device: ")

    for idx, device in enumerate(device_list):
        if device_code in device:
            device_name = input("New device name: ")
            device_list[idx][1] = device_name

            is_device_updated = writeFile(device_list, devices_filename)
            if is_device_updated:
                print(device_list[idx][0], "is updated with device name", device_list[idx][1])
            break
    else:
        print("Device code", device_code, "is not found")


def searchDevice(device_list):
    device_keyword = input("Enter keyword: ")

    keyword_ctr = 0
    for idx, device in enumerate(device_list):
        if device_keyword.lower() in "".join(device).lower():
            print(device_list[idx][0], device_list[idx][1])
            keyword_ctr += 1

    if keyword_ctr == 0:
        print("Keyword", device_keyword, "is not found")


def validateDeviceCode():
    print("device code validation")


def readFile(filename):
    try:
        with open(filename, "rb") as file:
            content_list = pickle.load(file)
    except EOFError:
        content_list = []
    except FileNotFoundError:
        print("File not found:", filename)
        content_list = None
    return content_list


def writeFile(content_list, filename):
    try:
        with open(filename, "wb") as file:
            pickle.dump(content_list, file)
    except Exception as err:
        print("Unexpected error: ", err)
        return False

    return True


main()
