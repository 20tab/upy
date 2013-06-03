from django.contrib import admin
from upy.contrib.gmaps.widgets import GoogleMapsAddressWidget
from upy.contrib.gmaps.fields import AddressField
from django.conf import settings


class GmapsAdmin(admin.ModelAdmin):
    list_display = ('geoaddress','continent','country','city','address','zip_code')
    list_filter = ('continent',)
    search_fields = ('geoaddress','continent','country','city','address','zip_code')
    fieldsets = (
        (None, {'fields': (('continent','country'),('area','city',),
                           ('address','zip_code'),('geoaddress',),('geolocation',))}),
    )
    formfield_overrides = {
        AddressField: {'widget': GoogleMapsAddressWidget},    
    }
    class Media:
        js = (settings.JQUERY_LIB,
              '/upy_static/gmaps/js/geopopulate.js',
             )