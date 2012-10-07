"""
staticpage contrib depends by g11n module. 
If it's in installed app then StaticPage has e G11n model related.
"""
from upy.contrib.g11n.models import G11nBase,G11nModel 
from django.db import models
from upy.contrib.ckeditor.fields import RichTextField
from upy.contrib.tree.models import Page
from django.utils.translation import ugettext_lazy as _


class StaticPage(G11nBase):
    """
    Like a cms, use StaticPage to link a page with a static html content
    """
    page = models.ForeignKey(Page, unique = True, limit_choices_to = {'presentation_type':'StaticPage'},help_text = _(u"Choose a page."), verbose_name = _(u"Page"))
    category = models.ForeignKey(u"StaticPageCategory", null=True, blank=True, on_delete = models.SET_NULL, help_text = _(u"Choose a category."), verbose_name = _(u"Category"))
    
    def get_absolute_url(self,upy_context):
        return self.page.get_absolute_url(upy_context)
    
    def __unicode__(self):
        return u"%s" % (self.page)
    class G11nMeta:
        g11n = 'StaticPageG11n'
        fieldname = 'staticpage'
    class Meta:
        verbose_name = _(u"Static Page")
        verbose_name_plural = _(u"Static Pages")
        ordering = ['page']

class StaticPageG11n(G11nModel):
    """
    It translates related StaticPage instance
    """
    alias = models.CharField(max_length = 50, help_text = _(u"Set the page's alias."), verbose_name = _(u"Alias"))
    html = RichTextField(blank = True, verbose_name = _(u"HTML"))
    staticpage = models.ForeignKey(u"StaticPage", help_text = _(u"Choose a Static page to associate."), verbose_name = _(u"Static page"))
    
    def __unicode__(self):
        return u"%s (%s)" % (self.alias, self.language)
    
    class Meta:
        verbose_name = _(u"Static Page G11n Content")
        verbose_name_plural = _(u"Static Page G11n Contents")

class StaticPageCategory(models.Model):
    """
    It's simply a category
    """
    name = models.CharField(max_length = 50, help_text = _(u"Category name."), verbose_name = _(u"Name"))
    
    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        verbose_name = _(u"Category")
        verbose_name_plural = _(u"Categories")
        ordering = ['name']

