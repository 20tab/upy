from django.conf.urls.defaults import *
from django.conf import settings
from project import config
from django.contrib import admin as contrib_admin
if config.USE_UPY_TREE:
    from upy.contrib.tree.urls import LOGIN_REQUIRED_URLS
contrib_admin.autodiscover()
from django.contrib.admin.sites import site
if settings.USE_UPY_ADMIN and settings.USE_CUSTOM_ADMIN:
    site.index_template = "admin/custom_index.html"
    
from upy.contrib.tree.utility import *

if config.USE_UPY_G11N:
    from upy.contrib.g11n.utility import getLanguageList,getDefaultLanguage
    settings.LANGUAGES = getLanguageList()
    language = getDefaultLanguage()
    if language:
        settings.DEFAULT_LANGUAGES = [(language.code,language.name)]
        settings.LANGUAGE_CODE = language.code

if not settings.HANDLER_404:
    handler404 = 'upy.contrib.tree.views.view_404'
else:
    handler404 = settings.HANDLER_404
if not settings.HANDLER_500:
    handler500 = 'upy.contrib.tree.views.view_500'
else:
    handler500 = settings.HANDLER_500
    
urlpatterns = patterns('',
    (r'^admin/', include(contrib_admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    (r'^accounts/logout/$','django.contrib.auth.views.logout', {'template_name': 'logout.html'}),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'', include('upy.contrib.ckeditor.urls')),
    (r'', include('project.custom_urls')),
)
if config.USE_UPY_TREE:
    urlpatterns += patterns('',
        (r'', include('upy.contrib.tree.urls'))
    )
if config.USE_UPY_IMAGE:
    urlpatterns += patterns('',
        (r'', include('upy.contrib.image.urls')),
    )
if config.USE_CUSTOM_ADMIN:
    urlpatterns += patterns('',
        (r'', include('upy.contrib.customadmin.urls')),
    )