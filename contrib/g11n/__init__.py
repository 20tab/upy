from django.conf import settings
if 'upy.contrib.g11n' in settings.INSTALLED_APPS:
    try:
        from upy.contrib.g11n.management.commands import g11n_validate
        c = g11n_validate.Command()
        c.execute()
    except:
        raise