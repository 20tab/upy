from upy.contrib.customadmin.models import CustomAdmin
from django.template import RequestContext

from django.shortcuts import render_to_response

def custom_admin_layout(request):
    """
    It renders customadmin.css that defines rules to customize admin's interface
    """
    try:
        custom = CustomAdmin.objects.select_related().get(default =True)
    except:
        custom = None
    return render_to_response("customadmin.css.html", 
                              {"custom":custom}, 
                              context_instance=RequestContext(request),
                              mimetype="text/css; charset=utf-8")
    
    