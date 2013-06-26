from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils import simplejson
from django.core.exceptions import ImproperlyConfigured
from django.forms.util import flatatt
from upy.contrib.ckeditor.config import CONFIGURATIONS
json_encode = simplejson.JSONEncoder().encode


class CKEditorWidget(forms.Textarea):
    """
    Widget providing CKEditor for Rich Text Editing.
    Supports direct image uploads and embed.
    """
    class Media:
        try:
            js = (
                settings.JQUERY_LIB,
                settings.CKEDITOR_MEDIA_PREFIX + 'ckeditor/ckeditor.js',
                settings.CKEDITOR_MEDIA_PREFIX + 'ckeditor/jquery-ckeditor.js',
            )
        except AttributeError:
            raise ImproperlyConfigured("django-ckeditor requires CKEDITOR_MEDIA_PREFIX setting. This setting specifies a URL prefix to the ckeditor JS and CSS media (not uploaded media). Make sure to use a trailing slash: CKEDITOR_MEDIA_PREFIX = '/media/ckeditor/'")

    def __init__(self, config_name='COMPLETE_CONFIG',config = None, *args, **kwargs):
        super(CKEditorWidget, self).__init__(*args, **kwargs)
        if not config:
            if config_name in CONFIGURATIONS.keys():
                self.config = CONFIGURATIONS[config_name]
            else:
                self.config = CONFIGURATIONS['COMPLETE_CONFIG']
        else:
            self.config = config
        if not self.config.has_key('skin'):
            self.config['skin'] = CONFIGURATIONS['COMPLETE_CONFIG']['skin']
        if not self.config.has_key('toolbar'):
            self.config['toolbar'] = CONFIGURATIONS['COMPLETE_CONFIG']['toolbar']
      
    def render(self, name, value, attrs={}):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        self.config['filebrowserUploadUrl'] = reverse('ckeditor_upload')
        self.config['filebrowserBrowseUrl'] = reverse('ckeditor_browse')
        return mark_safe(u'''<textarea%s data-processed="0" data-config='%s' data-id="%s" data-type="ckeditortype">%s</textarea>
                        ''' % (flatatt(final_attrs), json_encode(self.config), 
                        final_attrs['id'],conditional_escape(force_unicode(value)), 
                        ))