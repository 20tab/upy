"""
staticpage contrib depends by g11n module. 
If it's in installed app then StaticPage has e G11n model related.
"""
from upy.contrib.g11n.models import G11nBase,G11nModel 
from django.db import models
from upy.contrib.cked.fields import RichTextField
from upy.contrib.tree.models import Page
from django.utils.translation import ugettext_lazy as _


class StaticPage(G11nBase):
    """
    Like a cms, use StaticPage to link a page with a static html content
    """
    page = models.ForeignKey(Page, unique = True, limit_choices_to = {'presentation_type':'StaticPage'},help_text = _(u"Choose a page."), verbose_name = _(u"Page"))
    
    def get_absolute_url(self,upy_context):
        return self.page.get_absolute_url(upy_context)
    
    def __unicode__(self):
        return u"%s" % (self.page)
    class G11nMeta:
        g11n = 'StaticPageG11n'
        fieldname = 'staticpage'
    class Meta:
        abstract = True

class StaticPageG11n(G11nModel):
    """
    It translates related StaticPage instance
    """
    alias = models.CharField(max_length = 50, help_text = _(u"Set the page's alias."), verbose_name = _(u"Alias"))
    html = RichTextField(blank = True, verbose_name = _(u"HTML"))
    
    def __unicode__(self):
        return u"%s (%s)" % (self.alias, self.language)
    
    class Meta:
        abstract = True

class StaticPageCategory(models.Model):
    """
    It's simply a category
    """
    name = models.CharField(max_length = 50, help_text = _(u"Name."), verbose_name = _(u"Name"))
    
    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        abstract = True

