"""
AML-1214 Project - Fall 2022
Submitted by:
- Auradee Castro
- Bhumika Rajendra Babu
- Olivia Deguit
"""
import pickle
from enum import Enum

device_filename = "devices.txt"


class Command(Enum):
    View = "1"
    Add = "2"
    Delete = "3"
    Update = "4"
    Search = "5"
    Exit = "6"


def startDeviceManagement():
    loginAccount()

    print("+++++++++++++++++++++++++++++++++++++++++++")
    print("+ Welcome to the Device Management System +")
    print("+++++++++++++++++++++++++++++++++++++++++++")
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
            device_list = readFile(device_filename)

            if command == Command.View.value:
                viewDeviceList(device_list)
            elif command == Command.Add.value:
                addDevice(device_list)
            elif command == Command.Delete.value:
                deleteDevice(device_list)
            elif command == Command.Update.value:
                updateDevice()
            elif command == Command.Search.value:
                searchDevice()

            is_continue = ""
            while is_continue.lower() != "n" and is_continue.lower() != "y":
                is_continue = input("\nDo you want to continue? (y/n): ")
                if is_continue.lower() != "n" and is_continue.lower() != "y":
                    print("Invalid selection. Try again.")
            else:
                if is_continue.lower() == "n":
                    print("Thank you for using the application!")
                    break


# login function with username and password
# users have been pre-registered with their usernames and password, and saved in a file
# user has three attempts to try after which the app exits
def loginAccount():
    accounts_filename = "accounts"  # use pickle mode
    print("code for login")


# the view function lists all devices
def viewDeviceList(device_list):
    if len(device_list) > 0:
        for device in device_list:
            print(device[0], device[1], device[2])
    else:
        print("No device found")


# the add function adds a device when the user enters the name of the device,
# then the updated list of devices is written back to a file
def addDevice(device_list):
    add_device = input("Add device [code brand model]: ").split()
    device_list.append(add_device)

    is_device_added = writeFile(device_list, device_filename)
    if is_device_added:
        print(add_device[0], add_device[1], add_device[2], "is added")

    # pending: validation of the code (for confirmation)


# the delete function deletes a device when the user enters the device code,
# then the updated list of devices is written back to the file
def deleteDevice(device_list):
    del_device = input("Delete device [code]: ")

    for idx, device in enumerate(device_list):
        if del_device in device:
            deleted_device = device_list.pop(idx)
            is_device_deleted = writeFile(device_list, device_filename)

            if is_device_deleted:
                print(deleted_device[0], deleted_device[1], deleted_device[2], "is deleted")
            break
    else:
        print("Device code", del_device, "not found")


# the update function updates the name of a device when the user enters the device code,
# then the updated list of devices is written back to the file
def updateDevice():
    print("code for update device")


# the search function allows the user to enter a keyword
# if found the devices that contain the keyword will be returned
def searchDevice():
    print("code for search device")


def validateDeviceCode():
    print("code validation")


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


startDeviceManagement()
