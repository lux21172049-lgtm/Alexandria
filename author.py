import json
import hashlib


def hash_password(password:str) -> str:
    password_bytes = password.encode("utf-8")
    hashed = hashlib.sha256(password_bytes).hexdigest()
    return hashed 
def load():
    with open('user2.json','r') as file:
        return json.load(file)
def autor(username,password):
    users = load()
    print(users)
    if username in users and  users[username] == hash_password(password):
        return True
    return False   
