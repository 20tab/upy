from django.conf.urls import url, patterns

urlpatterns = patterns('upy.contrib.rosetta.views',
    url(r'^admin/rosetta$', 'home', name='rosetta-home'),
    url(r'^admin/rosetta/pick/$', 'list_languages', name='rosetta-pick-file'),
    url(r'^admin/rosetta/download/$', 'download_file', name='rosetta-download-file'),
    url(r'^admin/rosetta/select/(?P<langid>[\w\-]+)/(?P<idx>\d+)/$', 'lang_sel', name='rosetta-language-selection'),
)
