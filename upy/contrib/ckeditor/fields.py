"""
It contains RichTextField. It's a TextField with CKEditor widget in his form 
"""
from django.db import models
from django import forms

from upy.contrib.ckeditor.widgets import CKEditorWidget

class RichTextField(models.TextField):
    """
    Field that construct the textarea field with CKEditor widget.
    """
    def __init__(self,*args, **kwargs):
        self.config_name = kwargs.pop("config_name", "COMPLETE_CONFIG")
        super(RichTextField, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        defaults = {
            'form_class': RichTextFormField,
            'config_name': self.config_name,
        }
        defaults.update(kwargs)
        return super(RichTextField, self).formfield(**defaults)
        
class RichTextFormField(forms.fields.Field):
    """
    FormField for RichTextField
    """
    def __init__(self, config_name='COMPLETE_CONFIG', *args, **kwargs):
        kwargs.update({'widget': CKEditorWidget(config_name=config_name)})
        super(RichTextFormField, self).__init__(*args, **kwargs)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^upy\.contrib\.ckeditor\.fields\.RichTextField"])
except ImportError:
    pass