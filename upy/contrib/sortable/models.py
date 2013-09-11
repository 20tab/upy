from django.db import models
from upy.models import UpyModel
from django.utils.translation import ugettext_lazy as _

class PositionModel(UpyModel):
    position = models.PositiveIntegerField(_(u'Position'),default = 0)
    
    def __unicode__(self):
        return u"%s %s" % (self.__class__.__name__, self.position)
    
    @property
    def max_pos(self):
        max_number_instance = self.__class__.objects.aggregate(models.Max('position'))['position__max']
        if max_number_instance:
            return max_number_instance + 1
        else:
            return 0

    class Meta:
        abstract = True