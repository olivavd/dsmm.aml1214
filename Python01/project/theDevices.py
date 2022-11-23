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
import os

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

    login_attempt = 0
    is_login_account = False

    account_list = readFile(accounts_filename)

    # If there are no errors reading the account file
    if account_list is not None:

        while login_attempt != 3:
            username = input("Enter username: ")
            password = input("Enter password: ")

            for account in account_list:
                if username in account[0] and password in account[1]:
                    is_login_account = True
                    break
            else:
                print("Invalid username and/or password\n")

            if is_login_account:
                print("Log In Successful\n")
                break

            login_attempt += 1
        else:
            print("You have exceeded three login attempts")

    return is_login_account


def startDeviceManagement():

    print("+++++++++++++++++++++++++++++++++++++++++++++++++")
    print("+    Welcome to the Device Management System    +")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++")

    command = None
    while command != Command.Exit.value:
        print()
        print("1. View all device")
        print("2. Add a device")
        print("3. Delete a device")
        print("4. Update a device")
        print("5. Search for a device")
        print("6. Exit the program")

        command = input("\nSelect one option from the list (1, 2, 3, 4, 5 or 6): ")

        if command not in [item.value for item in Command]:
            print("Invalid selection. Try again.")
        elif command == Command.Exit.value:
            print("Thank you for using the application!")
        else:
            device_list = readFile(devices_filename)

            # If there is an error reading the device file
            if device_list is None:
                print("Exiting application...")
                break

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
                is_continue = input("\nDo you want to continue? [y/n]: ")
                if is_continue.lower() != "n" and is_continue.lower() != "y":
                    print("Invalid input. Type 'y' for yes or 'n' for no.")
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
    print("Note: Device code should consist of 7 numbers and 2 characters")
    add_device = input("Add device, format [device code] [device name]: ").split(" ", 1)

    if len(add_device) <= 1:
        print("Invalid input. Format: [code] [device name]")
    elif not isValidDeviceCode(add_device[0]):
        print("Invalid device code pattern")
    else:
        is_continue = ""
        if isDuplicateDevice(add_device[0], add_device[1], device_list):
            while is_continue.lower() != "n" and is_continue.lower() != "y":
                is_continue = input("Record already exists. Do you want to continue? [y/n]: ")
                if is_continue.lower() != "n" and is_continue.lower() != "y":
                    print("Invalid input. Type 'y' for yes or 'n' for no.")
        else:
            is_continue = "y"

        if is_continue.lower() == "y":
            device_list.append(add_device)
            is_device_added = writeFile(device_list, devices_filename)
            if is_device_added:
                print(add_device[0], add_device[1], "is added")
        else:
            print(add_device[0], add_device[1], "is not added")


def deleteDevice(device_list):
    device_code = input("Enter code to delete device: ")

    device_name_list = getDeviceName(device_code, device_list)

    if len(device_name_list) > 0:

        if len(device_name_list) == 1:
            device_num_list = "1"   # only 1 record found
        else:
            device_num_list = input("Enter number to delete device (comma separated): ").split(",")

        del_ctr = 0
        for device_num in device_num_list:
            device_num_ctr = 0

            for idx, device_name in enumerate(device_name_list):
                if device_num == str(device_name[0]):
                    orig_device_idx = device_name_list[idx][1] - del_ctr
                    deleted_device = device_list.pop(orig_device_idx)

                    device_num_ctr += 1
                    del_ctr += 1

                    is_device_deleted = writeFile(device_list, devices_filename)
                    if is_device_deleted:
                        print(deleted_device[0], deleted_device[1], "is deleted")
                    break

            if device_num_ctr == 0:
                print("Invalid device name number", device_num, ". Skipped..")


def updateDevice(device_list):
    device_code = input("Enter code to update device: ")

    device_name_list = getDeviceName(device_code, device_list)

    if len(device_name_list) > 0:

        if len(device_name_list) == 1:
            device_num_list = "1"   # only 1 record found
        else:
            device_num_list = input("Enter number to update device (comma separated): ").split(",")

        for device_num in device_num_list:
            device_num_ctr = 0

            for idx, device_name in enumerate(device_name_list):
                if device_num == str(device_name[0]):
                    print("Old device name:", device_name_list[idx][2])
                    new_device_name = input("New device name: ")

                    orig_device_idx = device_name_list[idx][1]
                    device_list[orig_device_idx][1] = new_device_name
                    device_num_ctr += 1

                    is_device_updated = writeFile(device_list, devices_filename)
                    if is_device_updated:
                        print("Device name is updated successfully")
                    break

            if device_num_ctr == 0:
                print("Invalid device name number", device_num, ". Skipped..")


def searchDevice(device_list):
    device_keyword = input("Enter keyword: ")

    keyword_ctr = 0
    for idx, device in enumerate(device_list):
        if device_keyword.lower() in "".join(device).lower():
            print(device_list[idx][0], device_list[idx][1])
            keyword_ctr += 1

    if keyword_ctr == 0:
        print("Keyword", device_keyword, "is not found")


def getDeviceName(device_code, device_list):
    new_device_name_list = []
    device_ctr = 1

    device_name_list = [[idx, device_list[idx][1]] for idx, device in enumerate(device_list) if device_list[idx][0] == device_code]

    if len(device_name_list) == 0:
        print("Device code", device_code, "is not found")
    else:
        if len(device_name_list) > 1:
            print("Device names using code", device_code)

        for idx, device_name in enumerate(device_name_list):
            if len(device_name_list) > 1:
                print(str(device_ctr)+".", device_name[1])
            # list contains: [0] temp ID [1] index from original list [2] device name
            new_device_name_list.append([device_ctr, device_name[0], device_name[1]])
            device_ctr += 1

    return new_device_name_list


def isValidDeviceCode(device_code):
    device_code_pattern = re.compile(r"\d{7}\w{2}")
    result = device_code_pattern.fullmatch(device_code)
    return True if result is not None else False


def isDuplicateDevice(device_code, device_name, device_list):
    has_duplicate = False
    for device in device_list:
        if device_code in device[0] and device_name in device[1]:
            has_duplicate = True
            break
    return has_duplicate


def readFile(filename):
    try:
        with open(filename, "rb") as file:
            content_list = pickle.load(file)
    except EOFError:
        content_list = []
    except Exception as err:
        print("Unexpected error:", err)
        content_list = None

    return content_list


def writeFile(content_list, filename):
    try:
        with open(filename, "wb") as file:
            pickle.dump(content_list, file)
    except Exception as err:
        print("Unexpected error:", err)
        return False

    return True


main()
