
from re import compile

PASSWORD_REGEX = compile(r'\A(?=\S*?\d)(?=.*?[0-9])(?=.*?[#?!@$%^&*-])(?=.*[A-Za-z]){8,}\Z')
USERNAME_REGEX = compile(r'\A[\w\-\.]{3,}\Z')

def password_is_valid(password):
    match = PASSWORD_REGEX.finditer(password)

    return PASSWORD_REGEX.match(password) is not None

def username_is_valid(username):
    return USERNAME_REGEX.match(username) is not None