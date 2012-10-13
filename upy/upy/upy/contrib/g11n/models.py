from django.db import models
from django.utils import translation
from django.conf import settings
from upy.utils import clean_cache
from django.utils.translation import ugettext_lazy as _
from upy.contrib.g11n.g11n_threading import get_publication
from django.db.models.base import ModelBase
import os

class G11nBaseCurrentManager(models.Manager):
    """
    It's a special manager for G11nBase model that filter queryset 
    with current language and publication
    """
    def get_query_set(self):
        try:
            g11nmodel = models.get_model(self.model._meta.app_label,self.model.G11nMeta.g11n)
            db_table = g11nmodel._meta.db_table
            select_dict = dict([(field.column,"%s.%s" % (db_table,field.column)) for field in g11nmodel._meta.fields if field.name not in ['id',self.model.G11nMeta.fieldname]])
            filter_dict = {"%s__language__code__iexact" % self.model.G11nMeta.g11n.lower():translation.get_language(), 
                           "%s__publication" % self.model.G11nMeta.g11n.lower(): get_publication()}
            return super(G11nBaseCurrentManager, self).get_query_set().extra(select=select_dict,tables=('%s' % (db_table),)).filter(**filter_dict)
        except:
            raise
            #return super(G11nBaseCurrentManager, self).get_empty_query_set()

class G11nCurrentManager(models.Manager):
    """
    It's the manager for all G11nModel model filtering queryset 
    with current language and publication
    """
    def get_query_set(self):
        try:
            return super(self.__class__, self).get_query_set().filter(publication=get_publication(),language__code__iexact=translation.get_language())
        except:
            return super(self.__class__, self).get_empty_query_set()


class G11nManager(models.Manager):
    """
    This is a default manager for G11n objects that implements the g11n searching
    of content. Curr_pub/curr_lan --> curr_pub/default_lan --> default_pub/default_lan --> Raise DoesNotExist
    obj_filter is a dynamic list of filter to pre-pone to our query
    """
    def g11nsearch(self, language_code = None, publication_url = None, depth = None, **obj_filter):
        dict_depth = {None: 0, "no_default":0, "language_default":1, "publication_default":2,}
        if language_code is None:
            language_code = translation.get_language()
        try:
            language = Language.objects.get(code__iexact=language_code)
            if publication_url is None:
                publication = get_current_publication()
            else:
                publication = Publication.objects.get(url__iexact=publication_url)
        except Language.DoesNotExist:
            raise ValueError("Language does not exists in %s.%s" % (self.__module__,self.__class__.__name__))
        except Publication.DoesNotExist,e:
            raise ValueError("Publication does not exists in %s.%s" % (self.__module__,self.__class__.__name__))
        except Exception, e:
            raise ValueError("Error in %s.%s: %s" % (self.__module__,self.__class__.__name__,e))
        else: # we set successfully current language e publication
            try:
                result = super(self.__class__, self).get_query_set().filter(publication=publication,language=language,**obj_filter)
                if not result and dict_depth[depth] > 0:
                    language = publication.default_language
                    try:
                        result = super(self.__class__, self).get_query_set().filter(publication=publication,language=language,**obj_filter)
                        if not result and dict_depth[depth] > 1:
                            publication = Publication.objects.get(is_default=True)
                            language = publication.default_language
                            try:
                                result = super(self.__class__, self).get_query_set().filter(publication=publication,language=language,**obj_filter)
                            except Exception, e:
                                raise ValueError("Raised in %s. Error in %s.%s: %s" % (os.path.dirname(__file__),self.__module__,self.__class__.__name__,e))
                            else:
                                return result
                        else:
                            return result
                    except Exception, e:
                        raise ValueError("Raised in %s. Error in %s.%s: %s" % (os.path.dirname(__file__),self.__module__,self.__class__.__name__,e))
                    else:
                        return result
                else:
                    return result
            except Exception, e:
                raise ValueError("Raised in %s. Error in %s.%s: %s" % (os.path.dirname(__file__),self.__module__,self.__class__.__name__,e))
            else:
                return result
            
    

class G11nBaseManager(models.Manager):
    """
    This is a default manager for G11n objects that implements the g11n searching
    of content. Curr_pub/curr_lan --> curr_pub/default_lan --> default_pub/default_lan --> Raise DoesNotExist
    obj_filter is a dynamic list of filter to pre-pone to our query
    """
    def g11nsearch(self, language_code = None, publication_url = None, depth = None):
        try:
            g11nmodel = models.get_model(self.model._meta.app_label,self.model.G11nMeta.g11n)
            return super(self.__class__, self).get_query_set().filter(pk__in = [getattr(x,self.model.G11nMeta.fieldname).pk for x in g11nmodel.g11nFilter.g11nsearch(language_code, publication_url, depth)])
            
        except Exception, e:
            raise ValueError("Raised in %s. Error in %s.%s: %s" % (os.path.dirname(__file__),self.__module__,self.__class__.__name__,e))

