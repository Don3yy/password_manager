# -- Notes --
# . Hashed "master" key, encrypted passwords
# . JSON
import hashlib
from cryptography.fernet import Fernet

def check_key(key):
    enc_key = key.encode()
    digest = hashlib.sha256(enc_key).hexdigest()

    try:
        with open("master.hash") as f:
            stored_hash = f.read()
    except FileNotFoundError:
        print("'master.hash' not in specified dir")
        return False
    except PermissionError:
        print("Permission denied")
        return False

    if digest.strip() == stored_hash.strip():
        print("Password Correct!\n")
        return True
    else:
        print("Password Incorrect!\n")
        return False


def add_password():
    print("\n->> Add passord <<-")
    service = input("Service/site e.g. github.com: ")
    username = input("Username: ")
    password = input("Password: ")

    password_enc = enc_password(password)
    #need to add encryption -> figure out how to store the key

    password_enc_json = {
        service : {
            "username" : username,
            "password" : password_enc
        }
    } 

    print(password_enc_json)

def enc_password(password):
    with open("key") as f:
        key = f.read().strip().encode()

    fern = Fernet(key)
    return fern.encrypt(password.encode()).decode()


def main():

    print("====== Password Manager ========")
    key = input("Enter master key: ")
    correct = check_key(key)
    
    if not correct:
        return
    
    while True:
        print("---- Options ----")
        print("1. Add password")
        print("2. View passwords")
        print("3. Search password")
        print("4. Delete password")
        
        try: 
            opt = int(input("Select option: "))
            break
        except ValueError:
            print("Please enter a valid option!\n")

    match opt:
        case 1:
            add_password()
            """
        case 2:
            #view_passwords()
        case 3:
            #search_password()
        case 4:
            #delete_password()
            """
            
if __name__ == "__main__":
    main()
