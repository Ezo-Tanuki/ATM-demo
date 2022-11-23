from user import User

class Customer(User):
    def __init__(self, name : str, password : str, balance : int = 0) -> None:
        self._balance = balance
        super().__init__(name, password, False)

    def getBalance(self) -> int:
        return self._balance