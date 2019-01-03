import binascii
import os


def generate_token():
    return binascii.hexlify(os.urandom(20)).decode()
