import pickle


def createAccount():

    accounts = readAccount()

    print(accounts)

    name = input("Enter username: ")
    password = input("Enter password: ")

    account = [name, password]
    accounts.append(account)
    saveAccount(accounts)


def saveAccount(accounts):
    with open("accounts", "wb") as input_file:
        pickle.dump(accounts, input_file)


def readAccount():
    try:
        with open("accounts", "rb") as output_file:
            accounts = pickle.load(output_file)
    except EOFError:
        accounts = []
    except FileNotFoundError:
        print("File not found:", "accounts")
        accounts = None
    return accounts


createAccount()
