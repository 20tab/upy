# Django settings for UPY project.
#import project
import os
from upy.upy_conf import upy_static

PROJECT_PATH = os.path.realpath(os.path.dirname("../"))

ROOT_URLCONF = "project.urls"
SITE_ID = 1
USE_I18N = True
USE_L10N = True
    
STATIC_ROOT_NAME = 'static'
MEDIA_ROOT_NAME = 'media'
STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, STATIC_ROOT_NAME))
RELATIVE_STATIC_ROOT = '../%s/' % STATIC_ROOT_NAME
MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, MEDIA_ROOT_NAME))
STATIC_URL = '/%s/' % STATIC_ROOT_NAME
MEDIA_URL = '/%s/' % MEDIA_ROOT_NAME
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
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
TEMPLATE_CONTEXT_PROCESSORS = [
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
]

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
    'upy.contrib.cked',
    'upy.contrib.inspect',
    'upy.contrib.image',
]

    
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

JQUERY_LIB = "/upy_static/js/lib/jquery-1.9.0.js" 
JQUERYUI_LIB = "/upy_static/js/lib/jquery-ui-1.10.0.custom.min.js"

JQUERYUI_CSSLIB = "/upy_static/css/jqueryui/jquery-ui-1.10.0.custom.css"

ADMIN_THUMBNAIL_DEFAULT_TEMPLATE = "admin/default_thumbnail.html"

#This variables are necessary for treenode template
UPY_ADMIN_MEDIA = '/upy_static/'
UPY_ADMIN_MEDIA_LOCATION = upy_static()

UPY_TREE_EDITOR_INCLUDE_ANCESTORS = False
UPY_TREE_EDITOR_OBJECT_PERMISSIONS = False

"""
CONFIG CKEditor
"""
CKEDITOR_UPLOADS = 'uploads'
if not os.path.exists(u'%s/%s/' % (STATIC_ROOT,CKEDITOR_UPLOADS)):
    os.makedirs(u'%s/%s/' % (STATIC_ROOT,CKEDITOR_UPLOADS))


ELFINDER_OPTIONS = {
    'root': os.path.join(STATIC_ROOT, CKEDITOR_UPLOADS),
    'URL': '/%s/%s/' % (STATIC_ROOT_NAME, CKEDITOR_UPLOADS),
}
