from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils import simplejson

from django.core.exceptions import ImproperlyConfigured
from django.forms.util import flatatt

json_encode = simplejson.JSONEncoder().encode

DEFAULT_CONFIG = {
    'skin': 'office2003',
    'toolbar': 'Full',
    'height': 300,
    'width': 800,
    #'contentsCss':'/static/example_layout.css'
}

class CKEditorWidget(forms.Textarea):
    """
    Widget providing CKEditor for Rich Text Editing.
    Supports direct image uploads and embed.
    """
    class Media:
        try:
            js = (
                settings.CKEDITOR_MEDIA_PREFIX + 'ckeditor/ckeditor.js',
            )
        except AttributeError:
            raise ImproperlyConfigured("django-ckeditor requires CKEDITOR_MEDIA_PREFIX setting. This setting specifies a URL prefix to the ckeditor JS and CSS media (not uploaded media). Make sure to use a trailing slash: CKEDITOR_MEDIA_PREFIX = '/media/ckeditor/'")

    def __init__(self, config_name='default',config = None, *args, **kwargs):
        super(CKEditorWidget, self).__init__(*args, **kwargs)
        # Setup config from defaults.
        if not config:
            self.config = DEFAULT_CONFIG
        else:
            self.config = config
        if not self.config.has_key('skin'):
            self.config['skin'] = DEFAULT_CONFIG['skin']
        if not self.config.has_key('toolbar'):
            self.config['toolbar'] = DEFAULT_CONFIG['toolbar']
            
    def render(self, name, value, attrs={}):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        self.config['filebrowserUploadUrl'] = reverse('ckeditor_upload')
        self.config['filebrowserBrowseUrl'] = reverse('ckeditor_browse')
        return mark_safe(u'''<textarea%s>%s</textarea>
        <script type="text/javascript">
            CKEDITOR.replace("%s", %s);
        </script>''' % (flatatt(final_attrs), conditional_escape(force_unicode(value)), final_attrs['id'], json_encode(self.config)))
