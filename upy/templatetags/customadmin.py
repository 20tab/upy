from django.conf import settings

if 'upy.contrib.customadmin' in settings.INSTALLED_APPS:
    from upy.contrib.customadmin.templatetags.customadmin import *