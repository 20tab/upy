from django.utils.translation import ugettext_lazy as _
from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import SmartResize, Adjust
from django.db.models.base import ModelBase


class UPYImageBase(ModelBase):
    """
    UPYImage metaclass. This metaclass parses UPYImageOptions.
    """
    def __new__(cls, name, bases, attrs):
        class UPYImageMeta:
            label = _(u"Original image")
            required = False

        attrs['UPYImageMeta'] = UPYImageMeta
        return super(UPYImageBase, cls).__new__(cls, name, bases, attrs)


class UPYImage(models.Model):
    """
    This abstract class only provide original_image and admin_thumbnail field, with the 
    admin_thumbnail_view function. Inherit this class in you models.py and import imagekit ImageSpec
    to create other thumbnail or display field with any processor you need.
    """
    original_image = models.ImageField(null=True, blank=True, upload_to='upyimage')
    admin_thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
                                      SmartResize(25, 25)], source='original_image', options={'quality': 90})

    def admin_thumbnail_view(self):
        """
        It's a property used in admin interface. It decorates list_display items with a thumbnail 
        and with prettyPhoto jQuery plugin to open images in a lightbox.
        """
        if self.original_image:
            try:
                return u'''<a href="{0}" class="upy_colorbox" title="{1}">
                              <img src="{2}" class="upy_admin_thumb" alt="{3}"/>
                           </a>'''.format(
                    self.original_image.url,
                    _("view image"),
                    self.admin_thumbnail.url,
                    self.admin_thumbnail.url
                )
            except:
                return _(u'Missing file')
        else:
            return None

    admin_thumbnail_view.short_description = _(u'Thumbnail')
    admin_thumbnail_view.allow_tags = True

    class UPYImageMeta:
        label = _(u"Original image")
        required = False

    def __unicode__(self):
        return u"{0}".format(self.original_image)

    class Meta:
        abstract = True


class PositionImage(UPYImage):
    """
    Class for Images with position. It adds position field and manages position
    on admin interface.
    """
    position = models.PositiveSmallIntegerField(u'Position', default=0)

    class Meta:
        ordering = [u'position', ]
        abstract = True
