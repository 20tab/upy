from django.db import models
from upy.contrib.tree.models import Node, Page
from django.utils.translation import ugettext_lazy as _
from upy.models import UpyModel
from upy.fields import NullTrueField


class TransSite(UpyModel):
    """
    This is the class that defines meta informations of the website.
    """
    default = NullTrueField(unique=True, verbose_name=_(u"Default"))
    title = models.CharField(max_length=150, help_text=_(u"Set the website's title."),
                             verbose_name=_(u"Title"))
    description = models.CharField(max_length=250, null=True, blank=True,
                                   help_text=_(u"Set the website's description."),
                                   verbose_name=_(u"Description"))
    keywords = models.CharField(max_length=150, null=True, blank=True,
                                help_text=_(
                                    u"Set the list of website keywords. Don't use more than 10 words approximately."),
                                verbose_name=_(u"Keywords"))
    author = models.CharField(max_length=150, null=True, blank=True, help_text=_(u"Set the website's author."),
                              verbose_name=_(u"Author"))
    content_type = models.CharField(max_length=150, default=u"utf-8", null=True, blank=True,
                                    help_text=_(u"Set the website's charset."),
                                    verbose_name=_(u"Charset"))
    robots = models.CharField(max_length=50, null=True, blank=True, choices=(("index,follow", "index,follow"),
                                                                             ("noindex,follow", "noindex,follow"),
                                                                             ("index,nofollow", "index,nofollow"),
                                                                             ("noindex,nofollow", "noindex,nofollow"),
    ),
                              help_text=_(u"Select the value of meta tag robots if you want set it."),
                              verbose_name=_(u"Robots"))
    generator = models.CharField(max_length=250, null=True, blank=True, help_text=_(u"Set the website's generator."),
                                 verbose_name=_(u"Generator"))

    def get_fields(self):
        """
        It returns all fields of this model
        """
        return [(field.name, field.value_to_string(self)) for field in TransSite._meta.fields]

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u"Site's translation")
        verbose_name_plural = _(u"Site's translations")


class TransNode(UpyModel):
    """
    This is the class that defines static contents of a page of the structure.
    """
    alias = models.CharField(max_length=150, help_text=_(u"Set the node's display name."),
                             verbose_name=_(u"Alias"))
    title = models.CharField(max_length=150, null=True, blank=True, help_text=_(u"Set the node's title (in <a> tag)."),
                             verbose_name=_(u"Title"))
    node = models.OneToOneField(Node, help_text=_(u"Set the node to associate with the Node's Meta Content."),
                                verbose_name=_(u"Node"))

    def __unicode__(self):
        return u"%s - %s" % (self.alias, self.node.name)

    class Meta:
        verbose_name = _(u"Node's translation")
        verbose_name_plural = _(u"Node's translations")
        ordering = ['node']


class TransPage(UpyModel):
    """
    This is the class that defines static contents of a page of the structure.
    """
    title = models.CharField(max_length=150, null=True, blank=True, help_text=_(u"Set the page's title."),
                             verbose_name=_(u"Title"))
    description = models.CharField(max_length=250, null=True, blank=True,
                                   help_text=_(u"Set the website's description."),
                                   verbose_name=_(u"Description"))
    keywords = models.CharField(max_length=150, null=True, blank=True,
                                help_text=_(
                                    u"Set the list of page's keywords. Don't use more than 10 words approximately."),
                                verbose_name=_(u"Keywords"))
    author = models.CharField(max_length=150, null=True, blank=True, help_text=_(u"Set the page's author."),
                              verbose_name=_(u"Author"))
    content_type = models.CharField(max_length=150, null=True, blank=True, help_text=_(u"Set the page's content type."),
                                    verbose_name=_(u"Content type"))
    robots = models.CharField(max_length=50, null=True, blank=True, choices=(("index,follow", "index,follow"),
                                                                             ("noindex,follow", "noindex,follow"),
                                                                             ("index,nofollow", "index,nofollow"),
                                                                             ("noindex,nofollow", "noindex,nofollow"),
    ),
                              help_text=_(u"Select the value of meta tag robots if you want set it."),
                              verbose_name=_(u"Robots"))
    page = models.OneToOneField(Page, help_text=_(u"Set the page to associate with the Page's Meta Content."),
                                verbose_name=_(u"Page"))

    def get_fields(self):
        """
        It returns all fields as key, value in a dictionary
        """
        return [(field.name, field.value_to_string(self)) for field in TransPage._meta.fields]

    def __unicode__(self):
        return u"{0}".format(self.page.name)

    class Meta:
        verbose_name = _(u"Page's translation")
        verbose_name_plural = _(u"Page's translations")
        ordering = ['page']
