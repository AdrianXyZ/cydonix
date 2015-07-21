auth_wrapper.sh +ejabberd-auth.py
 

 auth_wrapper.sh -    script that sets DJANGO_SETTINGS_MODULE and
  PYTHONPATH to the desired values and executes this script  ejabberd-auth.py

 ejabberd-auth.py -  is a simple python script to be used for external authentication in ejabberd. The script can be used to  authenticate against a database from Django project. 



Requirements
 
   Python
   Django
   Database(SQLlite)

Usage
In order to use  auth_wrapper.sh you have to edit the ejabberd configuration in your ejabberd.cfg:
-configure ejabberd to use the above wrapper script, for example:

{auth_method, external}.

{extauth_program, "/path/to/auth_wrapper.sh"}]}.
