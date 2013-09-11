from django.conf.urls import *
from django.conf import settings
from upy.contrib.tree.utility import getUrlList


urlpatterns = patterns('',
        (r'^favicon.ico$', 'upy.contrib.tree.views.favicon'),
        (r'^sitemap.xml$', 'upy.contrib.tree.views.sitemap'),
        (r'^robots.txt$', 'upy.contrib.tree.views.robots'),
)
upy_urls, tree_urls = getUrlList()

for app_url in upy_urls:
    urlpatterns += patterns('', app_url)
TREE_URLS = tree_urls