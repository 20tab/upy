"""
It defines the urlpattern for css file with rules for admin's interface customization.
"""
from django.conf.urls.defaults import *
urlpatterns = patterns('',
        (r'^upy_custom_admin_layout.css$','upy.contrib.customadmin.views.custom_admin_layout'),
)
