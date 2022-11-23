from user import User

class Administrator(User):
    def __init__(self, name : str, password : str) -> None:
        super().__init__(name, password, True)
