from django.forms import ModelForm
from django.template.loader import render_to_string
from upy.contrib.newsletter.mail import send_rendered_mail
from django.utils.translation import ugettext_lazy as _
from upy.contrib.newsletter.models import Contact, List, settings, now
from upy.contrib.g11n.models import get_current_publication

def upy_nl_confirm(request,secret_key, 
                         message_ok = _(u"Hi %s, your account is succesfully confirmed"), 
                         message_error = _(u"Some problems are occurred during confirmation. Please, contact %s"),
                         use_contact = True, email_host = settings.EMAIL_USER):
    """
    This view is used to confirm a registered Contact to a newsletter
    """
    try:
        contact = Contact.objects.get(secret_key = secret_key)
        contact.confirmed = True
        contact.save()
        if use_contact:
            message = message_ok.replace("%s","%s" % contact)
        else:
            message = message_ok.replace("%s","")
    except:
        contact = None
        message = message_error.replace("%s",email_host)
    
    return message

class UPYNewsletterForm(ModelForm):
    """
    It's represents a form with all fields if only_mail is True
    else it shows only email field
    """
    def __init__(self,only_email,*args, **kwargs):
        super(UPYNewsletterForm, self).__init__(*args, **kwargs)
        if only_email:
            exclude_list = ('name','surname','secret_key','confirmed','subscribed')
        else:
            exclude_list = ('secret_key','confirmed','subscribed')
        for field in exclude_list:
            del self.fields[field]
       
    class Meta:
        model = Contact
     
    def send_confirm_mail(self,request):
        """
        It sends a mail to a contact with confirmation link
        """
        current_publication = get_current_publication()
        try:
            contact = Contact.objects.get(email = request.POST.get("email"))
        except:
            contact = None
        if not contact:
            if self.is_valid():
                try:
                    contact = self.save()
                except:
                    return {"status": False, "error":"contact_save"}
                try:
                    nwl_list = List.objects.get(name = "List %s" % current_publication)
                except:
                    nwl_list = List(name = "List %s" % current_publication, 
                                                      description = "List created on %s" % now(),
                                                      priority = 1,
                                                      publication = current_publication)
                try:
                    nwl_list.save()
                    nwl_list.contacts.add(contact)
                    nwl_list.save()
                except:
                    result = {"status": False, "error":"list_save"}
                user = "%s" % contact
                
                confirm_url = "http://%s/confirm_subscription/%s" % (current_publication.url,contact.secret_key)
                message = render_to_string("send_confirmation.txt.html",{"user": user,
                                                                         "confirm_url":confirm_url,
                                                                         "website": "http://%s" % current_publication.url})
                send_rendered_mail(_(u"Confirm subscription"), message,
                                          "send_confirmation.html", {"user": user,
                                                                     "confirm_url":confirm_url,
                                                                     "website": "http://%s" % current_publication.url}, 
                                          settings.EMAIL_USER,[contact.email])
                result = {"status": True, "error":""}
                return result
            return {"status": False, "error":"form_not_valid"}
        else:
            return {"status": False, "error":"contact_exists"}
        
        
