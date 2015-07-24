#!/bin/sh

export DJANGO_SETTINGS_MODULE=DjangoPROJECT.settings
export PYTHONPATH=/path/to/DjangoPROJECT

#venv:
pwd
cd /path/to/DjangoProject
pwd  

exec /path/to/env      /path/to/ejabberd-auth.py
