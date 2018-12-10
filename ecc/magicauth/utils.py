from random import randint


def generate_numeric_token():
    return str("%06d" % randint(0, 999999))
