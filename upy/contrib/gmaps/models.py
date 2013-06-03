from django.db import models
from django.utils.translation import ugettext_lazy as _
from upy.contrib.gmaps import fields as map_fields
from upy.fields import CountryField

class GmapsModel(models.Model):
    continent = models.CharField(_(u'Continent'),max_length=100,choices=((u'europe',_(u'Europe')),
                                                                        (u'north-america',_(u'North America')),
                                                                        (u'south-america',_(u'South America')),
                                                                        (u'africa',_(u'Africa')),
                                                                        (u'asia',_(u'Asia')),
                                                                        (u'oceania',_(u'Oceania'))))
    country = CountryField(_(u"Country"), default = u'FR', max_length = 250)
    area = models.CharField(_(u"Area"), null=True, blank=True, max_length = 250)
    city = models.CharField(_(u'City'), max_length = 250)
    address = models.CharField(_(u"Address"), max_length = 250)
    zip_code  = models.CharField(_(u"Zip code"), max_length = 50)
    geoaddress = map_fields.AddressField(_(u"Geo Address"), max_length=250)
    geolocation = map_fields.GeoLocationField(_(u"Geo Location"), max_length=250)
      
    def __unicode__(self):
        return u"%s" % self.geoaddress
    
    class Meta:
        abstract = True