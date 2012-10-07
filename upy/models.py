from django.db import models
from django.utils.translation import ugettext_lazy as _

class UpyModel(models.Model):
    creation_date = models.DateTimeField(_(u"Creation date"), auto_now_add = True, help_text = _(u"Establishment date."))
    last_update_date = models.DateTimeField(_(u"Last Update date"), auto_now = True, help_text = _(u"Last update date."))
    class Meta:
        abstract = True