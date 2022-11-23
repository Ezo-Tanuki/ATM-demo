from admin import Administrator
from customer import Customer

class ATM():
    def __init__(self, name : str, addAdminPassword : str) -> None:
        
        self.__name = name
        self.__addAdminPassword = addAdminPassword
        self.__numOfUser = 0
        self.__user = {"Admin" : Administrator("Admin", "12345")}
        self.__currentClient = None

    def __checkUser(self, name : str) -> bool:
        if self.__user.get(name, None) == None:
            return False

        return True

    def __confirmation(self):
        confirmation = input().lower()

        while confirmation != 'y' and confirmation != 'n':
            confirmation = input().lower()

        return confirmation

    def __overwriteConfirmation(self, name : str) -> str:
        print(f"The user with the name {name} is already created, overwrite? (y/n)")
        return self.__confirmation()

    def __addAdmin(self, name : str, password : str) -> bool:
        if self.__checkUser(name):
            confirmation = self.__overwriteConfirmation(name)
            if confirmation == 'n':
                return False

        self.__user.update({name: Administrator(name, password)})
        self.__numOfUser += 1
        return True

    def __checkPrivilege(self) -> bool:
        return self.__currentClient._getPrivilege()

    def __addCustomer(self, name : str, pin : str, balance : int = 0) -> bool:
        if not self.__checkPrivilege:
            print("You have no access to this feature!")
            return False

        if self.__checkUser(name):
            confirmation = self.__overwriteConfirmation(name)
            if confirmation == 'n':
                return False

        self.__user.update({name: Customer(name, pin, balance)})
        self.__numOfUser += 1
        return True

    def __addCustomerProc(self):
        name = input("Enter the username:\n")
        password = input("Enter the password:\n")
        balance = int(input("Enter the balance (optional):\n"))
        self.__addCustomer(name, password, balance)

    def __login(self) -> bool:
        name = input("Please enter your username: ")
        if not self.__checkUser(name):
            print(f"There is no user with the name {name} exist!")
            return False
        
        for i in range(5):
            password = input(f"Please enter your password ({i+1}/5): ")
            if password == self.__user[name].getPassword():
                print("Login successfully!")
                self.__currentClient = self.__user[name]
                return True
        
        print("Please try again!")
        return False

    def __logout(self) -> bool:
        self.__currentClient = None
        return True

    def __deposit(self, amount : int) -> bool:
        user = self.__currentClient
        user._balance += amount
        print(f"Money deposited, current balance: {user._balance}")
        return True
    
    def __withdraw(self, amount : int) -> bool:
        user = self.__currentClient
        if user._balance < amount:
            print("The withdraw amount is greater than the balance")
            return False
        
        user._balance -= amount
        print(f"Money withdrawn, current balance: {user._balance}")
        return True

    def __checkBalance(self) -> int:
        return self.__currentClient._balance
    
    def __addAdminProc(self) -> bool:
        password = input("Enter password: ")
        if password != self.__addAdminPassword:
            print("Wrong password!")
            return False
        newName = input("Enter new admin name: ")
        newPassword = input("Enter new password: ")
        return self.__addAdmin(newName, newPassword)
    
    def __removeUser(self) -> bool:
        if not self.__checkPrivilege:
            print("You have no access to this feature!")
            return False

        name = input("Enter the username that want to be removed: ")
        if not self.__checkUser(name):
            print(f"There is no user with the name {name} exist!")
            return False
        self.__user.pop(name)
        self.__numOfUser -= 1
        return True

    def __customerMenu(self) -> None:
        
        while True:
            print("1: Deposit", "2: Withdraw", "3: Check Balance", "4: Exit",sep="\n")
            inp = input()

            while True:
                match inp:
                    case "1":
                        amount = int(input("Money to be deposited: "))
                        self.__deposit(amount)
                        break
                    
                    case "2":
                        amount = int(input("Money to be withdrawn: "))
                        self.__withdraw(amount)
                        break
                    
                    case "3":
                        print(f"Bank account: {self.__checkBalance()}")
                        break

                    case "4":
                        break
                    
                    case _:
                        inp = input()
                        continue
            
            if inp == "4":
                break

            print("Continue? (y/n)")
            inp = self.__confirmation()
            if inp == "n":
                break
        
        print("Logout successfully!")
    
    def __adminMenu(self) -> None:
        
        while True:
            print("1: Add new admin", "2: Add new customer", "3: Remove user", "4: Exit",sep="\n")
            inp = input()

            while True:
                match inp:
                    case "1":
                        self.__addAdminProc()
                        break
                    
                    case "2":
                        self.__addCustomerProc()
                        break
                    
                    case "3":
                        self.__removeUser()
                        break

                    case "4":
                        break
                    
                    case _:
                        inp = input()
                        continue
            
            if inp == "4":
                break

            print("Continue? (y/n)")
            inp = self.__confirmation()
            if inp == "n":
                break
        
        print("Logout successfully!\n")

    def start(self) -> None:

        while True:
            self.__login()

            if self.__currentClient == None:
                continue
            
            if self.__checkPrivilege():
                self.__adminMenu()

            else:
                self.__customerMenu()
            
            self.__logout()

            print("Exit?(y/n)")
            inp = self.__confirmation()

            if inp == "y":
                break
