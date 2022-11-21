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


# login function with username and password
# users have been pre-registered with their usernames and password, and saved in a file
# user has three attempts to try after which the app exits
def loginAccount():
    accounts_filename = "accounts"  # use pickle mode
    print("code for login")


# the view function lists all devices
def viewDeviceList(device_list):
    print("code for view device")


# the add function adds a device when the user enters the name of the device,
# then the updated list of devices is written back to a file
def addDevice(device_list):
    print("code for add device")

    # pending: validation of the code (for confirmation)


# the delete function deletes a device when the user enters the device code,
# then the updated list of devices is written back to the file
def deleteDevice(device_list):
    print("code for delete device")


# the update function updates the name of a device when the user enters the device code,
# then the updated list of devices is written back to the file
def updateDevice(device_list):
    print("code for update device")


# the search function allows the user to enter a keyword
# if found the devices that contain the keyword will be returned
def searchDevice(device_list):
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
