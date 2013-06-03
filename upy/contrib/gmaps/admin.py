from django.contrib import admin
from upy.contrib.gmaps.widgets import GoogleMapsAddressWidget
from upy.contrib.gmaps.fields import AddressField
from django.conf import settings


class GmapsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        AddressField: {'widget': GoogleMapsAddressWidget},    
    }
    class Media:
        js = (settings.JQUERY_LIB,
              '/upy_static/gmaps/js/geopopulate.js',
             )