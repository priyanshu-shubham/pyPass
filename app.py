import secret
import dependency
from password import Password
import os
import pyperclip

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

recPass = Password.getPassword(Password.normalChars+Password.specialChars, 16)
print("Recommended Password:", recPass)
pyperclip.copy(recPass)
print("The recommended password is copied to the clipboard")

if not os.path.exists("passwordManager-passwords.db"):
    dependency.initial()

_auth = Password.getAuthoriser()
if not _auth:
    dependency.initial()
    _auth = Password.getAuthoriser()

key = Password.validate()

while True:
    response = dependency.getCommand().lower()
    if response == "quit" or response == "4" or response == "q":
        print("Thanks for Using.")
        quit()

    elif response == "1" or response == "save" or response == "s":
        username = input("ENTER USERNAME FOR THIS PASSWORD: ")
        site = input("ENTER THE WEBSITE FOR THIS USERNAME AND PASSWORD: ")
        dependency.save(username, recPass, site, key)

    elif response == "o" or response == "3" or response == "out":
        key = Password.validate()

    elif response == "a" or response == "2" or response == "avl":
        dependency.show(key)

    else:
        print("INVALID COMMAND")
