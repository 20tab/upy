from django.conf import settings
from django.contrib import admin
from django import forms

class UPYImageForm(forms.ModelForm):
    """
    Abstract form to use for UPYImage
    """ 
    def __init__(self,*args, **kwargs):
        super(UPYImageForm, self).__init__(*args, **kwargs)
        if hasattr(self.instance.__class__.UPYImageMeta,'label'):
            self.fields['original_image'].label = self.instance.__class__.UPYImageMeta.label
        if hasattr(self.instance.__class__.UPYImageMeta,'required'):
            self.fields['original_image'].required = self.instance.__class__.UPYImageMeta.required
              
class UPYImageAdmin(admin.ModelAdmin):
    """
    Abstract admin option class for UPYImage
    """
    list_display = ('original_image','admin_thumbnail_view',)
    form = UPYImageForm
    
    class Media:
        css = {"all" : ("/upy_static/colorbox/colorbox.css",)}
        js = (settings.JQUERY_LIB,
              settings.JQUERYUI_LIB,
              '/upy_static/colorbox/jquery.colorbox-min.js',
              '/upy_static/js/colorbox-init.js')
        
    class Meta:
        abstract = True
    
    
class PositionImageAdmin(UPYImageAdmin):
    """
    Abstract admin option class for PositionImage
    """
    list_display = ('position','original_image','admin_thumbnail_view',)
    list_editable = ['position',]
    list_display_links = ['original_image',]
    ordering = ('position',)
    exclude = ('position',)
    
    class Media:
        js = UPYImageAdmin.Media.js+('/upy_static/js/admin-list-reorder.js',)
    
    class Meta:
        abstract = True
