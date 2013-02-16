"""
Contains some common upy project context_processors
"""
from django.conf import settings
import upy

def use_upy_admin(request):
    """
    Adds settings.USE_UPY_ADMIN and settings.JQUERY_LIB to context dictionary
    """
    context_extras = {}
    context_extras['USE_UPY_ADMIN'] = settings.USE_UPY_ADMIN
    context_extras['JQUERY_LIB'] = settings.JQUERY_LIB
    context_extras['USE_UPY_JQUERY_LIB'] = settings.USE_UPY_JQUERY_LIB
    context_extras['JQUERYUI_LIB'] = settings.JQUERYUI_LIB
    context_extras['USE_UPY_JQUERYUI_LIB'] = settings.USE_UPY_JQUERY_LIB
    context_extras['JQUERYUI_CSSLIB'] = settings.JQUERYUI_CSSLIB
    context_extras['USE_UPY_CSS_RESET'] = settings.USE_UPY_CSS_RESET
    context_extras['USE_UPY_ROSETTA'] = settings.USE_UPY_ROSETTA
    context_extras['UPY_VERSION'] = upy.__version__
    return context_extras