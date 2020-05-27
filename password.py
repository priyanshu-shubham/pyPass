class Password:

    normalChars = list(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#_")

    specialChars = list("""~`!@#$%^&*()_-+={[}]|\:;"'<,>.?/""")

    __isValidated = 0

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
        """Encrypt the self.password"""
        from cryptography.fernet import Fernet
        f = Fernet(key)
        token = f.encrypt(self.password.encode()).decode()
        self.token = token
        return token

    @classmethod
    def fromString(cls, password):
        """Initialize the Password class from string."""
        instance = cls(cls.normalChars, 5)
        instance.password = password
        return instance

    @classmethod
    def fromToken(cls, token):
        """Initialize the Password Class from Token."""
        pass

    def __str__(self):
        return self.password

    @staticmethod
    def getKey(masterPassword):
        """Returns Fermet.key from the master Password."""
        import base64
        from cryptography.fernet import Fernet
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        password = masterPassword.encode()
        import secret
        salt = secret.salt
        # binary sat using os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key

    @classmethod
    def validate(cls):
        import getpass
        from cryptography.fernet import Fernet
        import secret
        # Flag:There can be problems here since maybe the fetchone method in getAuthoriser returns a tuple in place of a string.
        authoriser = Password.getAuthoriser()
        for i in range(3):
            master = getpass.getpass(prompt="Enter Master Password:")
            key = Password.getKey(master)
            f = Fernet(key)
            _auth = f.decrypt(authoriser.encode())
            if _auth == secret.authoriser:
                Password.__isValidated = 1
                return key
            else:
                print("Wrong Password")
                continue
        import sys
        sys.exit(0)

    @staticmethod
    def getAuthoriser():
        """Gets the authoriser text stored in database "passwords" which is encrypted"""
        import sqlite3
        conn = sqlite3.connect("passwords")
        cur = conn.cursor()
        result = cur.execute("SELECT * FROM authoriser")
        authoriser = cur.fetchone()[0]
        #  Flag : What cursor.fetchone returns.
        print(authoriser)
        conn.close()
        return authoriser


p1 = Password.fromString("HeyBro")
print(p1.getKey("HElooThere"))
