from django.conf.urls.defaults import *
from django.conf import settings
from upy.contrib.tree.utility import getUrlList



urlpatterns = patterns('',
        # UPY URLS CONFIGURATION
        (r'^favicon.ico$', 'upy.contrib.tree.views.favicon'),
        (r'^sitemap.xml$', 'upy.contrib.tree.views.sitemap'),
        (r'^robots.txt$', 'upy.contrib.tree.views.robots'),
        (r'^upy_get_languages$','upy.contrib.tree.views.get_languages'),  
)
upy_urls, urls_login_required, tree_urls = getUrlList()

for app_url in upy_urls:
    urlpatterns += patterns('', app_url)
if settings.USE_UPY_ROUTING:
    urlpatterns += patterns('',
        (r'^.*$', 'upy.contrib.tree.views.render_page'),
    )

LOGIN_REQUIRED_URLS = urls_login_required
TREE_URLS = tree_urls