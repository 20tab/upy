ONUWSGI = False
try:
    import uwsgi
    ONUWSGI = True
except: 
    pass
from django.conf import settings
if 'upy.contrib.g11n' in settings.INSTALLED_APPS and not ONUWSGI:
    from upy.contrib.g11n.management.commands import g11n_validate
    c = g11n_validate.Command()
    c.execute()