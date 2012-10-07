"""
This views are defined only for examples. They doesn't work.
"""
from django.http import HttpResponse
from upy.contrib.newsletter.utility import UPYNewsletterForm,upy_nl_confirm 
from upy.contrib.tree.views import upy_render
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson
from django.conf import settings

def send_confirm_mail(request):
    """
    It's used to send a confirmation mail
    """
    form = UPYNewsletterForm(True,request.POST)
    status = form.send_confirm_mail(request)
    data = simplejson.dumps({"status":status})
    return HttpResponse(data)


def confirm_subscription(request, secret_key):
    """
    When you want create a view like this, to serve a confirmation link, remeberd that 
    it's need an url decorated with a regex exactly like this following regex: (?P<secret_key>.+)
    """
    rendered = upy_nl_confirm(request,secret_key,message_ok = _(u"Hi %s, your account is succesfully confirmed"), 
                         message_error = _(u"Some problems are occurred during confirmation. Please, contact %s"),
                         use_contact = True, email_host = settings.EMAIL_HOST_USER)
    return HttpResponse(rendered)
    
    
    
    
def newsletter(request,template_name):
    """
    It's used to create a newsletter form to render in a template
    """
    form = UPYNewsletterForm(True)
    return upy_render(request, template_name,{"form":form})
