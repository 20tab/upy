from django.conf import settings
from project import config
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
if config.USE_UPY_G11N:
    from upy.contrib.g11n.admin import G11nAdmin,G11nTabularInlineAdmin
    from upy.contrib.image.models import UPYImageG11n 
    if config.USE_UPY_IMAGE:
        from upy.contrib.image.models import ImageRepositoryG11n
    
from upy.contrib.image.models import UPYImage, PositionImage
if config.USE_UPY_IMAGE:
        from upy.contrib.image.models import ImageRepository
from django import forms
import Image as PilImage
from django.forms.fields import ImageField


def clean_image(obj,field_name):       
    """
    Function for the Image Form to check the filesize, according to UPYIMAGE settings
    """
    img_temp = obj.cleaned_data[field_name]
    if img_temp:
        im = PilImage.open(img_temp.file)
        width, height = im.size
        if height*width > settings.UPYIMAGE_LIMIT_AREA: # 2073600 = fullHD 1920x1080px
            #raise forms.ValidationError(_("Image size out of range. Actual size: %(width)spx X %(height)spx" % {'width':width, 'height':height}))
            obj._errors[field_name] = obj.error_class([_("Image size out of range. Actual size: %(width)spx X %(height)spx" % {'width':width, 'height':height})])
            
        if settings.RGBA_FILTER:
            mode = im.mode
            if mode not in ("RGB","RGBA"):
                #raise forms.ValidationError(_("Image mode not in RGB or RGBa."))
                obj._errors[field_name] = obj.error_class([_("Image mode not in RGB or RGBa.")])


class UPYImageForm(forms.ModelForm):
    """
    Abstract form to use for UPYImage
    """ 
    def __init__(self,*args, **kwargs):
        super(UPYImageForm, self).__init__(*args, **kwargs)
        self.fields['original_image'].label = self.instance.original_image_label
              
    
    def clean(self):
        """
        It cleans all ImageField in this form
        """
        for name,field in self.fields.items():
            print name, " - ", field.__class__
            if issubclass(field.__class__,ImageField):
                clean_image(self,name)
        return self.cleaned_data
    
class UPYImageOption(admin.ModelAdmin):
    """
    Abstract admin option class for UPYImage
    """
    list_display = ('original_image','admin_thumbnail_view',)
    form = UPYImageForm
    
    class Media:
        css = {"all" : ("/upy_static/css/prettyPhoto.css",)}
        js = (settings.JQUERY_LIB,
              settings.JQUERYUI_LIB,
              '/upy_static/js/lib/jquery.prettyPhoto.js',
              '/upy_static/js/prettyPhoto-init.js')
        
    class Meta:
        abstract = True
    
    
class PositionImageOption(UPYImageOption):
    """
    Abstract admin option class for PositionImage
    """
    list_display = ('position','original_image','admin_thumbnail_view',)
    list_editable = ['position',]
    list_display_links = ['original_image',]
    ordering = ('position',)
    exclude = ('position',)
    
    class Media:
        js = UPYImageOption.Media.js+('/upy_static/js/admin-list-reorder.js',)
    
    class Meta:
        abstract = True
    
    

if config.USE_UPY_G11N:

    class UPYImageG11nInline(G11nTabularInlineAdmin):
        """
        Abstract admin option class for UPYImageG11n inline
        """
        fieldsets = (('', {'fields': 
                           ('title','alt'),
            },),) + G11nAdmin.fieldsets
        model = UPYImageG11n
        class Meta:
            abstract = True

if config.USE_UPY_IMAGE and config.USE_UPY_G11N:
    class ImageRepositoryG11nInline(G11nTabularInlineAdmin):
        """
        Admin option class for ImageRepositoryG11n inline
        """
        fieldsets = (('', {'fields': 
                           ('title','alt','description'),
            },),) + G11nAdmin.fieldsets
        model = ImageRepositoryG11n
    
    class ImageRepositoryG11nOption(G11nAdmin):
        """
        Concrete admin option class for ImageRepositoryG11n
        """
        list_display = ('id','title', 'alt', 'language')
        list_display_links = ['id']
        list_editable = ('title', 'alt', 'language',)
        list_filter = ('language',)
        fieldsets = (('', {'fields': 
                           ('title', 'alt', 'description','image_repository'),
            },),) + G11nAdmin.fieldsets
            
    class ImageRepositoryOption(PositionImageOption):
        """
        Concrete admin option class for ImageRepository
        """
        list_display = ('position','name','date','original_image','admin_thumbnail_view',)
        list_editable = ['position','date',]
        list_display_links = ['name']
        ordering = ('position',)
        save_on_top = True
        search_fields = ('name','date')
        inlines = [ImageRepositoryG11nInline,]
        form = UPYImageForm
    
    
    #admin.site.register(ImageRepositoryG11n, ImageRepositoryG11nOption)    
    admin.site.register(ImageRepository, ImageRepositoryOption)

elif config.USE_UPY_IMAGE:
    class ImageRepositoryOption(PositionImageOption):
        """
        Concrete admin option class for ImageRepository
        """
        list_display = ('position','name','date','title','alt','original_image','admin_thumbnail_view',)
        list_editable = ['position','date','title','alt']
        list_display_links = ['name']
        ordering = ('position',)
        save_on_top = True
        search_fields = ('name','title','alt','date')
        form = UPYImageForm
    
    admin.site.register(ImageRepository, ImageRepositoryOption)