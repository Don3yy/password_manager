import hashlib
from cryptography.fernet import Fernet
import json

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
        print("Password Correct!")
        return True
    else:
        print("Password Incorrect!\n")
        return False


def add_password():
    print("\n->> Add passord <<-")
    service = input("Service/site: ")
    username = input("Username: ")
    password = input("Password: ")

    encrypted_password = encrypt_password(password)

    #convert to json
    encrypted_password_json = json.dumps({
        service : {
            "username" : username,
            "password" : encrypted_password
        }
    })

    try:
        print("\nWriting to 'vault.json'...")
        with open("vault.json", "a+") as f:
            f.write(encrypted_password_json)   # to-do: check duplicate capability
            f.write("\n")
    except PermissionError:
        print("Permission denied")

    return True

def encrypt_password(password):
    with open("key") as f:
        key = f.read().strip().encode()

    fern = Fernet(key)
    return fern.encrypt(password.encode()).decode()

def decrypt_password(password):
    with open("key") as f:
        key = f.read().strip().encode()

    fern = Fernet(key)
    return fern.decrypt(password.encode()).decode()


def view_passwords():
    print("\n->> View passwords <<-")
    passwords = []
    try:
        with open("vault.json", "r") as f:
            for line in f:
                password_dict = json.loads(line)
                passwords.append(password_dict)
    except FileNotFoundError:
        print("File 'vault.json' does not exist!")
        return
    except PermissionError:
        print("Permission denied")
        return

    for i in range(0, len(passwords)):
        password = passwords[i]
        r = list(password.keys())
        key = r[0]
    
        print(f"\n{i+1}. {key}: ")
        print(f"      Username: {password[key]['username']}")
        print(f"      Password: {decrypt_password(password[key]['password'].strip())}")


#def delete_password():
    


def main():

    print("====== Password Manager ========")
    key = input("Enter master key: ")
    correct = check_key(key)
    
    if not correct:
        return
    
    while True:
        print("\n---- Options ----")
        print("1. Add password")
        print("2. View passwords")
        print("3. Search password")
        print("4. Delete password")
        print("5. Exit")
        
        try: 
            opt = int(input("Select option: "))
            match opt:
                case 1:
                    added = add_password()
                    if added:
                        print("Password added!")
                    else:
                        print("Password already exists!")
                case 2:
                    view_passwords()
                    """
                case 3:
                    search_password()
                case 4:
                    delete_password()
                    """
                case 5:
                    break
        except ValueError:
            print("\n ->Please enter a valid option!\n")

            
if __name__ == "__main__":
    main()
