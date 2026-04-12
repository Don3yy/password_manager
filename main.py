import hashlib
from cryptography.fernet import Fernet
import json
import os

passwords = []

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
    site = input("Service/site: ")
    username = input("Username: ")
    password = input("Password: ")

    encrypted_password = encrypt_password(password)
    
    encrypted_password_dict = {
        "site" : site,
        "username" : username,
        "password" : encrypted_password
    }

    encrypted_password_json = json.dumps(encrypted_password_dict)
    
    print("\nSaving password...")
    saved = save_password(encrypted_password_json)
    if not saved: 
        print("An error occured!")

    print("Password saved!")

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

def save_password(encrypted_password_json):
    print("\nWriting to 'vault.json'...")
    try:
        with open("vault.json", "a") as f:
            f.write(encrypted_password_json)
            f.write('\n')
            return True
    except PermissionError:
        print("Permission denied!")
        return False


def view_passwords():

    load_passwords()
    if not passwords:
        print("\nNo passwords yet!")
        return
    
    #print(passwords)

    for i in range (0, len(passwords)):
        password = passwords[i]
        print(f"\n{i+1}. {password["site"]}")
        print(f"       Username: {password["username"]}")
        print(f"       Password: {decrypt_password(password["password"].strip())}")
        

def load_passwords():
    global passwords
    passwords = []

    try:
        print("\nReading 'vault.json'...")
        with open("vault.json", "r") as f:
            for line in f:
                password_dict = json.loads(line)
                passwords.append(password_dict)
    except FileNotFoundError:
        print("File 'vault.json' doesn't exist!")
    except PermissionError:
        print("Permission denied")


def delete_password():
    view_passwords()
    global passwords
    try:
        if len(passwords) == 0:
            return
        elif len(passwords) == 1:
            opt = int(input(f"\nSelect password to delete (1): "))
        else:
            opt = int(input(f"\nSelect password to delete (1 - {len(passwords)}): "))
    except ValueError:
        print("\n ->Please enter a valid option!\n")
        return
    
    if opt < 1 or opt > len(passwords):
        print("\n ->Please enter a valid option!\n")
        return
    
    del passwords[opt-1]
    save_passwords()
    print("Password deleted!")

def save_passwords():
    global passwords
    print("Writing to 'vault.json'...")
    try:
        with open("vault.json", "w") as f:
            for password in passwords:
                f.write(json.dumps(password))
                f.write('\n')
    except FileNotFoundError:
        print("File 'vault.json' does not exist!")
        return
    except PermissionError:
        print("Permission denied!")
        return


def search_password():
    search_term = input("Search for: ").strip().lower()

    load_passwords()
    if not passwords:
        print("\nNo passwords yet!")

    i = 0
    for password in passwords:
        if search_term in password["site"].strip().lower():
            i+=1
            print(f"\n{i}. {password["site"]}")
            print(f"       Username: {password["username"]}")
            print(f"       Password: {decrypt_password(password["password"].strip())}")
            
    if i == 0:
        print("No matching patterns found!")
        

def main():

    print("====== Password Manager ========")
    for i in range (0, 3):
        key = input("Enter master key: ")
        correct = check_key(key)
        
        if correct:
            break
        if i == 2:
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
                    print("\n->> Add passwords <<-")
                    added = add_password()
                case 2:
                    print("\n->> View passwords <<-")
                    view_passwords()
                case 3:
                    print("\n->> Search passwords <<-")
                    search_password()
                case 4:
                    print("\n->> Delete passwords <<-")
                    delete_password()
                case 5:
                    break
        except ValueError:
            print("\n ->Please enter a valid option!\n")

            
if __name__ == "__main__":
    main()
