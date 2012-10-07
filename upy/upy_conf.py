"""
Contains come utilities used by settings.py to configure a upy project
"""
import os,sys

def upy_static():
    """
    Returns upy_static path
    """
    PROJECT_PATH = os.path.realpath(os.path.dirname(__file__)) 
    return os.path.join(PROJECT_PATH, 'upy_static')

def upy_templates():
    """
    Returns upy templates path
    """
    PROJECT_PATH = os.path.realpath(os.path.dirname(__file__)) 
    return os.path.join(PROJECT_PATH, 'templates')

def upy_tpl():
    """
    Returns upy.contrib.tree templates path
    """
    PROJECT_PATH = os.path.realpath(os.path.dirname(__file__)) 
    return os.path.join(PROJECT_PATH, 'contrib/tree/tpl')

def upy_locale():
    """
    Returns upy locale path
    """
    PROJECT_PATH = os.path.realpath(os.path.dirname(__file__)) 
    return os.path.join(PROJECT_PATH, 'locale')

def validate_config(config):
    """
    Validates config.py before launching some manage's functions
    """
    check_uwsgi_config(config)
    if not config.USE_UPY_G11N:
        if config.USE_UPY_TREE:
            print "UPY improperly configured: you can't set USE_UPY_TREE = True if USE_UPY_G11N is False"
            sys.exit()
    if not config.USE_UPY_TREE:
        if config.USE_UPY_ROUTING:
            print "UPY improperly configured: you can't set USE_UPY_ROUTING = True if USE_UPY_TREE is False"
            sys.exit()
        if config.USE_STATIC_PAGE:
            print "UPY improperly configured: you can't set USE_STATIC_PAGE = True if USE_UPY_TREE is False"
            sys.exit()
    if config.MULTI_DOMAIN and not config.MULTI_PUBLICATION:
        print "UPY improperly configured: If MULTI_DOMAIN is True, MULTI_PUBLICATION must be necessarily True"
        sys.exit()
    if not config.CKEDITOR_UPLOADS or config.CKEDITOR_UPLOADS == '':
        print "UPY improperly configured: you have to set CKEDITOR_UPLOADS variable"
        sys.exit()
    if not config.USE_UPY_COLOR and config.USE_CUSTOM_ADMIN:
        print "UPY improperly configured: you can't set USE_CUSTOM_ADMIN = True if USE_UPY_COLOR is False"
        sys.exit()
        

def check_uwsgi_config(config):
    """
    Validates the uwsgi configuration before launching some manage's functions
    """
    if config.USE_UPY_NEWSLETTER:
        if not config.USE_UPY_G11N:   
            print "UPY improperly configured: you can't set USE_UPY_NEWSLETTER = True if USE_UPY_G11N is False"
            sys.exit()
        if not config.UWSGI_INI:
            print "UPY improperly configured: you can't set USE_UPY_NEWSLETTER = True without uwsgi configuration file."
            sys.exit()
        else:
            if not os.path.exists(config.UWSGI_INI):
                print "UPY improperly configured: %s doesn't exists." % config.UWSGI_INI
                sys.exit()
            spooler = False
            spooler_chdir = False
            for line in open(config.UWSGI_INI):
                if line[:7] == "spooler" and (line[7:8] == " " or line[7:8] == "="):
                    spooler = True
                if line[:13] == "spooler-chdir":
                    spooler_chdir = True
            if not spooler or not spooler_chdir:
                print "UPY improperly configured: spooler or spooler-chdir not defined in %s" % config.UWSGI_INI
                sys.exit()