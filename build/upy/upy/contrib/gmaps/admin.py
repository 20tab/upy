from django.contrib import admin
from upy.contrib.gmaps.widgets import GoogleMapsAddressWidget
from upy.contrib.gmaps.fields import AddressField
from django.conf import settings
from django import forms
from upy.widgets import CountrySelect

class GmapsForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(GmapsForm, self).__init__(*args, **kwargs)
        if hasattr(self.instance.__class__.GmapsMeta,'default_country'):
            self.fields['country'].initial = self.instance.__class__.GmapsMeta.default_country
            self.fields['country'].widget = CountrySelect(choices=self.fields['country'].choices)
        if hasattr(self.instance.__class__.GmapsMeta,'default_continent'):
            self.fields['continent'].initial = self.instance.__class__.GmapsMeta.default_continent
            
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
    form = GmapsForm
    class Media:
        js = (settings.JQUERY_LIB,
              '/upy_static/gmaps/js/geopopulate.js',
              '/upy_static/gmaps/js/gmaps.js',
              
             )