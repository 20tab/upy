from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^admin/inspect/browse/$', 'upy.contrib.inspect.views.browse', name='inspect_browse'),
)
