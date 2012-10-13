from upy.contrib.customadmin.models import CustomAdmin, CustomLink
from django.conf import settings

def customadmin_context(request):
    """
    This context processor adds to request context CustomAdmin default instance
    and all CustoLink to customize django's admin
    """
    context_extras = {}
    try:
        context_extras['CUSTOM_ADMIN'] = CustomAdmin.objects.get(is_default = "default")
        context_extras['CUSTOM_LINK_LIST'] = CustomLink.objects.all()
    
    except CustomAdmin.DoesNotExist:
        context_extras['CUSTOM_ADMIN'] = None
    if settings.USE_UPY_ADMIN:
        context_extras['USE_CUSTOM_ADMIN'] = settings.USE_CUSTOM_ADMIN
    else:
        context_extras['USE_CUSTOM_ADMIN'] = False
    return context_extras