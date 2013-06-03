"""
Newsletter contrib needs uwsgi application server to work because it uses the spooler decorator to send mails.
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import hmac, hashlib,base64
from django.conf import settings
from upy.contrib.g11n.models import Publication
from datetime import datetime

class UPYNL(models.Model):
    """
    It's an abstrat model used by all newsletter's model.
    It has only two fields that saves establishment datetime and last update datetime for each instance
    """
    creation_date = models.DateTimeField(auto_now_add = True, help_text = _(u"Establishment date"), 
                                        verbose_name = _(u"Creation date"))
    last_update = models.DateTimeField(auto_now = True, help_text = _(u"Last update"), 
                                        verbose_name = _(u"Last update"))
    class Meta:
        abstract = True

class Contact(UPYNL):
    """
    This represents a contact for lists of this newsletter
    """
    email = models.EmailField(help_text = _(u"Insert your e-mail."), verbose_name = _(u"E-mail"), unique = True)
    name = models.CharField(null = True, blank = True, max_length = 150, help_text = _(u"Insert you name"),
                            verbose_name = _(u"Name"))
    surname = models.CharField(null = True, blank = True, max_length = 150,
                                help_text = _(u"Insert you surname"), verbose_name = _(u"Surname"))
    secret_key = models.TextField(help_text = _(u"Set secret key"), verbose_name = _(u"Secret key"))
    confirmed = models.BooleanField(default = False, 
                                    help_text = _(u"Check if this contact is confirmed"), 
                                    verbose_name = _(u"Confirmed"))
    subscribed = models.BooleanField(default = True,
                                    help_text = _(u"Check if this contact is subscribed"), 
                                    verbose_name = _(u"Subscribed"))
        
    def __unicode__(self):
        if self.name and self.surname:
            return u"\"%s %s\" <%s> " % (self.surname, self.name, self.email)
        return u"%s" % (self.email)
    
    def save(self, *args, **kwargs):
        if not self.confirmed:
            tohash = "%s%s" % (self.email,datetime.now())
            dig = hmac.new(b'%s' % settings.UPY_SECRET_KEY, msg=tohash, digestmod=hashlib.sha256).digest()
            self.secret_key = base64.b64encode(dig).decode().replace("/","_")
        super(Contact,self).save( *args, **kwargs)
    
    class Meta:
        verbose_name = _(u"Contact")
        verbose_name_plural = _(u"Contacts")
        ordering = [u'email',u'surname',u'name']


class List(UPYNL):
    """
    A list groupes some contacts
    """
    name = models.CharField(max_length = 150, help_text = _(u"Insert list's name"), verbose_name = _(u"Name"))
    description = models.TextField(null = True, blank = True, help_text = _(u"Set list's description"), 
                                    verbose_name = _(u"Description"))
    priority = models.CharField(max_length = 150, help_text = _(u"Set list's priority"), 
                                    verbose_name = _(u"Priority"), choices = ([("%s"% n,n) for n in range(1,11)]))
    contacts = models.ManyToManyField(u"Contact", help_text = _(u"A list of contacts to associate"), 
                                    verbose_name = _(u"Contacts"))
    publication =models.ForeignKey(Publication,  help_text = _(u"Set the Publication for this list"), 
                                    verbose_name = _(u"Publication"))
    test = models.BooleanField(default = False, help_text = _(u"Check if this list is a test list"),
                                verbose_name = _(u"Test"))
       
    def __unicode__(self):
        return u"%s" % (self.name)
    
    class Meta:
        verbose_name = _(u"List")
        verbose_name_plural = _(u"Lists")
        ordering = [u'name']

class Attachment(UPYNL):
    """
    It represents a file to attach in a newsletter
    """
    name = models.CharField(max_length = 150, unique = True, help_text = _(u"Attachment's name"), 
                            verbose_name = _(u"Name"))
    attached_file = models.FileField(null = True, blank = True, upload_to = u"newsletter/attachments", 
                                        help_text = _(u"Upload the attachment's file."), verbose_name = _(u"File"))
    
    def __unicode__(self):
        return u"%s" % (self.name)
    
    class Meta:
        ordering = ['name']
        verbose_name = _(u"Attachment")
        verbose_name_plural = _(u"Attachments")
    
class Newsletter(UPYNL):
    """
    Here you can write your mail to send to some lists
    """
    subject = models.CharField(max_length = 250, help_text = _(u"Insert subject"), verbose_name = _(u"Subject"))
    body_text = models.TextField(help_text = _(u"Set body in text format"), verbose_name = _(u"Body text"))
    body_html = models.TextField(help_text = _(u"Set body in html format. If you want add an image in html content, you must replace url in src attribute with the cid content. Example src='cid:name_of_an_attachment_image'"), verbose_name = _(u"Body html"))
    attachments = models.ManyToManyField( u"Attachment", null = True, blank = True,
                                    help_text = _(u"A list of Attachments to associate"), 
                                    verbose_name = _(u"Attachments"))
    sent = models.BooleanField(default = False, 
                                help_text = _(u"Check if this newsletter is sent"),
                                verbose_name = _(u"Sent"))
    
    def __unicode__(self):
        return u"%s" % (self.subject)
    
    
    def save(self, *args, **kwargs):
        try:
            publication = Publication.get_default()
            self.body_html = self.body_html.replace('"%s/uploads' % settings.CKEDITOR_MEDIA_URL,'"http://%s%s/uploads' % (publication.url,settings.CKEDITOR_MEDIA_URL))
        except Exception, e:
            print "\n\n",e
        super(Newsletter,self).save( *args, **kwargs)
    
    class Meta:
        verbose_name = _(u"Newsletter")
        verbose_name_plural = _(u"Newsletters")
        ordering = [u'subject']
        
class Dispatcher(UPYNL):
    """
    It's processed by spooler to send mails
    """
    contact_list = models.ForeignKey(u"List", help_text = _(u"Set a list of distribution"), verbose_name = _(u"List"))
    newsletter = models.OneToOneField(u"Newsletter", help_text = _(u"Set a newsletter"), verbose_name = _(u"Newsletter"), limit_choices_to = {'sent': False})
    last_mail_sent = models.ForeignKey(u"Contact", null = True, blank = True, help_text = _(u"Set the last mail sent"), verbose_name = _(u"Last mail sent"))
    status = models.CharField(max_length = 250, help_text = _(u"Set status"), verbose_name = _(u"Status"), default = u'waiting', choices = [(u'waiting',_(u'waiting')),
                                                                                                                                           (u'processing',_(u'processing')),
                                                                                                                                           (u'sent',_(u'sent')),
                                                                                                                                           (u'deleted',_(u'deleted')),
                                                                                                                                           (u'stopped',_(u'stopped')),
                                                                                                                                           ])
    send_date = models.DateTimeField(null = True, blank = True, help_text = _(u"Choose when to send the newsletter. Empty field means now"), verbose_name = _(u"Send date"))
    sent_date = models.DateTimeField(null = True, blank = True, help_text = _(u"Process complete date"), verbose_name = _(u"Sent date"))
    user_create = models.ForeignKey(User, null = True, blank = True, help_text = _(u"Set who create this dispatcher"), verbose_name = _(u"User create"))
    
    @property
    def priority(self):
        return self.contact_list.priority
    
    @property
    def current_status(self):
        disp = Dispatcher.objects.get(pk=self.pk)
        return disp.status
    
    def __unicode__(self):
        return u"%s - %s" % (self.newsletter, self.contact_list)
    
    class Meta:
        verbose_name = _(u"Dispatcher")
        verbose_name_plural = _(u"Dispatchers")
        ordering = [u'contact_list__priority',u'status']

