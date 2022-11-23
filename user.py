class User():
    def __init__(self, name : str, password : str, privilege : bool) -> None:
        self.__name = name
        self.__password = password
        self.__isAdmin = privilege

    def getPassword(self) -> str:
        return self.__password

    def getName(self) -> str:
        return self.__name

    def _getPrivilege(self) -> bool:
        return self.__isAdmin