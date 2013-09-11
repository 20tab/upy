from django.conf.urls import *
from django.conf import settings
from project import config
from django.contrib import admin as contrib_admin
contrib_admin.autodiscover()
from django.contrib.admin.sites import site
if settings.USE_UPY_ADMIN and settings.USE_CUSTOM_ADMIN:
    site.index_template = "admin/custom_index.html"

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
    (r'^cked/', include('upy.contrib.cked.urls')),
    (r'', include('upy.contrib.inspect.urls')),
    (r'', include('project.custom_urls')),
)
if config.USE_UPY_TREE:
    urlpatterns += patterns('',
        (r'', include('upy.contrib.tree.urls'))
    )
if config.USE_CUSTOM_ADMIN:
    urlpatterns += patterns('',
        (r'', include('upy.contrib.customadmin.urls')),
    )
if config.USE_UPY_ROSETTA:
    urlpatterns += patterns('',
        (r'', include('upy.contrib.rosetta.urls')),
    )