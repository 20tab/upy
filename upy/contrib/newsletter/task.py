from django.db import close_connection
from upy.contrib.newsletter.mail import send_mail
from django.conf import settings
from datetime import datetime
from upy.contrib.newsletter.models import Dispatcher
from upy.uwsgidecorators import spool, timer
from upy.utils import datetimeToUnixSec
from django.db.models.signals import post_save

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
            print "Exception in upy.contrib.newsletter.task.send_dispatcher_list: ",e
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
            #print "DISPATCHER: ",disp
            if disp.status == "deleted": return  
            # ho deciso di annullare l'invio dopo che il dispatcher era gia' stato spoolato. 
            # Return e bbona notte.
            disp.status = "processing"
            disp.save()
            try: 
                send_dispatcher_list(disp)
            except Exception, e:
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
                return
            else:    
                close_dispatcher(disp)
except Exception, e:
    print "Warning in %s: %s" %(__file__,e)

