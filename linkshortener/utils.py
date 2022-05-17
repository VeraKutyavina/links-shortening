import os
import hashlib

LENGTH = 10


# Creates hash with salt for user url

def generate_link_hash(long_link):
    salt = os.urandom(32)
    plaintext = long_link.encode()

    # params: (hash algorithm, byte string of url, salt, e number of times the hash algorithm is called, length)
    a = hashlib.pbkdf2_hmac('sha256', plaintext, salt, 10000, LENGTH).hex()

    return a


# Generate short link for url

def generate_short_url(model_instance):
    link_hash = generate_link_hash(model_instance.long_link)

    model_class = model_instance.__class__

    # Call method again if string have already exist
    if model_class.objects.filter(short_link=link_hash).exists():
        return generate_short_url(model_instance)

    return link_hash