class G11nOptions(type):
    """
    Options class for G11nModelBase.
    """
    class Schema:
        def __getattr__(self, attr):
            t_model = getattr(self, self.G11nMeta.tradmodel)
            return getattr(self, attr, getattr(t_model, attr))

class G11nModelBase(ModelBase):
    """
    G11n metaclass. This metaclass parses G11nOptions.
    """
    def __new__(cls, name, bases, attrs):
        new = super(G11nModelBase, cls).__new__(cls, name, bases, attrs)
        g11n_opts = attrs.pop('G11nMeta', None)
        setattr(new, '_g11n_meta', G11nOptions(g11n_opts))
        return new

class G11nBase(models.Model):
    """
    This is an abstract class that defines the base object to globalization of content.
    """
    __metaclass__ = G11nModelBase
    g11nFilter = G11nBaseManager()
    g11nobjects = G11nBaseCurrentManager()
    objects = models.Manager()
    
    @property
    def g11n(self):
        """
        It returns the related G11nModel instance with the current language and publication
        """
        try:
            g11nmodel = models.get_model(self.__class__._meta.app_label,self.__class__.G11nMeta.g11n)
            kwargs = {
                      '%s__pk' % self.__class__.G11nMeta.fieldname: self.pk
            }
            return g11nmodel.g11nobjects.get(**kwargs)
        except Exception,e:
            print ValueError("Raised in %s/models.py Error in %s.%s: %s. Function called by %s" % (os.path.dirname(__file__),self.__module__,self.__class__.__name__,e,self.__class__.G11nMeta.g11n))
            return None
    
    def __unicode__(self):
        if self.g11n and hasattr(self.g11n,'__unicode__'):
            return self.g11n.__unicode__()
        else:
            return "%s %s" % (self.__class__.__name__, self.pk)
        
    class G11nMeta:
        """
        This is a class Meta that define which model is the related G11nModel and which field in the related model refers to this G11nBase model
        """
        g11n = None  # Must be a string that define the G11nModel class name that refers to sel as foreign key
        fieldname = None
    class Meta:
        abstract = True
 

class G11nModel(models.Model):
    """
    This is an abstract class that defines the globalization of content.
    """
    publication = models.ForeignKey(u"Publication", help_text = _(u"Set the Publication for Globalization."), verbose_name = _(u"Publication"))
    language = models.ForeignKey(u"Language", help_text = _(u"Set the Language for Globalization."), verbose_name = _(u"Language"))
    objects = models.Manager()
    g11nFilter = G11nManager()
    g11nobjects = G11nCurrentManager()
    class Meta:
        abstract = True

class Publication(G11nBase):
    """
    This is the class that defines the referenced Publication of the website.
    """
    name = models.CharField(max_length = 100, unique = True, help_text = _(u"Identifying name of the website."), 
                            verbose_name = _(u"Name"))
    languages = models.ManyToManyField(u"Language", help_text = _(u"List of languages to be made available on the website."), 
                                       verbose_name = _(u"Languages"))
    url = models.CharField(max_length = 150, unique = True, 
                           help_text = _(u"Identifying url of the website. (In multidomain project it should be 'http://servername', in monodomain project just a slugfield with the unique name of the Publication.)"), 
                           verbose_name = _(u"Url"))  
    enabled = models.BooleanField(default = True, help_text = _(u"Uncheck it to disable the website."), 
                                  verbose_name = _(u"Enabled"))
    is_default = models.CharField(max_length = 50, choices = (("default","Default"),), null = True, blank = True,unique = True, 
                                     help_text = _(u"Select it if it's the default publication for the website."), 
                                     verbose_name = _(u"Is default"))
    default_language = models.ForeignKey(u"Language", null = True, blank = True, related_name = 'default_language', 
                                         help_text = _(u"Default language to use in this publication."), 
                                         verbose_name = _(u"Default language"))
    favicon = models.FileField(null = True, blank = True, upload_to = "favicon", help_text = _(u"Upload the favicon file. (25x25 px / .ico extension)"))
    creation_date = models.DateTimeField(auto_now_add = True, help_text = _(u"Establishment date"), 
                                         verbose_name = _(u"Creation date"))
    last_update = models.DateTimeField(auto_now = True, help_text = _(u"Last update"), 
                                       verbose_name = _(u"Last update"))
    
    
    def save(self, *args, **kwargs):
        clean_cache(settings.UPYCACHE_DIR)
        super(Publication,self).save( *args, **kwargs)
    
    def delete(self):
        if settings.MULTI_DOMAIN and not settings.MULTI_PUBLICATION:
            clean_cache(settings.UPYCACHE_DIR)
        super(Publication,self).delete()
    
    def __unicode__(self):
        return u"%s" % (self.name)
    
    class G11nMeta:
        g11n = "PublicationG11n"
        fieldname = "publication"
    
    class Meta:
        verbose_name = _(u"Publication")
        verbose_name_plural = _(u"Publications")
        ordering = [u'name']

    @staticmethod
    def getCurrent(request):
        """
        It returns current publication. It's not used because current publication is saved in current thread
        """
        if not settings.MULTI_DOMAIN and settings.MULTI_PUBLICATION:
            publication_url = request.get_full_path()
            publication_url = publication_url.split('/')[1]                
        else:
            publication_url = request.get_host()
        try:
            publication = Publication.objects.get(url__iexact=publication_url)
        except Publication.DoesNotExist:
            raise ValueError("Raised in %s. Error in %s.Publication. Publication doesn't exists" % (os.path.dirname(__file__),Publication.__module__))
        except Exception, e:
            raise ValueError("Raised in %s. Error in %s.Publication: %s" % (os.path.dirname(__file__),Publication.__module__,e))
        else:
            return publication
    
    @staticmethod    
    def get_default():
        """
        It returns default publication
        """
        try:
            return Publication.objects.get(is_default="default")
        except: 
            return None  

    
    
        
