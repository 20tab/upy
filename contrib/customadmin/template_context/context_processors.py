from upy.contrib.customadmin.models import CustomAdmin, CustomLink
from django.conf import settings

def customadmin_context(request):
    context_extras = {}
    try:
        context_extras['CUSTOM_ADMIN'] = CustomAdmin.objects.get(is_default = "default")
        context_extras['CUSTOM_LINK_LIST'] = CustomLink.objects.all()
    
    except CustomAdmin.DoesNotExist:
        context_extras['CUSTOM_ADMIN'] = None
    context_extras['USE_CUSTOM_ADMIN'] = settings.USE_CUSTOM_ADMIN
    return context_extras