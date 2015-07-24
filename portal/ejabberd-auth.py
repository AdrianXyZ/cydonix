"""
Run as an ejabberd external authentication program and accept any
authentication request that uses a password that matches in django database .
"""

import django
django.setup()
import struct
import logging
import logging.handlers
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoREST.settings')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from django.conf import settings
from django.db import transaction
from django import db
from django.utils.decorators import method_decorator
from struct import *
from django.contrib.auth.models import User, check_password



def from_ejabberd():
    input_length = sys.stdin.read(2)
    (size,) = unpack('>h', input_length)
    return sys.stdin.read(size).split(':', 1)


def to_ejabberd(bool):
    answer = 0
    if bool:
        answer = 1
    token = pack('>hh', 2, answer)
    sys.stdout.write(token)
    sys.stdout.flush()
 

def auth(username, server, password):
    logger.info("inside auth")
    try:
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            return True
        else:
            logging.info(username + ' failed auth')
            return False
    except User.DoesNotExist:
        logging.info(username + ' is not a valid user')
        return False
    
    

def process():
    logger.info("inside process")
    while True:
        data = from_ejabberd()
        success = False
        if data[0] == "auth":
            (username, server, password) = data[1].split(':', 2)
            success = auth(username, server, password)
        to_ejabberd(success)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    process()
    
