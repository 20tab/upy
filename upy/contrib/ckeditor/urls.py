from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    '',
    url(r'^upload/', 'upy.contrib.ckeditor.views.upload', name='ckeditor_upload'),
    url(r'^browse/', 'upy.contrib.ckeditor.views.browse', name='ckeditor_browse'),
)
