class Password:
    normalChars = list(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#_")
    specialChars = list("~`! @#$%^&*()_-+={[}]|\:;\"'<,>.?/")

    def __init__(self, password=""):
        self.password = password

    def getPassword(self, symbolSequence, length):
        """Returns a new password of length=length with characters from symbolSequence"""
        symbolArray = list(symbolSequence)
        import random
        password = ""
        # initializing with a new password
        intpos = [i for i in range(length)]
        random.shuffle(intpos)
        n = random.randint(1, length//4)
        # atleast n places where integer will be put depending on the first n values in intpos.
        for i in range(length):
            password += symbolArray[random.randint(0, len(symbolArray)-1)]
        # putting in n integers
        for i in range(n):
            password = password[:intpos[i]] + \
                str(random.randint(0, 9))+password[intpos[i]+1:]
        return password
