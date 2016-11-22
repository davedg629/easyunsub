from os import urandom
from base64 import urlsafe_b64encode


# generate a random token
def generate_token():
    return urlsafe_b64encode(urandom(30)).rstrip("=")
