"""
Newsletter contrib needs uwsgi application server to work because it uses the spooler decorator to send mails.
"""
from django.db import models,close_connection
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import hmac
import hashlib
import base64
from django.conf import settings
from upy.utils import datetimeToUnixSec  
from upy.contrib.g11n.models import Publication
from django.db.models.signals import post_save
from datetime import datetime
try:
    from upy.uwsgidecorators import spool, timer
except Exception, e: 
    print "Warning in %s: %s" %(__file__,e)
from upy.contrib.newsletter.mail import send_mail

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


def send_dispatcher_list(disp, recovery = False):
    """
    This function sends newsletter to all contacts in dispatcher's list
    """
    if recovery: lista = disp.contact_list.contacts.filter(email__gt=disp.last_mail_sent.email)
    else: lista = disp.contact_list.contacts.all()
    loop = 0
    for contact in lista:
        loop += 1
        if loop >= len(lista)/10: #ogni 10% dei contatti verifico se ho stoppato
            loop = 0
            if disp.current_status == "stopped": 
                return # se nel frattempo ho stoppato l'esecuzione esco
        contact_list = [contact.email] 
        # il campo email.to vuole una lista, ma noi mandiamo un indirizzo per volta per fare 
        #le email personalizzate e monitorare gli invii
        try:
            send_mail(disp.newsletter.subject,
                      disp.newsletter.body_text,
                      settings.EMAIL_USER,
                      contact_list,
                      disp.newsletter.body_html,
                      disp.newsletter.attachments.all(),
                      disp.contact_list.publication)
            
            disp.last_mail_sent = contact
            disp.save()
        except Exception, e:
            print e
            return
        
def close_dispatcher(disp):
    """
    utility function to set dispatcher and newsletter to sent (if not test list)
    """
    try:
        disp.status = "sent"
        disp.sent_date = datetime.now()
        if not disp.contact_list.test:
            newsl = disp.newsletter
            newsl.sent = True
        disp.save()
        newsl.save()
    except:
        raise

try:
    @spool
    def spooling_dispatcher (args):
        """
        This function enqueue a created dispatcher or a dispatcher with waiting status
        and which has not deleted status
        """
        try:
            close_connection()
        except:
            pass
        try:
            disp = Dispatcher.objects.get(pk=int(args['disp']))
            if disp.status == "deleted": return  
            # ho deciso di annullare l'invio dopo che il dispatcher era gia' stato spoolato. 
            # Return e bbona notte.
            disp.status = "processing"
            disp.save()
            try: 
                send_dispatcher_list(disp)
            except Exception, e:
                print e
                return #tanto lo status resta su processing, al prossimo giro del timer riprova a mandarlo
            else:    
                close_dispatcher(disp)
            
        except Exception, e:
            print e
    
    def run_dispatcher(sender, instance, created, **kwargs):
        """
        When you a dispatcher a new dispatcher, if it's new or its status is 'waiting', then 
        this dispather will be given to spooler that processes it
        """
        if created or instance.status=="waiting":  
            #se il dispatcher e' appena stato creato o ri-settato su waiting accodalo
            if not instance.send_date: instance.send_date = datetime.now()
            timestamp = datetimeToUnixSec(instance.send_date)
            spooling_dispatcher.spool(disp="%s" % instance.pk,at=timestamp)
    
    post_save.connect(run_dispatcher, sender=Dispatcher)
    
    
    @timer(settings.UPY_NEWSLETTER_SPOOLER_TIMEOUT, target='spooler')
    def check_dispatchers(args):
        """
        This function enqueue a processing dispatcher. It checks every UPY_NEWSLETTER_SPOOLER_TIMEOUT seconds.  
        """
        disps = Dispatcher.objects.filter(status='processing')
        for disp in disps:
            try: 
                send_dispatcher_list(disp, recovery=True)
            except Exception,e:
                print e
                return
            else:    
                close_dispatcher(disp)
except Exception, e:
    print "Warning in %s: %s" %(__file__,e)