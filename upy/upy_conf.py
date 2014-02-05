"""
Contains come utilities used by settings.py to configure a upy project
"""
import os
import sys


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


def validate_config(USE_UPY_SEO, USE_UPY_TREE, LANGUAGES, USE_MODELTRANSLATION, USE_UPY_COLOR,
                    USE_CUSTOM_ADMIN, ALLOWED_HOSTS):
    """
    Validates local_settings.py before launching some manage's functions
    """
    if USE_UPY_SEO:
        if not USE_UPY_TREE:
            print "UPY improperly configured: you can't set USE_UPY_SEO = True if USE_UPY_TREE is False"
            sys.exit()
        if not LANGUAGES:
            print "UPY improperly configured: you can't set USE_UPY_SEO = True without LANGUAGES"
            sys.exit()
        if not USE_MODELTRANSLATION:
            print "UPY improperly configured: you can't set USE_UPY_SEO = True if USE_MODELTRANSLATION is False"
            sys.exit()
    if not USE_UPY_COLOR and USE_CUSTOM_ADMIN:
        print "UPY improperly configured: you can't set USE_CUSTOM_ADMIN = True if USE_UPY_COLOR is False"
        sys.exit()
    for host in ALLOWED_HOSTS:
        if "_" in host:
            print "UPY improperly configured: you can't set ALLOWED_HOSTS with some \"_\""
            sys.exit()
