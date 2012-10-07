from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.MIMEImage import MIMEImage
import mimetypes

def send_mail(subject, text_content, from_email, to, html_content = None, attachments = None, publication = ""):
    """
    This function sends mail using EmailMultiAlternatives and attachs all attachments
    passed as parameters
    """
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    if html_content:
        msg.attach_alternative(html_content, "text/html")
    if attachments:
        for att in attachments:            
            mimetype, encoding = mimetypes.guess_type(att.file.url)
            if str(mimetype) in ('image/jpeg', 'image/pjpeg', 'image/png', 'image/gif'):
                try:
                    with open(att.file.path) as f:
                        email_embed_image(msg, att.name, f.read())
                except Exception, e:
                    print e
            else:
                msg.attach_file("%s" % (att.file.url[1:]))
    try:
        msg.send()
    except Exception, e:
        print e
        
    
def send_rendered_mail(subject, text_content, template_name, context_dict, from_email,to, attachments = None):
    """
    It sends mail after rendering html content
    """
    try:
        rendered = render_to_string(template_name,context_dict)
    except Exception, e:
        print e
    return send_mail(subject, text_content, from_email, to, rendered, attachments)


def email_embed_image(email, img_content_id, img_data):
    """
    email is a django.core.mail.EmailMessage object
    """
    img = MIMEImage(img_data)
    img.add_header('Content-ID', '<%s>' % img_content_id)
    img.add_header('Content-Disposition', 'inline')
    email.attach(img)
    