from django.utils.translation import ugettext_lazy as _
from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from pilkit.processors import SmartResize, Adjust
from django.conf import settings
from upy.contrib.g11n.models import G11nModel

class UPYImage(models.Model):
    """
    This abstract class only provide original_image and admin_thumbnail field, with the 
    admin_thumbnail_view function. Inherit this class in you models.py and import imagekit ImageSpec
    to create other thumbnail or display field with any processor you need.
    """
    original_image = ProcessedImageField(null = True, blank = True, upload_to='upyimage')#, processors=[_choose_preprocessor(),])
    admin_thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            SmartResize(25, 25)], source='original_image', options={'quality': 90})  #format='JPEG', 

    def admin_thumbnail_view(self):
        """
        It's a property used in admin interface. It decorates list_display items with a thumbnail 
        and with prettyPhoto jQuery plugin to open images in a lightbox.
        """
        if self.original_image:
            return u'<a href="%s" class="upy_colorbox" title="%s"><img src="%s" class="upy_admin_thumb" alt="%s"/></a>' % (self.original_image.url, _("view image"), self.admin_thumbnail.url, self.admin_thumbnail.url )
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
            
            
if settings.USE_UPY_G11N:
        
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