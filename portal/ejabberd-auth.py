#!/usr/bin/env python

# File Name: 'ejabberd-auth'
#
# Project: 'Integratech'
#
# Created: '4/10/14', '4:48 PM'
#
# Author: 'Ganea Ionut Iulian' (ionut.ganea@vitheia.com)
#
# Copyright (c) Vitheia Development S.R.L All rights reserved.
"""
Usage: ejabberd-auth.py

Run as an ejabberd external authentication program and accept any
authentication request that uses a password that matches the value
of the BOSH_SECRET Django setting.

How to configure and use:
- generate a random secret and save it in your Django settings file
  under the name BOSH_SECRET
- create a wrapper script that sets DJANGO_SETTINGS_MODULE and
  PYTHONPATH to the desired values and executes this script:

#/bin/sh

export DJANGO_SETTINGS_MODULE=...
export PYTHONPATH=...

# ADD THE FOLLOWING LINE
exec /path/to/ejabberd-auth.py

# OR THE NEXT
exec /path_to_virtual_env/python /path/to/ejabberd-auth.py

- configure ejabberd to use the above wrapper script, for example:

{host_config, "localhost", [{auth_method, [external, internal]},
                            {extauth_program, "/etc/ejabberd/ejabberd-auth-wrapper"}]}.

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
    """Script is configurable:
        - run with hard coded BOSH_SECRET;
        - run with auto generated tokens.
    """
    logger.info("inside auth")
    #return True 
    try:
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            # End Tunnel specific
            return True
            # Tunnel specific .....
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
    #auth("tedddst1","22222","test1")
    
