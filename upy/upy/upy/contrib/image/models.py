from django.utils.translation import ugettext_lazy as _
from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit, SmartResize, Adjust
from upy.utils import today
from django.conf import settings
from project import config
from upy.contrib.g11n.models import G11nModel

def _choose_preprocessor():
    """
    Function to define the preprocessor on original_image field. It crops the original image, so user
    cannot save on server too big images. (in order to prevent disk space wasting)
    """
    if settings.USE_FULLHD_SUPPORT:
        return ResizeToFit(width=1920, height=1366) #upscale=False)
    else:
        return ResizeToFit(width=800, height=800) #upscale=False)

    
class UPYImage(models.Model):
    """
    This abstract class only provide original_image and admin_thumbnail field, with the 
    admin_thumbnail_view function. Inherit this class in you models.py and import imagekit ImageSpec
    to create other thumbnail or display field with any processor you need.
    """
    original_image = ProcessedImageField(null = True, blank = True, upload_to='upyimage', processors=[_choose_preprocessor(),])
    admin_thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            SmartResize(25, 25)], image_field='original_image', options={'quality': 90})  #format='JPEG', 

    def admin_thumbnail_view(self):
        """
        It's a property used in admin interface. It decorates list_display items with a thumbnail 
        and with prettyPhoto jQuery plugin to open images in a lightbox.
        """
        if self.original_image:
            return u'<a href="%s" data-rel="prettyPhoto" title="%s"><img src="%s" class="upy_admin_thumb" alt="%s"/></a>' % (self.original_image.url, _("view image"), self.admin_thumbnail.url, self.admin_thumbnail.url )
        else:
            return None
    admin_thumbnail_view.short_description = _(u'Thumbnail')
    admin_thumbnail_view.allow_tags = True
    
    original_image_label = _(u"Original image")
    
    def __unicode__(self):
        return u"%s" % (self.original_image)

    class Meta:
        abstract = True
                
class PositionImage(UPYImage):
    """
    Class for Images with position. It adds position field and manages position
    on admin interface.
    """
    position = models.PositiveSmallIntegerField(u'Position', default=0)

    class Meta: 
        ordering = [u'position',]
        abstract = True   
            
            
if config.USE_UPY_G11N:
        
    class UPYImageG11n(G11nModel):
        """
        Abstract class for G11nModel to inherit if you need localized contents for your UPYImage model
        """
        title = models.CharField(max_length = 150, help_text = _(u"Set the image title."))
        alt = models.CharField(max_length = 150, help_text = _(u"Set the image alternative field."))
        
        def __unicode__(self):
            return u"%s" % (self.language)
        
        class Meta:
            abstract = True

if config.USE_UPY_IMAGE:            
    class ImageRepositoryBase(PositionImage):
        """
        Concrete class for Images. It add useful fields like position, name, date... and manage position
        on the admin.
        """
        name = models.CharField(max_length=100)
        display_image = ImageSpecField([ResizeToFit(800,600)], image_field='original_image', options={'quality': 90})  #format='JPEG',
        date = models.DateField(default = today(), help_text = _(u"Set the date you want to display for this image.")) 
        creation_date = models.DateTimeField(auto_now_add = True, help_text = _(u"Establishment date"), 
                                             verbose_name = _(u"Creation date"))
        def admin_thumbnail_view(self):
            """
            It's a property used in admin interface. It decorates list_display items with a thumbnail 
            and with prettyPhoto jQuery plugin to open images in a lightbox.
            """
            if self.original_image:
                return u'<a href="%s" data-rel="prettyPhoto" title="%s"><img src="%s" alt="%s"/></a>' % (self.display_image.url, _("view image"), self.admin_thumbnail.url, self.admin_thumbnail.url )
            else:
                return None
        admin_thumbnail_view.short_description = _(u'Thumbnail Display')
        admin_thumbnail_view.allow_tags = True
        
        def get_name(self):
            return self.name
        
        def __unicode__(self):
            return u"%s" % (self.name)
            
        class Meta:
            verbose_name = _(u"Image")
            verbose_name_plural = _(u"Images")
            ordering = [u'position',]
            abstract = True
    
        
    if config.USE_UPY_G11N:
        
                
        class ImageRepositoryG11n(UPYImageG11n):
            """
            It defines image's repository g11n model if G11n is used in this project
            """
            description = models.TextField(null = True, blank = True, help_text = _(u"Image description."))
            image_repository = models.ForeignKey(u"ImageRepository", help_text = _(u"Choose an Image Repository element to associate."), verbose_name = _(u"Image Repository element"))
    
        class ImageRepository(ImageRepositoryBase):
            """
            It defines image's repository model if G11n is used in this project
            """
            class G11nMeta:
                g11n = 'ImageRepositoryG11n'
                fieldname = 'image_repository'
    
    else:
        
        class ImageRepository(ImageRepositoryBase):
            """
            It defines image's repository model if G11n is not used in this project
            """
            title = models.CharField(max_length = 150, help_text = _(u"Set the image title."))
            alt = models.CharField(max_length = 150, help_text = _(u"Set the image alternative field."))
            description = models.TextField(null = True, blank = True, help_text = _(u"Image description."))