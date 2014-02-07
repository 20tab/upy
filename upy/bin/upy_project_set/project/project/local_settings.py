import os
from settings import *
gettext = lambda s: s
from upy.upy_conf import upy_templates, upy_tpl, upy_locale, validate_config

REMOTE_SERVER = False
"""True if application is in production, False if it's in development"""
if REMOTE_SERVER:
    ALLOWED_HOSTS = ('mysite.com',)
    """A list of strings representing the host/domain names that this Django site can serve."""
    UWSGI_INI = "../uwsgi_unbit.ini" 
    """ The file's name that define the uwsgi configuration. If you don't want use uwsgi define this var with None value """
    DEBUG = False
    """ True only in development to debug your application"""
else:
    ALLOWED_HOSTS = ('localhost','127.0.0.1')
    """A list of strings representing the host/domain names that this Django site can serve."""
    UWSGI_INI = "../uwsgi.ini" 
    """ The file's name that define the uwsgi configuration. If you don't want use uwsgi define this var with None value """
    DEBUG = True
    """ True only in development to debug your application"""

PROJECT_APPS = [
]
INSTALLED_APPS.extend(PROJECT_APPS)
""" It defines list of additional applications for your project """
PROJECT_APP_DEFAULT = ""
""" Must be the name of your default app. It is used to autocomplete application name in tree.template and tree.views """

DATABASES = {
    'remote': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.dirname(__file__) + "/../dev.db",#'/path/example.db'. Path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                     # Set to empty string for default. Not used with sqlite3.
    },
    'local': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.dirname(__file__) + "/../dev.db",#'/path/example.db'. Path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                     # Set to empty string for default. Not used with sqlite3.
    },
}

if REMOTE_SERVER:
    DATABASES['default'] = DATABASES['remote']
else:
    DATABASES['default'] = DATABASES['local']

UWSGI_COMMAND = "uwsgi"
""" uWSGI command location. On unbit's servers usually located to /proc/unbit/uwsgi/uwsgi. """
MANAGERS = (("errors","errors@email.com"),)
""" It's important set administrators to monitor how application works """
HANDLER_404 = None 
""" The name of the view for handler404 """
HANDLER_500 = None 
""" The name of the view for handler500 """
TIME_ZONE = 'Europe/Rome'
""" See the TIME_ZONE's details on django settings documentation """
LANGUAGE_CODE = 'it'
""" See the LANGUAGE_CODE's details on django settings documentation """
LANGUAGES = [('it',gettext('Italian')),]
""" Languages list for translations """
USE_MODELTRANSLATION = False
""" True if you want install django-modeltranslation """
USE_UPY_TREE = True
""" True if you want install tree and manage node's structure. IT NEEDS USE_UPY_G11N = True """
USE_UPY_SEO = True
""" True if you want install seo and manage meta informations IT NEEDS USE_UPY_TREE = True """
USE_UPY_ADMIN = True  
""" If True, upy admin templates will be used """
USE_CUSTOM_ADMIN = True
""" If True CustomAdmin app will be installed and you can customize your admin """
USE_UPY_COLOR = True
""" If True Colors app will be installed and you can use its utilities and widgets """
USE_UPY_ROSETTA = True 
""" If True the rosetta module will be installed """
ALLOW_STAFF_TO_ROSETTA = True 
""" If True staff can translate through rosetta """
USE_FULLHD_SUPPORT = False 
""" If True allow big size image (1920x1080px) """
RGBA_FILTER = True 
""" Allow only RGB and RGBa images' modes """
USE_UPY_JQUERY_LIB = True
""" If True standard upy jquery library will be included in base template """
USE_UPY_JQUERYUI_LIB = False
""" If True standard upy jquery ui library will be included in base template """
USE_UPY_CSS_RESET = True
""" If True standard upy css reset will be included in base template """
USE_GLOBAL_TEMPLATES_DIR = True
""" If True upy.contrib.tree.Template saves templates in the global directory else in the application templates directory """
SECRET_KEY = 'secret_key_example'
""" Make this unique, and don't share it with anybody. """
DISALLOW_ALL_ROBOTS = False
""" If True the directive: \"User-agent: * Disallow: /\" will be added in robots.txt """
USE_LOCAL_SMTP_SERVER = True
""" If True there is no need to set smtp parameters """
EMAIL_USER = "info@emailtest.com"
""" Default user's e-mail """ 
SERVER_EMAIL = EMAIL_USER
""" Default server's e-mail """ 
DEFAULT_FROM_EMAIL = "info@emailtest.com"
""" Default sender's e-mail """
CKEDITOR_UPLOADS = 'uploads' 
""" Must be the only name of directory where you want upload file through ckeditor, without slash """

if USE_UPY_TREE:
    MIDDLEWARE_CLASSES.append('upy.contrib.tree.middleware.upy_context.SetUpyContextMiddleware')

if USE_UPY_TREE:
    TEMPLATE_CONTEXT_PROCESSORS.append("upy.contrib.tree.template_context.context_processors.set_meta")
    if USE_UPY_SEO:
        TEMPLATE_CONTEXT_PROCESSORS.append("upy.contrib.seo.template_context.context_processors.set_meta")
if USE_CUSTOM_ADMIN:
    TEMPLATE_CONTEXT_PROCESSORS.append("upy.contrib.customadmin.template_context.context_processors.customadmin_context")
if USE_UPY_ADMIN:
    TEMPLATE_CONTEXT_PROCESSORS.append("upy.template_context.context_processors.use_upy_admin")

GLOBAL_TEMPLATES_DIR = '../templates'
TEMPLATE_DIRS = [GLOBAL_TEMPLATES_DIR]
if USE_GLOBAL_TEMPLATES_DIR:
    list_dirs = ["%s/%s" % (GLOBAL_TEMPLATES_DIR, tdir) for tdir in os.listdir(GLOBAL_TEMPLATES_DIR)]
    if list_dirs:
        TEMPLATE_DIRS.extend(list_dirs)
if USE_UPY_ADMIN:
    TEMPLATE_DIRS.extend(
        [upy_templates(),upy_tpl(),]
    )

LOCALE_PATHS = [upy_locale()]

if USE_UPY_TREE:
    INSTALLED_APPS.append('upy.contrib.tree')
    if USE_UPY_SEO:
        INSTALLED_APPS.append('upy.contrib.seo')

if USE_FULLHD_SUPPORT:
    PIL_IMAGEFILE_MAXBLOCK = 256 * 2 ** 13 # 2MB
    UPYIMAGE_LIMIT_AREA = 2073700 # 1920*1080px +
else:
    PIL_IMAGEFILE_MAXBLOCK = 256 * 2 ** 10 # 260KB
    UPYIMAGE_LIMIT_AREA = 1049188 # 1366*768px +

if USE_UPY_COLOR:
    INSTALLED_APPS.append('upy.contrib.colors')

if USE_CUSTOM_ADMIN:
    INSTALLED_APPS.append('upy.contrib.customadmin')

if USE_UPY_ROSETTA:
    INSTALLED_APPS.append('upy.contrib.rosetta')

if USE_MODELTRANSLATION:
    INSTALLED_APPS.extend(
        ['modeltranslation','upy.contrib.tabbed_translation']
    )

TEMPLATE_DEBUG = DEBUG

validate_config(USE_UPY_SEO, USE_UPY_TREE, LANGUAGES, USE_MODELTRANSLATION, USE_UPY_COLOR,
                USE_CUSTOM_ADMIN, ALLOWED_HOSTS)