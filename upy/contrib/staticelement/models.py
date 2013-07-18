"""
staticelement contrib depends by g11n module. 
If it's in installed app then StaticElement has e G11n model related.
"""
from django.db import models
from upy.contrib.cked.fields import RichTextField
from upy.contrib.tree.models import _
from upy.contrib.g11n.models import G11nBase,G11nModel 
    
class StaticElementG11nBase(G11nBase):
    """
    It's a model that allows you to write some static element to use in your template
    """
    name = models.CharField(max_length = 50, help_text = _(u"Set the element's name."), verbose_name = _(u"Name"))
    category = models.ForeignKey(u"StaticElementCategory", null=True, blank=True, on_delete = models.SET_NULL, help_text = _(u"Choose a category."), verbose_name = _(u"Category"))
    
    def __unicode__(self):
        return u"%s" % (self.name)
    
    class G11nMeta:
        g11n = 'StaticElementG11n'
        fieldname = 'staticelement'
    class Meta:
        abstract=True

class StaticElementG11n(G11nModel):
    """
    It's translate related StaticElement's instance
    """
    alias = models.CharField(max_length = 50, help_text = _(u"Set the element's alias."), verbose_name = _(u"Alias"))
    html = RichTextField(blank = True, verbose_name = _(u"HTML"))
    
    def __unicode__(self):
        return u"%s (%s)" % (self.alias, self.language)
    
    class Meta:
        abstract = True


class StaticElement(models.Model):
    """
    If g11n it isn't in installed app then StaticElement is a model that
    contains also fields for textual contents
    """
    name = models.CharField(max_length = 50, help_text = _(u"Set the element's name."), verbose_name = _(u"Name"))
    alias = models.CharField(max_length = 50, help_text = _(u"Set the element's alias."), verbose_name = _(u"Alias"))
    html = RichTextField(blank = True, verbose_name = _(u"HTML"))
    
    def __unicode__(self):
        return u"%s" % (self.name)
    
    class Meta:
        abstract = True

class StaticElementCategory(models.Model):
    """
    It's simply e category
    """
    name = models.CharField(max_length = 50, help_text = _(u"Category name."), verbose_name = _(u"Name"))
    
    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        abstract = True

