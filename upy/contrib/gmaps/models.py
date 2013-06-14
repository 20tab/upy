from django.db import models
from django.utils.translation import ugettext_lazy as _
from upy.contrib.gmaps import fields as map_fields
from upy.fields import ContinentCountryField,CONTINENTS
from django.db.models.base import ModelBase

class GmapsOptions(type):
    """
    Options class for UPYImageBase.
    """
    class Schema:
        def __getattr__(self, attr):
            t_model = getattr(self, self.GmapsMeta.tradmodel)
            return getattr(self, attr, getattr(t_model, attr))

class GmapsBase(ModelBase):
    """
    UPYImage metaclass. This metaclass parses UPYImageOptions.
    """
    def __new__(cls, name, bases, attrs):
        new = super(GmapsBase, cls).__new__(cls, name, bases, attrs)
        g11n_opts = attrs.pop('GmapsMeta', None)
        setattr(new, '_gmaps_meta', GmapsOptions(g11n_opts))
        return new

class GmapsModel(models.Model):
    continent = models.CharField(_(u'Continent'),max_length=100,choices=(CONTINENTS))
    country = ContinentCountryField(_(u"Country"), max_length = 250)
    area = models.CharField(_(u"Area"), null=True, blank=True, max_length = 250)
    city = models.CharField(_(u'City'), max_length = 250)
    address = models.CharField(_(u"Address"), max_length = 250)
    zip_code  = models.CharField(_(u"Zip code"), max_length = 50)
    geoaddress = map_fields.AddressField(_(u"Geo Address"), max_length=250)
    geolocation = map_fields.GeoLocationField(_(u"Geo Location"), max_length=250)
      
    def __unicode__(self):
        return u"%s" % self.geoaddress
    
    class GmapsMeta:
        default_country = u'IT'
        
    class Meta:
        abstract = True