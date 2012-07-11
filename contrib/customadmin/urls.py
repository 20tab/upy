from django.conf.urls.defaults import *
urlpatterns = patterns('',
        (r'^upy_custom_admin_layout.css$','upy.contrib.customadmin.views.custom_admin_layout'),
)
