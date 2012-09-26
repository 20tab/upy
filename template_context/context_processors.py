"""
Contains some common upy project context_processors
"""
from django.conf import settings

def use_upy_admin(request):
    """
    Adds settings.USE_UPY_ADMIN and settings.JQUERY_LIB to context dictionary
    """
    context_extras = {}
    context_extras['USE_UPY_ADMIN'] = settings.USE_UPY_ADMIN
    context_extras['JQUERY_LIB'] = settings.JQUERY_LIB
    context_extras['USE_UPY_JQUERY_LIB'] = settings.USE_UPY_JQUERY_LIB
    return context_extras