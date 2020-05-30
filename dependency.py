from cryptography.fernet import Fernet
import secret
import os
import sqlite3
import getpass
import cryptography
from password import Password


def initial():
    """Creates all the dependencies when using the first time"""
    # PROMPT FOR entering master password
    while True:
        masterPass = getpass.getpass(prompt="Enter a new MASTER PASSWORD: ")
        _masterPass = getpass.getpass(prompt="Confirm the MASTER PASSWORD: ")
        if masterPass == _masterPass:
            print("----------------CONGRATS,NEW IDENTITY CREATED---------------")
            break
        else:
            print("----------------Both Passwords Don't Match--------------------")

    # Creating the authoriser text
    authText = secret.authoriser
    fernet = Fernet(Password.getKey(masterPass))
    cipher = fernet.encrypt(authText.encode()).decode()

    # Deleting if there exists an earlier database
    if os.path.exists(secret.DATABASE):
        os.remove(secret.DATABASE)

    # Pushing the authoriser text in the database.
    conn = sqlite3.connect(secret.DATABASE)
    os.popen(f"attrib +h {secret.DATABASE}")
    conn.execute("CREATE TABLE authoriser (auth varchar)")
    conn.execute(
        "CREATE TABLE passwords (username varchar, password varchar ,site varchar)")

    conn.execute("INSERT INTO authoriser VALUES (?)", (cipher,))
    conn.commit()
    conn.close()


def getCommand():
    menu = """





	Instruction to use:  (Case don't matter)
	1.To save the current provided password: Enter "Save" or "1" or "S".
	2.To open the list of available passwords: Enter "Avl" or "2" or "A".
	3.To LogOut: Enter "Out" or "3" or "O".
	4.To quit the app: Enter "Quit" or "4" or "Q".
	"""
    print(menu)
    return input("Command: ")


def save(username, password, site, key):
    """Saves the given password to the database"""
    password = Password(password, username, site)
    password.encrypt(key)
    conn = sqlite3.connect(secret.DATABASE)
    conn.execute(
        "INSERT INTO passwords (username, password, site) VALUES (?,?,?)", (password.username, password.password, password.site))
    conn.commit()
    conn.close()
    print(
        f"Password successfully saved with USERNAME= {username} and SITE={site}.")
    print("Press Enter To Continue.")
    input()


def show(key):
    """Shows the list of available passwords."""
    conn = sqlite3.connect(secret.DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT rowid,* FROM passwords")
    passwords = cur.fetchall()
    print(Password.row_format.format(
        "Index", "Website", "Username", "Password"))
    for i in passwords:
        tokens = i[1:]
        password = Password.fromToken(tokens, key)
        password.show(i[0])
        print("Press Enter To Continue.")
        input()
