import base64
import os
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def create_encrypted_key():
    password = input("Введите пароль для генерации ключа шифрования: ")
    password = bytes(password, 'utf-8')
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key.decode()


def create_hash(data):
    if data is None:
        return None
    with open('config.json', 'r') as file:
        config = json.load(file)
        key = config['key']
    key = bytes(key, 'utf-8')
    f = Fernet(key)
    generated_hash = f.encrypt(bytes(data, 'utf-8'))
    return generated_hash.decode()


def decode_hash(hash_from_db):
    with open('config.json', 'r') as file:
        config = json.load(file)
        key = config['key']
    key = bytes(key, 'utf-8')
    f = Fernet(key)
    data = f.decrypt(bytes(hash_from_db, 'utf-8'))
    return data.decode()












