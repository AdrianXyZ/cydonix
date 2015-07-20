#!/bin/sh

export DJANGO_SETTINGS_MODULE=DjangoREST.settings
export PYTHONPATH=/home/adi/p1/cydonix/portal/DjangoREST

#venv:
pwd
cd DjangoREST
pwd  

exec /home/adi/p1/cydonix/portal/envportal/bin/python /home/adi/p1/cydonix/portal/ejabberd-auth.py
