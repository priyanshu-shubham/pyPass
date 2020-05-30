"""Creates all the dependencies when using the first time"""
from cryptography.fernet import Fernet
import secret
import os
import sqlite3
import getpass
import cryptography

print("""
---------------------------PASSWORD MANAGER----------------------------
            ██████████
        ████░░░░░░░░░░████
      ██░░░░░░░░░░░░░░░░░░██
    ██░░░░░░░░░░░░░░░░░░░░░░██    ████
  ██░░░░░░░░░░░░░░░░░░░░░░░░██  ██░░██
  ██░░░░░░░░░░░░░░░░░░░░░░░░░░██░░░░████████████████████████████████
██░░░░░░██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██
██░░░░██      ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██
██░░░░██      ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██
██░░░░██      ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██░░░░░░░░██░░░░░░░░██
██░░░░░░██████░░░░░░░░░░░░░░░░░░░░░░██████░░██  ██░░░░██  ████████
  ██░░░░░░░░░░░░░░░░░░░░░░░░░░██░░░░██    ██      ████
  ██░░░░░░░░░░░░░░░░░░░░░░░░██  ██░░██
    ██░░░░░░░░░░░░░░░░░░░░░░██    ████
      ██░░░░░░░░░░░░░░░░░░██
        ████░░░░░░░░░░████
            ██████████
""")

# PROMPT FOR entering master password
while True:
    masterPass = getpass.getpass(prompt="Enter a new MASTER PASSWORD: ")
    _masterPass = getpass.getpass(prompt="Confirm the MASTER PASSWORD: ")
    if masterPass == _masterPass:
        print("----------------CONGRATS,NEW IDENTITY CREATED---------------")
        break
    else:
        print("----------------Both Passwords Don't Match--------------------")


# getkey
def getKey(masterPassword):
    """Returns Fernet.key from the master Password."""
    import base64
    from cryptography.fernet import Fernet
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    password = masterPassword.encode()
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


# Creating the authoriser text
authText = secret.authoriser
fernet = Fernet(getKey(masterPass))
cipher = fernet.encrypt(authText.encode())

# Deleting if there exists an earlier database
if os.path.exists(secret.DATABASE):
    os.remove(secret.DATABASE)


# Pushing the authoriser text in the database.
conn = sqlite3.connect(secret.DATABASE)
os.popen(f"attrib +h {secret.DATABASE}")
conn.execute("CREATE TABLE authoriser (auth blob)")
conn.execute("INSERT INTO authoriser VALUES (?)", (cipher,))
conn.commit()
conn.close()
