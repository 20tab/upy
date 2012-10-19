# Django settings for UPY project.
from project.config import *
import project
from upy.upy_conf import upy_static, upy_templates,upy_tpl, validate_config, upy_locale

validate_config(project.config)

PROJECT_PATH = os.path.realpath(os.path.dirname("../"))

TEMPLATE_DEBUG = DEBUG
ROOT_URLCONF = "project.urls"
MANAGERS = ADMINS
SITE_ID = 1
USE_I18N = True
USE_L10N = True
LANGUAGES = []
if not USE_UPY_G11N:
    LANGUAGES = DEFAULT_LANGUAGES
    
STATIC_ROOT_NAME = 'static'
STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, STATIC_ROOT_NAME))
RELATIVE_STATIC_ROOT = '../%s/' % STATIC_ROOT_NAME
MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, STATIC_ROOT_NAME))
STATIC_URL = '/%s/' % STATIC_ROOT_NAME
MEDIA_URL = STATIC_URL
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware', # per i18n
]
if USE_UPY_G11N:
    MIDDLEWARE_CLASSES.append('upy.contrib.g11n.middleware.publications.SetCurrentPublicationMiddleware')
if USE_UPY_TREE:
    MIDDLEWARE_CLASSES.append('upy.contrib.tree.middleware.publications.EnabledMiddleware')
    MIDDLEWARE_CLASSES.append('upy.contrib.tree.middleware.publications.RequireLoginMiddleware')

MIDDLEWARE_CLASSES.extend(
    PROJ_MIDDLEWARE_CLASSES
)

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
]
if USE_UPY_TREE:
    TEMPLATE_CONTEXT_PROCESSORS.append("upy.contrib.tree.template_context.context_processors.g11n")
if USE_CUSTOM_ADMIN:
    TEMPLATE_CONTEXT_PROCESSORS.append("upy.contrib.customadmin.template_context.context_processors.customadmin_context")
if USE_UPY_ADMIN:
    TEMPLATE_CONTEXT_PROCESSORS.append("upy.template_context.context_processors.use_upy_admin")

TEMPLATE_CONTEXT_PROCESSORS.extend(
    PROJ_TEMPLATE_CONTEXT_PROCESSORS
)
GLOBAL_TEMPLATES_DIR = '../templates'
TEMPLATE_DIRS = [GLOBAL_TEMPLATES_DIR]
if USE_GLOBAL_TEMPLATES_DIR:
    list_dirs = [ "%s/%s" % (GLOBAL_TEMPLATES_DIR,tdir) for tdir in os.listdir(GLOBAL_TEMPLATES_DIR)]
    if list_dirs:
        TEMPLATE_DIRS.extend(list_dirs)
if USE_UPY_ADMIN:
    TEMPLATE_DIRS.extend(
        [upy_templates(),upy_tpl(),]
    )
TEMPLATE_DIRS.extend(
    PROJ_TEMPLATE_DIRS
)
LOCALE_PATHS = []
LOCALE_PATHS.extend(
        [upy_locale()]
    )
LOCALE_PATHS.extend(PROJ_LOCALE_PATHS)
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'mptt',  
    'imagekit',
    'upy',
    'upy.contrib.ckeditor',
]
if USE_UPY_G11N:
    INSTALLED_APPS.append('upy.contrib.g11n')
    if USE_UPY_TREE:
        INSTALLED_APPS.append('upy.contrib.tree')
    INSTALLED_APPS.append('upy.contrib.language')
    if USE_UPY_TREE and USE_STATIC_PAGE:
        INSTALLED_APPS.append('upy.contrib.staticpage')
if USE_STATIC_ELEMENT:
    INSTALLED_APPS.append('upy.contrib.staticelement')
if USE_UPY_IMAGE:
    INSTALLED_APPS.append('upy.contrib.image')

if USE_FULLHD_SUPPORT:
    PIL_IMAGEFILE_MAXBLOCK = 256 * 2 ** 13 # 2MB
    UPYIMAGE_LIMIT_AREA = 2073700 # 1920*1080px +
else:
    PIL_IMAGEFILE_MAXBLOCK = 256 * 2 ** 10 # 260KB
    UPYIMAGE_LIMIT_AREA = 1049188 # 1366*768px +
            
if USE_UPY_NEWSLETTER:
    INSTALLED_APPS.append('upy.contrib.newsletter')

if USE_UPY_COLOR:
    INSTALLED_APPS.append('upy.contrib.colors')

if USE_CUSTOM_ADMIN:
    INSTALLED_APPS.append('upy.contrib.customadmin')  
    
INSTALLED_APPS.extend(
    PROJECT_APPS
)
    
# file size ---------
FILE_UPLOAD_MAX_MEMORY_SIZE = 32000000 #32 MB

CONTENT_TYPES = ['image', 'video']
# 2 MB  -   2048000
# 2.5MB -   2621440
# 5MB   -   5242880
# 10MB  -  10485760
# 20MB  -  20971520
# 50MB  -  52428800
# 100MB - 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = "2048000"

JQUERY_LIB = "/upy_static/js/lib/jquery-1.7.1.min.js" 
JQUERYUI_LIB = "/upy_static/js/lib/jquery-ui-1.8.17.custom.min.js"

#This variables are necessary for treenode template
UPY_ADMIN_MEDIA = '/upy_static/'
UPY_ADMIN_MEDIA_LOCATION = upy_static()

UPY_TREE_EDITOR_INCLUDE_ANCESTORS = False
UPY_TREE_EDITOR_OBJECT_PERMISSIONS = False

UPYCACHE_DIR = u'%s/upycache/' % (STATIC_ROOT)
UPYCACHE_SIZE_LIMIT = 2 # SIZE LIMIT IN MB

if not os.path.exists(UPYCACHE_DIR):
    os.makedirs(UPYCACHE_DIR) 

"""
CONFIG CKEditor
"""
if not os.path.exists(u'%s/%s/' % (STATIC_ROOT,CKEDITOR_UPLOADS)):
    os.makedirs(u'%s/%s/' % (STATIC_ROOT,CKEDITOR_UPLOADS)) 

CKEDITOR_MEDIA_URL = '/%s' % STATIC_ROOT_NAME
CKEDITOR_MEDIA_PREFIX = '/ckeditor/'
CKEDITOR_UPLOAD_PATH = os.path.join(STATIC_ROOT, 'uploads')