class PublicationG11n(G11nModel):
    """
    This is the class that defines meta informations of the website.
    """
    title = models.CharField(max_length = 150, help_text = _(u"Set the website's title."),
                             verbose_name = _(u"Title"))
    description = models.CharField(max_length = 250, null = True, blank = True, help_text = _(u"Set the website's description."),
                                   verbose_name = _(u"Description"))
    keywords = models.CharField(max_length = 150, null = True, blank = True, 
                                help_text = _(u"Set the list of website keywords. Don't use more than 10 words approximately."),
                                verbose_name = _(u"Keywords"))
    author = models.CharField(max_length = 150, null = True, blank = True, help_text = _(u"Set the website's author."),
                              verbose_name = _(u"Author"))
    content_type = models.CharField(max_length = 150, null = True, blank = True, help_text = _(u"Set the website's content type."),
                                    verbose_name = _(u"Content type"))
    enabled = models.BooleanField(default = True, help_text = _(u"Uncheck it to enable the website."),
                                  verbose_name = _(u"Enabled"))
    disabled_message = models.TextField(null = True, blank = True, help_text = _(u"Text or html code to use if the website is disabled."),
                                        verbose_name = _(u"Disabled message"))
    robots = models.CharField(max_length = 50, null = True, blank = True, choices = (("index,follow","index,follow"),
                                                           ("noindex,follow","noindex,follow"),
                                                           ("index,nofollow","index,nofollow"),
                                                           ("noindex,nofollow","noindex,nofollow"),
                                                           ),
                                    help_text = _(u"Select the value of meta tag robots if you want set it."),
                                    verbose_name = _(u"Robots"))
    generator = models.CharField(max_length = 250, null = True, blank = True, help_text = _(u"Set the website's generator."),
                                    verbose_name = _(u"Generator"))
    g11n_creation_date = models.DateTimeField(auto_now_add = True, help_text = _(u"Establishment date"), verbose_name = _(u"Creation date"))
    g11n_last_update = models.DateTimeField(auto_now = True, help_text = _(u"Last update"), verbose_name = _(u"Last update"))
    
    def get_fields(self):
        """
        It returns all fields of this model
        """
        return [(field.name, field.value_to_string(self)) for field in PublicationG11n._meta.fields]
    
    def save(self, *args, **kwargs):
        clean_cache(settings.UPYCACHE_DIR,"meta")
        super(PublicationG11n,self).save( *args, **kwargs)
    
    def delete(self):
        clean_cache(settings.UPYCACHE_DIR,"meta")
        super(PublicationG11n,self).delete()
    
    def __unicode__(self):
        return u"%s" % (self.publication.name)
    
    class Meta:
        verbose_name = _(u"Publication's g11n elements")
        verbose_name_plural = _(u"Publications' g11n elements")
        ordering = ['publication']
        
class Language(models.Model):
    """
    This is the class that defines a language
    """
    name = models.CharField(max_length = 50, help_text = _(u"Set the language's name."),
                            verbose_name = _(u"Name"))
    code = models.CharField(max_length = 50, 
                            help_text = _(u"Set the language's code. <a target='_blank' href='http://www.i18nguy.com/unicode/language-identifiers.html'>Open the language identifiers.</a>"),
                            verbose_name = _(u"Code"))
    alias = models.CharField(max_length = 50, help_text = _(u"Set the language's alias."),
                             verbose_name = _(u"Alias"))
    flag = models.FileField(null = True, blank = True, upload_to = "flags", help_text = _(u"Upload the flag file"), verbose_name = _(u'Flag'))
    
    creation_date = models.DateTimeField(auto_now_add = True, help_text = _(u"Establishment date"), verbose_name = _(u"Creation date"))
    last_update = models.DateTimeField(auto_now = True, help_text = _(u"Last update"), verbose_name = _(u"Last update"))
    
    def __unicode__(self):
        return u"%s" % (self.name.title())
    
    class Meta:
        verbose_name = _(u"Language")
        verbose_name_plural = _(u"Languages")
        #ordering = ['name']

    @staticmethod
    def get_default():
        """
        It returns default language for default publication
        """
        
        try:
            return Publication.objects.get(is_default="default").default_language
        except: 
            return None
    
def get_current_publication():
    """
    It returns current publication saved in current thread
    """
    return get_publication()