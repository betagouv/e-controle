from django import forms
import binascii
import os


def generate_token():
    return binascii.hexlify(os.urandom(20)).decode()


def raise_error():
    """
    Juste raise an erro - this can be used as a call back function
    when no user was found in DB during the login process.
    """
    raise forms.ValidationError(f"Aucun utilisateur trouvé")
