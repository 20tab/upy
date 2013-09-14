from django.db import models
from django.utils.translation import ugettext_lazy as _
from upy.contrib.gmaps import fields as map_fields
from upy.fields import ContinentCountryField, CONTINENTS
from django.db.models.base import ModelBase


class GmapsBase(ModelBase):
    """
    GmapsModel metaclass.
    """
    def __new__(cls, name, bases, attrs):
        gmaps_opt = attrs.pop('GmapsMeta', None)
        attrs['GmapsMeta'] = gmaps_opt
        return super(GmapsBase, cls).__new__(cls, name, bases, attrs)


class GmapsModel(models.Model):
    continent = models.CharField(_(u'Continent'), max_length=100, blank=True, choices=CONTINENTS)
    country = ContinentCountryField(_(u"Country"), blank=True, max_length=250)
    area = models.CharField(_(u"Area"), blank=True, max_length=250)
    city = models.CharField(_(u'City'), blank=True, max_length=250)
    address = models.CharField(_(u"Address"), blank=True, max_length=250)
    zip_code = models.CharField(_(u"Zip code"), blank=True, max_length=50)
    geoaddress = map_fields.AddressField(_(u"Geo Address"), blank=True, max_length=250)
    geolocation = map_fields.GeoLocationField(_(u"Geo Location"), blank=True, max_length=250)
      
    def __unicode__(self):
        return u"%s" % self.geoaddress
    
    class GmapsMeta:
        default_country = u'IT'
        default_continent=u'europe'
        
    class Meta:
        abstract = True