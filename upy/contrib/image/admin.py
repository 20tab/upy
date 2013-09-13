from django.conf import settings
from django.contrib import admin
from imagekit.admin import AdminThumbnail as IKAdminThumbnail
from upy.contrib.sortable.admin import PositionAdmin


class AdminThumbnail(IKAdminThumbnail):
    """
    A convenience utility for adding thumbnails to Django's admin change list.
    """
    def __init__(self, image_field, template=None):
        """
        :param image_field: The name of the ImageField or ImageSpecField on the
            model to use for the thumbnail.
        :param template: The template with which to render the thumbnail

        """
        self.image_field = image_field
        self.template = template or getattr(settings,
                                            "ADMIN_THUMBNAIL_DEFAULT_TEMPLATE",
                                            "imagekit/admin/thumbnail.html")


class ColorBoxAdmin(admin.ModelAdmin):
    """
    Abstract admin option class to add colorbox.js (jQuery plugin)
    """
    class Media:
        css = {"all": ("/upy_static/colorbox/colorbox.css",)}
        js = (settings.JQUERY_LIB,
              settings.JQUERYUI_LIB,
              '/upy_static/colorbox/jquery.colorbox-min.js',
              '/upy_static/js/colorbox-init.js')

    class Meta:
        abstract = True


class ColorBoxPositionAdmin(admin.ModelAdmin):
    """
    Abstract admin option class to add colorbox.js (jQuery plugin)
    """
    class Media:
        css = {"all": ("/upy_static/colorbox/colorbox.css",)}
        js = (settings.JQUERY_LIB,
              settings.JQUERYUI_LIB,
              '/upy_static/js/admin-list-reorder.js',
              '/upy_static/colorbox/jquery.colorbox-min.js',
              '/upy_static/js/colorbox-init.js')

    class Meta:
        abstract = True
