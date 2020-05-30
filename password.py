from secret import DATABASE


class Password:

    normalChars = list(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#_")

    specialChars = list("""~`!@#$%^&*()_-+={[}]|\:;"'<,>.?/""")

    row_format = "{:^25}" * (4)

    def __init__(self, password, username, site):
        self.password = password
        self.username = username
        self.site = site

    @staticmethod
    def getPassword(symbolSequence, length):
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

    def encrypt(self, key):
        """Encrypts the username, password and site"""
        from cryptography.fernet import Fernet
        f = Fernet(key)
        password = f.encrypt(self.password.encode()).decode()
        self.password = password
        self.username = f.encrypt(self.username.encode()).decode()
        self.site = f.encrypt(self.site.encode()).decode()

    def show(self, index=""):
        print(Password.row_format.format(
            index, self.site, self.username, self.password))

    @classmethod
    def fromToken(cls, tokens, key):
        """Initialize the Password Class from Token."""
        plain = []
        from cryptography.fernet import Fernet
        f = Fernet(key)
        for token in tokens:
            _plain = f.decrypt(token.encode()).decode()
            plain.append(_plain)
        username, password, site = plain
        return cls(password, username, site)

    def out(self):
        return self.password

    def __str__(self):
        return "*"*len(self.password)

    @staticmethod
    def getKey(masterPassword):
        """Returns Fernet.key from the master Password."""
        import base64
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

    @staticmethod
    def validate():
        import getpass
        from cryptography.fernet import Fernet
        import secret
        authoriser = Password.getAuthoriser()
        for i in range(3):
            master = getpass.getpass(prompt="Enter Master Password:")
            key = Password.getKey(master)
            f = Fernet(key)
            _auth = f.decrypt(authoriser.encode()).decode()
            if _auth == secret.authoriser:
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
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM authoriser")
        authoriser = cur.fetchone()
        conn.close()
        if authoriser:
            return authoriser[0]
        else:
            return None
