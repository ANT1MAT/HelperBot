import json
from encryption import create_encrypted_key


token = input('Введите токен бота:')
password = create_encrypted_key()
dictionary = {
    'key': password,
    'token': token
}
with open('config.json', 'w') as file:
    file.write(json.dumps(dictionary))

