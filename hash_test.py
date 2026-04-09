"""
import hashlib

password = "yamiko"
enc_password = password.encode()

digest = hashlib.sha256(enc_password).hexdigest()

with open("master.hash") as f:
    stored_hash = f.read()

print(f"Digest:      {digest} {type(digest)}")
print(f"Stored hash: {stored_hash} {type(stored_hash)}")
if digest.strip() == stored_hash.strip():
    print("hell yeah!")
else:
    print("No")
name = "yamiko"
age  = 12
height = 6

dictionary = {
    name : {
        "age" : age,
        "height" : 6
    }
}

print(dictionary)
"""
from cryptography.fernet import Fernet

password = "yamiko123"

with open("key") as f:
    key = f.read().strip().encode()

fern = Fernet(key)
password_enc = fern.encrypt(password.encode())


print(password_enc.decode())
