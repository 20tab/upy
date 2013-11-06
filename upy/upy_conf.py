"""
Contains come utilities used by settings.py to configure a upy project
"""
import os, sys


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
    if config.USE_UPY_SEO:
        if not config.USE_UPY_TREE:
            print "UPY improperly configured: you can't set USE_UPY_SEO = True if USE_UPY_TREE is False"
            sys.exit()
        if not hasattr(config, "LANGUAGES") or not config.LANGUAGES:
            print "UPY improperly configured: you can't set USE_UPY_SEO = True without LANGUAGES"
            sys.exit()
        if not config.USE_MODELTRANSLATION:
            print "UPY improperly configured: you can't set USE_UPY_SEO = True if USE_MODELTRANSLATION is False"
            sys.exit()
    if not config.CKEDITOR_UPLOADS or config.CKEDITOR_UPLOADS == '':
        print "UPY improperly configured: you have to set CKEDITOR_UPLOADS variable"
        sys.exit()
    if not config.USE_UPY_COLOR and config.USE_CUSTOM_ADMIN:
        print "UPY improperly configured: you can't set USE_CUSTOM_ADMIN = True if USE_UPY_COLOR is False"
        sys.exit()
    for host in config.ALLOWED_HOSTS:
        if "_" in host:
            print "UPY improperly configured: you can't set ALLOWED_HOSTS with some \"_\""
            sys.exit()
