from django.template.loader import render_to_string
from email.MIMEImage import MIMEImage
import mimetypes
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import loader, Context
from django.template import RequestContext
from django.utils.html import strip_tags


def umail(request, template, subject, sender, to, context={}, bcc=[], attachments=[]):
    """
    It sends mail with template. It supports html and txt template. In the first case it searches a txt template
    with the same name in the same position. If it will be found it sends both.
    'template', 'subject' and 'sender' are strings.
    'to' and 'bcc' are lists of addresses.
    'context' is a dictionary.
    'attachments' is a list of paths.
    """
    if request:
        c = RequestContext(request, context)
    else:
        c = Context(context)

    if template.endswith('.html'):
        t = loader.get_template(template)
        try:
            t_html = t
            txt_name = '%s.txt' % (template.rsplit('.', 1)[0])
            t = loader.get_template(txt_name)
        except:
            print "Missing .txt template for: %s" % (template)
            email = EmailMessage(subject, t_html.render(c), sender, to, bcc)
            email.content_subtype = "html"
        else:
            email = EmailMultiAlternatives(subject, strip_tags(t.render(c)), sender, to, bcc)
            email.attach_alternative(t_html.render(c).encode('utf-8'), "text/html")
    else:
        t = loader.get_template(template)
        email = EmailMessage(subject, strip_tags(t.render(c)), sender, to, bcc)

        for filepath in attachments:
            mimetype = mimetypes.guess_type(filepath)[0]
            email.attach_file(filepath, mimetype)
    email.send()


def send_mail(subject, text_content, from_email, to, html_content=None, attachments=None, publication=""):
    """
    This function sends mail using EmailMultiAlternatives and attachs all attachments
    passed as parameters
    """
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    if html_content:
        msg.attach_alternative(html_content, "text/html")
    if attachments:
        for att in attachments:
            if att.attached_file:
                mimetype = mimetypes.guess_type(att.attached_file.url)[0]
                if str(mimetype) in ('image/jpeg', 'image/pjpeg', 'image/png', 'image/gif'):
                    try:
                        with open(att.attached_file.path) as f:
                            email_embed_image(msg, att.name, f.read())
                    except Exception, e:
                        print e
                else:
                    msg.attach_file("%s" % (att.attached_file.url[1:]))
    msg.send()


def send_rendered_mail(subject, text_content, template_name, context_dict, from_email, to, attachments=None):
    """
    It sends mail after rendering html content
    """
    rendered = render_to_string(template_name, context_dict)
    return send_mail(subject, text_content, from_email, to, rendered, attachments)


def email_embed_image(email, img_content_id, img_data):
    """
    email is a django.core.mail.EmailMessage object
    """
    img = MIMEImage(img_data)
    img.add_header('Content-ID', '<%s>' % img_content_id)
    img.add_header('Content-Disposition', 'inline')
    email.attach(img)
