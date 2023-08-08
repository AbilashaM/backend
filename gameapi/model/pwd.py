#hashing password
import hashlib

def encode_password (password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password, hashed_password):
    encoded_password = encode_password(password)
    if(encoded_password == hashed_password):
        return True
    else:
        return False