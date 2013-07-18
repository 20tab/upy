from django.conf.urls import url, patterns


urlpatterns =\
    patterns('upy.contrib.cked.views',
             url(r'^elfinder/$', 'elfinder', name='cked_elfinder'),
             url(r'^elfinder/connector/$', 'elfinder_connector',
                 name='cked_elfinder_connector'),)
