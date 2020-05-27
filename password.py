class Password:

    normalChars = list(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#_")

    specialChars = list("""~`!@#$%^&*()_-+={[}]|\:;"'<,>.?/""")

    def __init__(self, symbolSequence, length):
        self.password = self.getPassword(symbolSequence, length)

    def getPassword(self, symbolSequence, length):
        """Returns a new password of length=length with characters from symbolSequence"""
        symbolArray = list(symbolSequence)
        import random
        self.password = ""
        # initializing with a new password
        intpos = [i for i in range(length)]
        random.shuffle(intpos)
        n = random.randint(1, length//4)
        # atleast n places where integer will be put depending on the first n values in intpos.
        for i in range(length):
            self.password += symbolArray[random.randint(0, len(symbolArray)-1)]
        # putting in n integers
        for i in range(n):
            self.password = self.password[:intpos[i]] + \
                str(random.randint(0, 9))+self.password[intpos[i]+1:]
        return self.password

    def encrypt(self, key):
        from cryptography.fernet import Fernet
        pass

    @classmethod
    def fromString(cls, password):
        instance = cls(cls.normalChars, 5)
        instance.password = password
        return instance

    @classmethod
    def fromToken(cls, token):
        pass

    def __str__(self):
        return self.password


p1 = Password.fromString("HeyBro")
print(p1)
