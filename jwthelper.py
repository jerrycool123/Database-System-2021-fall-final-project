import os
import jwt
import random, string

def gen_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
if SECRET_KEY == None:
    SECRET_KEY = gen_random_string(64)

def encode_data(payload):
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_data(token):
    return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])