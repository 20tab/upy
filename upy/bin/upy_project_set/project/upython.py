#!/usr/bin/python
"""
Use this snippet like python command to run manage's functions with uWSGI
"""
import os,sys
from project import config

os.environ.update({'UWSGI_INI':config.UWSGI_INI,
                   'UWSGI_PYRUN':sys.argv[1],
                   'UWSGI_PYARGV':" ".join(sys.argv[2:])})
os.system(config.UWSGI_COMMAND)