import os

IN_PRODUCTION = False
"""True if application is in production, False if it's in development"""
if IN_PRODUCTION:
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
""" It defines list of additional applications for your project """
PROJECT_APP_DEFAULT = "" 
""" Must be the name of your default app. It is used to autocomplete application name in tree.template and tree.views """
PROJ_MIDDLEWARE_CLASSES = [
]
""" It defines list of additional middleware for your project """
PROJ_TEMPLATE_CONTEXT_PROCESSORS = [
]
""" It defines list of additional context processors for your project """
PROJ_TEMPLATE_DIRS = [
]
""" It defines list of additional templates' directories for your project """

UWSGI_COMMAND = "uwsgi"
""" uWSGI command location. On unbit's servers usually located to /proc/unbit/uwsgi/uwsgi. """
ADMINS = (("errors","errors@email.com"),)
""" It's important set administrators to monitor how application works """
HANDLER_404 = None 
""" The name of the view for handler404 """
HANDLER_500 = None 
""" The name of the view for handler500 """
USE_MODELTRANSLATION = False
""" True if you want install django-modeltranslation """
TIME_ZONE = 'Europe/Rome'
""" See the TIME_ZONE's details on django settings documentation """
LANGUAGE_CODE = 'it'
""" See the LANGUAGE_CODE's details on django settings documentation """
LANGUAGES = []
""" Languages list for translations """
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
USE_UPY_NEWSLETTER = False 
""" If True upy newsletter module will be installed. It needs USE_UPY_G11N = True """
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
PROJ_LOCALE_PATHS = [
]
""" List of directory for your translations """
DISALLOW_ALL_ROBOTS = False
""" If """
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.dirname(__file__) + "/../dev.db",#'/path/example.db'. Path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                     # Set to empty string for default. Not used with sqlite3.
    },
}
""" 
Databases configuration like as:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.abspath('dev.db'),#'/path/example.db'. Path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                     # Set to empty string for default. Not used with sqlite3.
    },
}
"""

######################## Newsletter configuration #########################
UPY_NEWSLETTER_SPOOLER_TIMEOUT = 300 
""" Frequency of recovery spooler in seconds """
UPY_SECRET_KEY = "test_secret_key"
""" It contributes to hashing contact secret key """
USE_LOCAL_SMTP_SERVER = True
""" If True there is no need to set smtp parameters """
EMAIL_USER = "info@email.com"
""" Default user's e-mail """ 
SERVER_EMAIL = EMAIL_USER
""" Default server's e-mail """ 
DEFAULT_FROM_EMAIL = "info@email.com"
""" Default sender's e-mail """ 
if USE_LOCAL_SMTP_SERVER:
    EMAIL_HOST_USER = EMAIL_USER
    """ Should be like EMAIL_USER. So you shouldn't set this parameters """ 
else:
    EMAIL_HOST = "localhost" # or "smtp.myexamplesite.it"
    """ smtp host """
    EMAIL_PORT = 25
    """ smtp port """
    EMAIL_HOST_USER = EMAIL_USER
    EMAIL_HOST_PASSWORD = "pswd"
    """ smtp account's password """
    EMAIL_USE_TLS = False
    """ If True account uses tls """

CKEDITOR_UPLOADS = 'uploads' 
""" Must be the only name of directory where you want upload file through ckeditor, without slash """
#######################################################################################################################################