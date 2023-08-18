import json
import re


def load_users(path):
    with open(path, 'r') as file:
        text = file.read()
        if text == '':
            users_list = []
        else:
            users_list = json.loads(text)
    return users_list


def validate_user(user):
    errors = {}
    if not user['name']:
        errors['name'] = "Can't be blank"
    if not user['email']:
        errors['email'] = "Can't be blank"

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(regex, user['email']):
        errors['email'] = "Enter a valid email address"

    return errors