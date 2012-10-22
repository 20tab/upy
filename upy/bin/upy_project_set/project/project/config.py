import os

UWSGI_INI = "../uwsgi.ini" 
""" The file's name that define the uwsgi configuration. If you don't want use uwsgi define this var with None value """
UWSGI_COMMAND = "uwsgi"
""" uWSGI command location. On unbit's servers usually located to /proc/unbit/uwsgi/uwsgi. """
HANDLER_404 = None 
""" The name of the view for handler404 """
HANDLER_500 = None 
""" The name of the view for handler500 """
USE_UPY_G11N = True 
""" True if you want install G11n in your project and use Globalization """
DEFAULT_LANGUAGES = [('it', 'Italian')]
""" Set default language. It's important if you don't use G11n """
USE_UPY_TREE = True 
""" True if you want install tree and manage node's structure. IT NEEDS USE_UPY_G11N = True """
MULTI_DOMAIN = False 
""" True if the application is mapped by many different domains (host). False if only a domain (host) uses this application. """
MULTI_PUBLICATION = False  
""" If MULTI_DOMAIN is True, this variable must be necessarily True otherwise it's jerk. """
USE_UPY_ADMIN = True  
""" If True, upy admin templates will be used """
#USE_UPY_ROUTING non funziona. Guardare bene upy.contrib.tree.views.render_page
USE_UPY_ROUTING = False 
""" TODO: It needs USE_UPY_TREE = True. This is a useful option to create dynamic routing without server restarting """ 
USE_CUSTOM_ADMIN = True
""" If True CustomAdmin app will be installed and you can customize your admin """
USE_UPY_COLOR = True
""" If True Colors app will be installed and you can use its utilities and widgets """
USE_STATIC_PAGE = True 
""" If True the static page module will be installed. IT NEEDS USE_UPY_G11N = True """
USE_STATIC_ELEMENT = False
""" If True the static element module will be installed. """
USE_UPY_IMAGE = False 
""" If True the image module will be installed """
USE_FULLHD_SUPPORT = False 
""" If True allow big size image (1920x1080px) """
RGBA_FILTER = True 
""" Allow only RGB and RGBa images' modes """
USE_UPY_NEWSLETTER = False 
""" If True upy newsletter module will be installed. It needs USE_UPY_G11N = True """
DEBUG = True
""" True only in development to debug your application"""
USE_UPY_JQUERY_LIB = True
""" If True standard upy jquery library will be included in base template """
USE_GLOBAL_TEMPLATES_DIR = True
""" If True upy.contrib.tree.Template saves templates in the global directory else in the application templates directory """
ADMINS = (("errors","errors@email.com"),)
""" It's important set administrators to monitor how application works """
TIME_ZONE = 'Europe/Rome'
""" See the TIME_ZONE's details on django settings documentation """
LANGUAGE_CODE = 'it-It'
""" See the LANGUAGE_CODE's details on django settings documentation """
SECRET_KEY = 'secret_key_example'
""" Make this unique, and don't share it with anybody. """
PROJ_LOCALE_PATHS = [
]
""" List of directory for your translations """
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
PROJ_MIDDLEWARE_CLASSES = [
]
""" It defines list of additional middleware for your project """
PROJ_TEMPLATE_CONTEXT_PROCESSORS = [
]
""" It defines list of additional context processors for your project """
PROJ_TEMPLATE_DIRS = [
]
""" It defines list of additional templates' directories for your project """
PROJECT_APPS = [
]
""" It defines list of additional applications for your project """
PROJECT_APP_DEFAULT = "" 
""" Must be the name of your default app. It is used to autocomplete application name in tree.template and tree.views """

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
    EMAIL_HOST = "smtp.example.it"
    """ smtp host """
    EMAIL_PORT = 25
    """ smtp port """
    EMAIL_HOST_USER = EMAIL_USER
    EMAIL_HOST_PASSWORD = "pswd"
    """ smtp account's password """
    EMAIL_USE_TLS = True
    """ If True account uses tls """
    
######################################################################################################################################   
STATICPAGE_CKE_CONFIG = {
    'height': 300,
    'width': 800,
    #'contentsCss':'/static/example_layout.css'
    # others parameters
}
"""
STATICPAGE CKEditor configuration (for all parameters, look at http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.config.html)
STATICPAGE_CKE_CONFIG = {
    'height': 300,
    'width': 800,
    #'contentsCss':'/static/example_layout.css'
    # others parameters
}
"""

STATICELEMENT_CKE_CONFIG = {
    'height': 300,
    'width': 800,
    #'contentsCss':'/static/example_layout.css'
    # others parameters
}
"""
STATICELEMENT CKEditor configuration (for all parameters, look at http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.config.html)
STATICELEMENT_CKE_CONFIG = {
    'height': 300,
    'width': 800,
    #'contentsCss':'/static/example_layout.css'
    # others parameters
}
"""

CKEDITOR_UPLOADS = 'uploads' 
""" Must be the only name of directory where you want upload file through ckeditor, without slash """
#######################################################################################################################################