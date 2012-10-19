from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel
from django.conf import settings
from upy.utils import clean_cache
from django.conf.urls.defaults import url
from django.contrib.auth.models import Group
from ast import literal_eval
import os,sys,traceback
from upy.contrib.g11n.models import G11nBase,G11nModel,Publication
from upy.multiple_meta import classmaker

def formatExceptionInfo(maxTBlevel=5):
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)

class PublicationExtended(models.Model):
    """
    It's extends g11n.model.Publication model adding references to nodes and tree's structure.
    """
    tree_structure = models.ForeignKey(u"TreeStructure", help_text = _(u"Structure to use in the website."), 
                                       verbose_name = _(u"Tree structure"))
    index_node = models.ForeignKey(u"Node", null = True, blank = True, 
                                   help_text = _(u"Default node/page to display if path/slug is Blank."),limit_choices_to = {'page__view__isnull': False})
    publication = models.OneToOneField(Publication)
    
    @property
    def root(self):
        """
        It returns the root of this publication
        """
        return self.tree_structure.tree_root

    
    def __unicode__(self):
        return u"%s - %s" % (self.publication, self.tree_structure)
    
    class Meta:
        verbose_name = _(u"Publication")
        verbose_name_plural = _(u"Publications")
        ordering = [u'publication']

class TreeStructure(models.Model):
    """
    This is the class that defines the structure of the website.
    """
    name = models.CharField(max_length = 50, unique = True, help_text = _(u"Identifying structure's name."),
                            verbose_name = _(u"Name"))
    description = models.TextField(null = True, blank = True, help_text = _(u"Structure's description."),
                                   verbose_name = _(u"Description"))
    tree_root = models.ForeignKey(u"Node", help_text = _(u"Set the root node for the referenced tree."), 
                                  limit_choices_to = {'parent': None},
                                  verbose_name = _(u"Tree root"))
    css = models.ManyToManyField(u"Css", null = True, blank = True, help_text = _(u"TreeStructure's css"), verbose_name = _(u"Css"), through = u"CssTreeStructurePosition")
    
    js = models.ManyToManyField(u"Js", null = True, blank = True, help_text = _(u"TreeStructure's js"), verbose_name = _(u"Js"), through = u"JsTreeStructurePosition")
    
    creation_date = models.DateTimeField(auto_now_add = True, help_text = _(u"Establishment date"), 
                                         verbose_name = _(u"Creation date"))
    last_update = models.DateTimeField(auto_now = True, help_text = _(u"Last update"), 
                                       verbose_name = _(u"Last update"))
    
    def save(self, *args, **kwargs):
        clean_cache(settings.UPYCACHE_DIR,"meta")
        super(TreeStructure,self).save( *args, **kwargs)
    
    def delete(self):
        clean_cache(settings.UPYCACHE_DIR,"meta")
        super(TreeStructure,self).delete()
        
    def __unicode__(self):
        return u"%s" % (self.name)
        
    class Meta:
        verbose_name = _(u"Structure")
        verbose_name_plural = _(u"Structures")
        ordering = ['name']

class Node(G11nBase,MPTTModel):
    """
    This is the class that defines tree's nodes.
    """
    name = models.CharField(max_length = 50, help_text = _(u"Identifying name of the associated page."),
                            verbose_name = _(u"Name"))
    page = models.ForeignKey(u"Page", null = True, blank = True, help_text = _(u"Set the page for the referenced node."),
                             verbose_name = _(u"Page"))
    parent = models.ForeignKey('self', null = True, blank = True, related_name = 'children', 
                               help_text = _(u"Set the parent node for this node if it isn't root."),
                               verbose_name = _(u"Parent"))
    position = models.PositiveSmallIntegerField(u'Position', default=0)
    hide_in_navigation = models.BooleanField(help_text = _(u"Check it to hide the page in this node in the navigation."),
                                             verbose_name = _(u"Hide in navigation"))
    hide_in_url = models.BooleanField(help_text = _(u"Check it to hide the node in url path (only if node hasn't a page)."),
                                             verbose_name = _(u"Hide in url"))
    protected = models.BooleanField(help_text = _(u"Check it if the page related to this node should be protected from unauthorized access."),
                                    verbose_name = _(u"Protected"))
    
    show_if_logged = models.BooleanField(help_text = _(u"Check it if this node must be showed only for logged user or group."),
                                    verbose_name = _(u"Show if logged"))
    groups = models.ManyToManyField(Group, null = True, blank = True, help_text = _(u"List of groups to use with 'show if logged' parameter."), 
                                       verbose_name = _(u"Groups"),related_name = 'node_groups')
    
    value_regex = models.CharField(max_length = 50, null = True, blank = True, 
                                   help_text = _(u"Set the value to respect the regex of the associated page."),
                                   verbose_name = _(u"Value regex"))
    changefreq = models.CharField(max_length = 50, null = True, blank = True, choices = (("always","always"),
                                                                                         ("hourly","hourly"),
                                                                                         ("daily","daily"),
                                                                                         ("weekly","weekly"),
                                                                                         ("monthly","monthly"),
                                                                                         ("yearly","yearly"),
                                                                                         ("never","never")), 
                                    help_text = _(u"The chengefreq attribute for sitemap.xml"),
                                    verbose_name = _(u"Changefreq"))
    priority = models.CharField(max_length = 50, choices = (("0.1","0.1"),
                                                           ("0.2","0.2"),
                                                           ("0.3","0.3"),
                                                           ("0.4","0.4"),
                                                           ("0.5","0.5"),
                                                           ("0.6","0.6"),
                                                           ("0.7","0.7"),
                                                           ("0.8","0.8"),
                                                           ("0.9","0.9"),
                                                           ("1.0","1.0"),
                                                           ), default = "0.5", 
                                    help_text = _(u"The priority attribute for sitemap.xml"),
                                    verbose_name = _(u"Priority"))
    robots = models.ManyToManyField(u"Robot", null = True, blank = True, help_text = _(u"List of robots to communicate that this node is disallowed."), 
                                       verbose_name = _(u"Robots"))
    disallow = models.BooleanField(help_text = _(u"Check it to disallow the page in this node in the file robots.txt."),
                                             verbose_name = _(u"Disallow"))
    
    creation_date = models.DateTimeField(auto_now_add = True, help_text = _(u"Establishment date"), verbose_name = _(u"Creation date"))
    last_update = models.DateTimeField(auto_now = True, help_text = _(u"Last update"), verbose_name = _(u"Last update"))
    
    def save(self, *args, **kwargs):
        clean_cache(settings.UPYCACHE_DIR,"menu")
        clean_cache(settings.UPYCACHE_DIR,"breadcrumb")
        super(Node,self).save( *args, **kwargs)
    
    def delete(self):
        clean_cache(settings.UPYCACHE_DIR,"menu")
        clean_cache(settings.UPYCACHE_DIR,"breadcrumb")
        super(Node,self).delete()
    
    @property
    def page_name(self):
        """
        It returns page's name of this node
        """
        try:
            return self.page.name
        except:
            return None
    
    @property
    def view_path(self):
        """
        It returns page's view_path
        """
        if self.page:
            return "%s" % self.page.view_path
        return ""
    
    @property
    def slug(self):
        """
        It returns node's slug
        """
        if self.page:
            return self.page.slug
        elif not self.hide_in_url:
            return self.name
        else:
            return ""

    @property
    def complete_slug(self):
        """
        It returns complete slug for this node
        """
        compl_slug = self.treeslug
        if self.page:
            compl_slug += "%s" % self.page.slug
        return compl_slug
    
    @property
    def treeslug(self):
        """
        It returns tree's slug including all ancestors
        """
        ancestors = self.get_ancestors()
        tree_slug = ""
        for node in ancestors[1:]:
            if not node.hide_in_url:
                tree_slug += "%s/" % node.slug
            else:
                tree_slug += "%s" % node.slug
        return tree_slug
    
    @property
    def basenode(self):
        """
        It returns self's base node
        """
        ancestors = self.get_ancestors()
        if ancestors:
            return ancestors[0]
        return self
    
    def absolute_url(self,pub_extended,node):
        """
        It calculates absolute url and it returns link as string and the relative url pattern
        """
        if self.page:
            page = self.page
            view = page.view
            if not settings.MULTI_DOMAIN and settings.MULTI_PUBLICATION:
                regex = r'^%s/%s%s/%s$' % (pub_extended.publication.url, self.treeslug, page.slug, page.regex)
                link = r'/%s/%s%s/%s' % (pub_extended.publication.url, self.treeslug, page.slug, page.regex)
            else:
                regex = r'^%s%s/%s$' % (self.treeslug, page.slug, page.regex)
                link = r'/%s%s/%s' % (self.treeslug, page.slug, page.regex)
            view = u'%s.%s.%s' % (view.app_name,view.module_name,view.func_name)
            self.page.check_static_vars(pub_extended,node)
            return link, url(regex, view, page.static_vars, page.scheme_name)
        
        return False
    
    def get_absolute_url(self,upy_context = None):
        """
        It returns simply a link as string
        """
        if upy_context:
            link, x =  self.absolute_url(upy_context['PUB_EXTENDED'], upy_context['NODE'])
        else:
            link = "%s" % self.pk
        return link
    
    @property
    def presentation_type(self):
        """
        It returns page's presentation_type
        """
        if self.page and self.page.presentation_type:
            return self.page.presentation_type
        return ""
        
    def __unicode__(self):
        if self.page_name is None:
            page_name = "-"
        else:
            page_name = self.page_name
        return u"%s (%s)" % (self.name, page_name)
    
    __metaclass__ = classmaker()
    
    class G11nMeta:
        g11n = 'NodeG11n'
        fieldname = 'node'
    
    class Meta:
        verbose_name = _(u"Node")
        verbose_name_plural = _(u"Nodes")
        ordering = ['tree_id', 'lft']
    
    @staticmethod
    def getCurrent(publication, page):
        """
        DEPRECATED: It returns the current node, calculating it. But the current node is in the upy_context dictionary
        """
        tree_structure_root = publication.tree_structure.tree_root
        nodes = tree_structure_root.get_descendants()
        for node in nodes:
            if page == node.page:
                return node

        raise ValueError("Node don't found in utility.getCurrentNode")
    
    @staticmethod
    def rebuild():
        """
        DEPRECATED: It rebuilds mptt structure in database
        """
        def rebuild_tree(node, tree_id, lft=0, level=1):
            rght = lft + 1
            print "%s%s (%s)" % ("    " * (level - 1), node.name, unicode(node.parent))
            for child in node.children.all().order_by("position"):
                rght = rebuild_tree(child, tree_id, rght, level + 1)
            node.lft, node.rght = lft, rght
            node.tree_id = tree_id
            node.level = level
            node.save()
            return rght + 1
        tree_id = 0
        for root_node in Node.tree.root_nodes().order_by("position"):
            rebuild_tree(root_node, tree_id)
            tree_id += 1

class NodeG11n(G11nModel):
    """
    This is the class that defines static contents of a page of the structure.
    """
    alias = models.CharField(max_length = 150, help_text = _(u"Set the node's display name."),
                             verbose_name = _(u"Alias"))
    title = models.CharField(max_length = 150, null = True, blank = True, help_text = _(u"Set the node's title (in <a> tag)."),
                             verbose_name = _(u"Title"))
    node = models.ForeignKey(u"Node", help_text = _(u"Set the node to associate with the Node's Meta Content."),
                             verbose_name = _(u"Node"))
    g11n_creation_date = models.DateTimeField(auto_now_add = True, help_text = _(u"Establishment date"), verbose_name = _(u"Creation date"))
    g11n_last_update = models.DateTimeField(auto_now = True, help_text = _(u"Last update"), verbose_name = _(u"Last update"))
    
    def save(self, *args, **kwargs):
        clean_cache(settings.UPYCACHE_DIR,"menu")
        clean_cache(settings.UPYCACHE_DIR,"breadcrumb")
        super(NodeG11n,self).save( *args, **kwargs)
    
    def delete(self):
        clean_cache(settings.UPYCACHE_DIR,"menu")
        clean_cache(settings.UPYCACHE_DIR,"breadcrumb")
        super(NodeG11n,self).delete()
    
    def __unicode__(self):
        return u"%s - %s" % (self.alias, self.node.name)
    
    class Meta:
        verbose_name = _(u"Node's G11n Content")
        verbose_name_plural = _(u"Node's G11n Contents")
        ordering = ['node']

                
class Page(G11nBase):
    """
    This is the class that defines a page of the structure.
    """
    name = models.CharField(max_length = 50, unique = True, help_text = _(u"Identifying page's name."),
                            verbose_name = _(u"Name"))
    slug = models.SlugField(max_length = 50, help_text = _(u"Identifying page's url."),
                            verbose_name = _(u"Slug"))
    regex = models.CharField(max_length = 150, null = True, blank = True, help_text = _(u"Set the regular expression that completes the url (e.g. \"(?P<element_id>\d+)\")."),
                             verbose_name = _(u"Regex"))
    static_vars = models.TextField(null = True, blank = True, 
                                   help_text = _(u"Set the dictionary of static parameters of the page in a regular format: {\"param1\":value1, \"param2\":value2}."),
                                   verbose_name = _(u"Static vars"))
    scheme_name = models.CharField(max_length = 100, null = True, blank = True, 
                                   help_text = _(u"Set the unique name to associate the view of a callback url."),
                                   verbose_name = _(u"Scheme name"))
    template = models.ForeignKey(u"Template", help_text = _(u"Set the template to associate with the page."),
                                 verbose_name = _(u"Template"))
    view = models.ForeignKey(u"View", help_text = _(u"Set the view to associate with the page."),
                             verbose_name = _(u"View"))
    presentation_type = models.CharField(max_length = 150, null = True, blank = True, choices = (("StaticPage","StaticPage"),("Custom","Custom"),),
                                    help_text = _(u"Select the presentation type."),
                                    verbose_name = _(u"Presentation type"))
    creation_date = models.DateTimeField(auto_now_add = True, help_text = _(u"Establishment date"), verbose_name = _(u"Creation date"))
    last_update = models.DateTimeField(auto_now = True, help_text = _(u"Last update"), verbose_name = _(u"Last update"))
    
    @property
    def view_path(self):
        """
        It returns view's view path
        """
        if self.scheme_name is None or self.scheme_name == "":
            return "%s" % self.view.view_path
        else:
            return "%s" % self.scheme_name
    
    def get_absolute_url(self,upy_context):
        """
        It returns absolute url defined by node related to this page
        """
        try:    
            node = Node.objects.filter(page = self)[0]
            return node.get_absolute_url(upy_context)
        except Exception, e:
            raise ValueError("Error in %s.%s: %s" % (self.__module__,self.__class__.__name__,e))
            return ""
    
    def check_static_vars(self,pub_extended,node): 
        """
        This function check if a Page has static vars
        """
        if self.static_vars == "" and hasattr(self,"template"):
            self.static_vars = {'upy_context':{'template_name':self.template.file_name,}}
        elif hasattr(self,"template"):
            self.static_vars = literal_eval(self.static_vars)
            self.static_vars['upy_context']['template_name'] = self.template.file_name
        self.static_vars['upy_context']['PUB_EXTENDED'] = pub_extended
        self.static_vars['upy_context']['NODE'] = node
        self.static_vars['upy_context']['PAGE'] = self
    
    def save(self, *args, **kwargs):
        clean_cache(settings.UPYCACHE_DIR)
        super(Page,self).save( *args, **kwargs)
    
    def delete(self):
        clean_cache(settings.UPYCACHE_DIR)
        super(Page,self).delete()
    
    def __unicode__(self):
        return u"%s" % (self.name)
    
    class G11nMeta:
        g11n = 'PageG11n'
        fieldname = 'page'
    
    class Meta:
        verbose_name = _(u"Page")
        verbose_name_plural = _(u"Pages")
        ordering = ['name']

    @staticmethod
    def getCurrent(request, publication):
        """
        DEPRECATED: It calculates current page but it's in upy_context dictionary
        """
        if settings.MULTI_DOMAIN is False and settings.MULTI_PUBLICATION is True:
            page_url = request.get_full_path()
            page_url = page_url.split('/')[2:]
        else:
            page_url = request.get_full_path()
        page_url = page_url.split('?')[0]
        if page_url == "" or page_url == "/":
            try:
                return publication.index_node.page
            except:
                raise ValueError("No index_node set in current publication")
        try:
            page_url = page_url.split('/')
            page = Page.objects.get(slug__iexact=page_url[-2:-1][0])
            return page
        except Page.DoesNotExist:
            raise ValueError("Page Doesn't exist in %s.Page.getCurrent" % Page.__module__)
        except Exception, e:
            raise ValueError("Error in %s.Page: %s" % (Page.__module__,e))

        
     
class PageG11n(G11nModel):
    """
    This is the class that defines static contents of a page of the structure.
    """
    title = models.CharField(max_length = 150, null = True, blank = True, help_text = _(u"Set the page's title."),
                             verbose_name = _(u"Title"))
    description = models.CharField(max_length = 250, null = True, blank = True, help_text = _(u"Set the website's description."),
                                   verbose_name = _(u"Description"))
    keywords = models.CharField(max_length = 150, null = True, blank = True, 
                                help_text = _(u"Set the list of page's keywords. Don't use more than 10 words approximately."),
                                verbose_name = _(u"Keywords"))
    author = models.CharField(max_length = 150, null = True, blank = True, help_text = _(u"Set the page's author."),
                              verbose_name = _(u"Author"))
    content_type = models.CharField(max_length = 150, null = True, blank = True, help_text = _(u"Set the page's content type."),
                                    verbose_name = _(u"Content type"))
    enabled = models.BooleanField(default = True, help_text = _(u"Uncheck it to disable the page."),
                                  verbose_name = _(u"Enabled"))
    disabled_message = models.TextField(null = True, blank = True, help_text = _(u"Text or html code to use if the page is disabled."),
                                        verbose_name = _(u"Disabled message"))
    
    robots = models.CharField(max_length = 50, null = True, blank = True, choices = (("index,follow","index,follow"),
                                                           ("noindex,follow","noindex,follow"),
                                                           ("index,nofollow","index,nofollow"),
                                                           ("noindex,nofollow","noindex,nofollow"),
                                                           ),
                                    help_text = _(u"Select the value of meta tag robots if you want set it."),
                                    verbose_name = _(u"Robots"))
    page = models.ForeignKey(u"Page", help_text = _(u"Set the page to associate with the Page's Meta Content."),
                             verbose_name = _(u"Page"))
    g11n_creation_date = models.DateTimeField(auto_now_add = True, help_text = _(u"Establishment date"), verbose_name = _(u"Creation date"))
    g11n_last_update = models.DateTimeField(auto_now = True, help_text = _(u"Last update"), verbose_name = _(u"Last update"))
    
    def get_fields(self):
        """
        It returns all fields as key, value in a dictionary
        """
        return [(field.name, field.value_to_string(self)) for field in PageG11n._meta.fields]
        
    def save(self, *args, **kwargs):
        clean_cache(settings.UPYCACHE_DIR)
        super(PageG11n,self).save( *args, **kwargs)
    
    def delete(self):
        clean_cache(settings.UPYCACHE_DIR)
        super(PageG11n,self).delete()
    
    def __unicode__(self):
        return u"%s (%s, %s)" % (self.page.name,self.publication,self.language)
    
    class Meta:
        verbose_name = _(u"Page's G11n Content")
        verbose_name_plural = _(u"Page's G11n Contents")
        ordering = ['page']

def list_apps():
    """
    It returns a list of application contained in PROJECT_APPS
    """
    list_apps = []
    for app in settings.PROJECT_APPS:
        list_apps.append([app.split(".")[-1]]*2)
    return list_apps  

class Template(models.Model):
    """
    This is the class that defines a template
    """
    name = models.CharField(max_length = 100, help_text = _(u"Set the template's name."),verbose_name = _(u"Name"))
    app_name = models.CharField(max_length = 100, help_text = _(u"Set the application's name of the view."),
                                default = settings.PROJECT_APP_DEFAULT,choices = list_apps(),verbose_name = _(u"App name"))
    file_name = models.CharField(max_length = 150, help_text = _(u"Set the template's file name."), verbose_name = _(u"File name"))
    input_vars = models.TextField(null = True, blank = True, help_text = _(u"Set the variables required by template (separated with ,)."),
                                  verbose_name = _(u"Input vars"))
    css = models.ManyToManyField(u"Css", null = True, blank = True, help_text = _(u"TreeStructure's css"), verbose_name = _(u"Css"), through = u"CssTemplatePosition")
    
    js = models.ManyToManyField(u"Js", null = True, blank = True, help_text = _(u"TreeStructure's js"), verbose_name = _(u"Js"), through = u"JsTemplatePosition")
    
    creation_date = models.DateTimeField(auto_now_add = True, help_text = _(u"Establishment date"), verbose_name = _(u"Creation date"))
    last_update = models.DateTimeField(auto_now = True, help_text = _(u"Last update"), verbose_name = _(u"Last update"))
    
    def __unicode__(self):
        return u"%s" % (self.name)
    
    def save(self, *args, **kwargs):
        tmpl_path = u'%s/templates/' % self.app_name
        if settings.USE_GLOBAL_TEMPLATES_DIR:
            tmpl_path = u'%s/templates/%s/' % (settings.PROJECT_PATH,self.app_name)
        if not os.path.exists(tmpl_path):
            os.makedirs(tmpl_path)
        index_tpl_name = u"%sindex.html" % tmpl_path
        file_tpl_name = u'%s%s' % (tmpl_path, self.file_name)
        
        if not os.path.exists(index_tpl_name): #non sovrascrivo l'index se gia esiste
            file_tpl = open(index_tpl_name,"w")
            str_to_write = u"{% extends \"base.html\" %}\n{% load i18n %}\n\n{% block body %}\n\n{% block main_content %}\n"
            for var in self.input_vars.split(","):
                if var != "":
                    str_to_write += u"%s: {{%s}}<br/>\n" % (var,var)
            str_to_write += u"{% endblock main_content %}\n\n{% endblock body %}"
            file_tpl.write(str_to_write)
            file_tpl.close()
        
        
        if not os.path.exists(file_tpl_name): #non sovrascrivo il file se gia esiste
            file_tpl = open(file_tpl_name,"w")
            str_to_write = u"{% extends \"index.html\" %}\n{% load i18n %}\n\n{% block main_content %}\n"
            for var in self.input_vars.split(","):
                if var != "":
                    str_to_write += u"%s: {{%s}}<br/>\n" % (var,var)
            str_to_write += u"{% endblock main_content %}"
            file_tpl.write(str_to_write)
            file_tpl.close()
        super(Template,self).save( *args, **kwargs)
        
    class Meta:
        verbose_name = _(u"Template")
        verbose_name_plural = _(u"Templates")
        ordering = ['name']
 
 
class AbsView(models.Model):
    """
    This is the class that defines a view
    """
    name = models.CharField(max_length = 100, help_text = _(u"Set the view's name."),verbose_name = _(u"Name"))
    app_name = models.CharField(max_length = 100, help_text = _(u"Set the application's name of the view."),
                                default = settings.PROJECT_APP_DEFAULT,choices = list_apps(),verbose_name = _(u"App name"))
    func_name = models.CharField(max_length = 100, help_text = _(u"Set the view's function name."),
                                 verbose_name = _(u"Func name"))
    input_vars = models.TextField(null = True, blank = True, help_text = _(u"Set the input variables required by view."),
                                  verbose_name = _(u"Input vars"))
    output_vars = models.TextField(null = True, blank = True, 
                                   help_text = _(u"Set the json list of output variables required by template."),
                                   verbose_name = _(u"Output vars"))
    creation_date = models.DateTimeField(auto_now_add = True, help_text = _(u"Establishment date"), verbose_name = _(u"Creation date"))
    last_update = models.DateTimeField(auto_now = True, help_text = _(u"Last update"), verbose_name = _(u"Last update"))
    
    @property
    def view_path(self):
        """
        It returns view_path as string like: 'app_name.module_mane.func_name'
        """
        return "%s.%s.%s" % (self.app_name, self.module_name, self.func_name)
    
    def __unicode__(self):
        return u"%s" % (self.name)
    
    def save(self, *args, **kwargs):
        if not os.path.exists(u'%s/' % self.app_name):
            os.makedirs(u'%s/' % (self.app_name))
        file_view_name = u'%s/%s.py' % (self.app_name, self.module_name)
        
        found = False
        if os.path.exists(file_view_name):
            file_view = open(file_view_name,"r")
            for l in file_view.readlines():
                if l[:3] == "def":
                    cont = len(self.func_name)
                    if l[4:cont+4] == self.func_name:
                        found = True
            file_view.close()
        if not found:
            file_view = open(file_view_name,"a")
            upy_context_string = ", upy_context"
            if self.__class__.__name__ == "ViewAjax":
                upy_context_string = ""
            str_to_write = u"\ndef %s(request%s" % (self.func_name,upy_context_string)
            if self.input_vars != "" and self.input_vars:
                if self.input_vars[0:1] == ",":
                    self.input_vars = self.input_vars[1:]
                if self.input_vars[-1] == ",":
                    self.input_vars = self.input_vars[:-1]
                str_to_write += ", %s" % self.input_vars
            str_to_write += "):\n"
            if self.output_vars != "" and self.output_vars:
                outputvars = self.output_vars[1:-1]
                for item in outputvars.split(','):
                    obj_tuple = item.split(':')
                    str_to_write += "    %s = \"%s to initialize\"\n" % (obj_tuple[1],obj_tuple[1])
            
            str_to_write += "    return main_render(request%s" % upy_context_string
            if self.output_vars != "" and self.output_vars:
                str_to_write += ", %s" % self.output_vars
            else:
                str_to_write += ",{}"
            str_to_write += ")\n"
            file_view.write(str_to_write)
            file_view.close()
        super(AbsView,self).save( *args, **kwargs)
    
    class Meta:
        abstract = True
        
class View(AbsView):
    """
    It defines view object and it's used to write view definition in views.py module 
    """
    module_name = models.CharField(max_length = 100, default = u"views", help_text = _(u"Set the module's name of the view."),
                                   verbose_name = _(u"Module name"))
    class Meta:
        verbose_name = _(u"View")
        verbose_name_plural = _(u"Views")
        ordering = ['name']
        
class ViewAjax(AbsView):
    """
    It defines view object for views called by jQuery through ajax calls 
    and it's used to write view definition in viewsajax.py module 
    """
    module_name = models.CharField(max_length = 100, default = u"viewsajax", help_text = _(u"Set the module's name of the view."),
                                   verbose_name = _(u"Module name"))
    class Meta:
        verbose_name = _(u"ViewAjax")
        verbose_name_plural = _(u"ViewAjax")
        ordering = ['name']


class Robot(models.Model):
    """
    It defines robots definition for search engines
    """
    name_id = models.CharField(max_length = 250, help_text = _(u"Short name for the robot. Check the robots' list at <a target='_blank' href='http://www.robotstxt.org/db.html'>All Robots</a>"),
                            verbose_name = _(u"Name id"))
    name = models.CharField(max_length = 250, help_text = _(u"Full name for the robot"),
                            verbose_name = _(u"Name"))
    
    def __unicode__(self):
        return u"%s" % (self.name)
    
    class Meta:
        verbose_name = _(u"Robot")
        verbose_name_plural = _(u"Robots")
        ordering = ['name']
    

class CssTemplatePosition(models.Model):
    """
    It's used to order css files in templates
    """
    css = models.ForeignKey(u"Css", help_text = _(u"Css associated"), verbose_name = _(u"Css"))
    template = models.ForeignKey(u"Template", help_text = _(u"Template associated"), verbose_name = _(u"Template"))
    position = models.PositiveSmallIntegerField(u'Position', default=0)
    
    def save(self, *args, **kwargs):
        if not self.pk and self.position == 0:
            try:
                last = CssTemplatePosition.objects.select_related("css","template").all().order_by("position").reverse()[0]
                self.position = last.position + 1
            except:
                self.position = 0
        clean_cache(settings.UPYCACHE_DIR,"meta")
        super(CssTemplatePosition,self).save( *args, **kwargs)
    
    def delete(self):
        clean_cache(settings.UPYCACHE_DIR,"meta")
        super(CssTemplatePosition,self).delete()
       
    def __unicode__(self):
        return u"%s - %s - %s" % (self.css,self.template,self.position)
    
    class Meta:
        ordering = ["position",]
        verbose_name = _(u"Css/Template Position")
        verbose_name_plural = _(u"Css/Template Positions")

class CssTreeStructurePosition(models.Model):
    """
    It's used to order css files in treestructure objects
    """
    css = models.ForeignKey(u"Css", help_text = _(u"Css associated"), verbose_name = _(u"Css"))
    tree_structure = models.ForeignKey(u"TreeStructure", help_text = _(u"TreeStructure associated"), verbose_name = _(u"TreeStructure"))
    position = models.PositiveSmallIntegerField(u'Position', default=0)
    
    def save(self, *args, **kwargs):
        if not self.pk and self.position == 0:
            try:
                last = CssTreeStructurePosition.objects.select_related("css","tree_structure").all().order_by("position").reverse()[0]
                self.position = last.position + 1
            except:
                self.position = 0
        clean_cache(settings.UPYCACHE_DIR,"meta")
        super(CssTreeStructurePosition,self).save( *args, **kwargs)
    
    def delete(self):
        clean_cache(settings.UPYCACHE_DIR,"meta")
        super(CssTreeStructurePosition,self).delete()
       
    class Meta:
        ordering = ["position",]
        verbose_name = _(u"Css/TreeStructure Position")
        verbose_name_plural = _(u"Css/TreeStructure Positions")
    
class Css(models.Model):
    """
    It defines the css file location
    """
    name = models.CharField(max_length = 100, help_text = _(u"Set the css's name."),verbose_name = _(u"Name"))
    description = models.TextField(null = True, blank = True, help_text = _(u"Set the css's description."),
                                   verbose_name = _(u"Description"))
    file_name = models.FilePathField(path=settings.RELATIVE_STATIC_ROOT, match=".css", recursive=True, help_text = _(u"Set the css's file name."), verbose_name = _(u"File name"))
    
    @property
    def url(self):
        return self.file_name.replace(settings.RELATIVE_STATIC_ROOT,settings.STATIC_URL).replace("//","/")
        
    def save(self, *args, **kwargs):
        clean_cache(settings.UPYCACHE_DIR,"meta")
        super(Css,self).save( *args, **kwargs)
    
    def delete(self):
        clean_cache(settings.UPYCACHE_DIR,"meta")
        super(Css,self).delete()
        
    def __unicode__(self):
        return u"%s" % (self.name)
    
    class Meta:
        ordering = ["file_name",]
        verbose_name = _(u"Css")
        verbose_name_plural = _(u"Css")

class JsTemplatePosition(models.Model):
    """
    It's used to order js files in templates 
    """
    js = models.ForeignKey(u"Js", help_text = _(u"Js associated"), verbose_name = _(u"Js"))
    template = models.ForeignKey(u"Template", help_text = _(u"Template associated"), verbose_name = _(u"Template"))
    position = models.PositiveSmallIntegerField(u'Position', default=0)
    
    def save(self, *args, **kwargs):
        if not self.pk and self.position == 0:
            try:
                last = JsTemplatePosition.objects.select_related("js","template").all().order_by("position").reverse()[0]
                self.position = last.position + 1
            except:
                self.position = 0
        clean_cache(settings.UPYCACHE_DIR,"meta")
        super(JsTemplatePosition,self).save( *args, **kwargs)
    
    def delete(self):
        clean_cache(settings.UPYCACHE_DIR,"meta")
        super(JsTemplatePosition,self).delete()
            
    def __unicode__(self):
        return u"%s - %s - %s" % (self.js,self.template,self.position)
    
    class Meta:
        ordering = ["position",]
        verbose_name = _(u"Js/Template Position")
        verbose_name_plural = _(u"Js/Template Positions")
    
class JsTreeStructurePosition(models.Model):
    """
    It's used to order js files in treestructure objects
    """
    js = models.ForeignKey(u"Js", help_text = _(u"Js associated"), verbose_name = _(u"Js"))
    tree_structure = models.ForeignKey(u"TreeStructure", help_text = _(u"TreeStructure associated"), verbose_name = _(u"TreeStructure"))
    position = models.PositiveSmallIntegerField(u'Position', default=0)
    
    def save(self, *args, **kwargs):
        if not self.pk and self.position == 0:
            try:
                last = JsTreeStructurePosition.objects.select_related("js","tree_structure").all().order_by("position").reverse()[0]
                self.position = last.position + 1
            except:
                self.position = 0
        clean_cache(settings.UPYCACHE_DIR,"meta")
        super(JsTreeStructurePosition,self).save( *args, **kwargs)
     
    def delete(self):
        clean_cache(settings.UPYCACHE_DIR,"meta")
        super(JsTreeStructurePosition,self).delete()
           
    def __unicode__(self):
        return u"%s - %s - %s" % (self.js,self.tree_structure,self.position)
    
    class Meta:
        ordering = ["position",]
        verbose_name = _(u"Js/TreeStructure Position")
        verbose_name_plural = _(u"Js/TreeStructure Positions")
    
class Js(models.Model):
    """
    It defines the js file location
    """
    name = models.CharField(max_length = 100, help_text = _(u"Set the js's name."),verbose_name = _(u"Name"))
    description = models.TextField(null = True, blank = True, help_text = _(u"Set the js's description."),
                                   verbose_name = _(u"Description"))
    file_name = models.FilePathField(path=settings.RELATIVE_STATIC_ROOT, match=".js", recursive=True, help_text = _(u"Set the js's file name."), verbose_name = _(u"File name"))
    html_position = models.CharField(max_length = 50, choices = (("header","Header"),
                                                           ("footer","Footer"),
                                                           ),
                                    default = 'header',
                                    help_text = _(u"Select the position in the html file."),
                                    verbose_name = _(u"Html position"))
    
    @property
    def url(self):
        return self.file_name.replace(settings.RELATIVE_STATIC_ROOT,settings.STATIC_URL).replace("//","/")
    
    def save(self, *args, **kwargs):
        clean_cache(settings.UPYCACHE_DIR,"meta")
        super(Js,self).save( *args, **kwargs)
    
    def delete(self):
        clean_cache(settings.UPYCACHE_DIR,"meta")
        super(Js,self).delete()
        
    def __unicode__(self):
        return u"%s" % (self.name)
    
    class Meta:
        ordering = ["file_name",]
        verbose_name = _(u"Js")
        verbose_name_plural = _(u"Js")  
    
    
class UrlAjax(models.Model):
    """
    This is the class that defines an Url Ajax.
    """
    name = models.CharField(max_length = 50, unique = True, help_text = _(u"Identifying UrlAjax's name."),
                            verbose_name = _(u"Name"))
    slug = models.CharField(max_length = 50, unique = True, help_text = _(u"Identifying UrlAjax's url."),
                            verbose_name = _(u"Slug"))
    regex = models.CharField(max_length = 150, null = True, blank = True, help_text = _(u"Set the regular expression that completes the url (e.g. \"(?P<element_id>\d+)\")."),
                             verbose_name = _(u"Regex"))
    static_vars = models.TextField(null = True, blank = True, 
                                   help_text = _(u"Set the dictionary of static parameters of the UrlAjax in a regular format: {\"param1\":value1, \"param2\":value2}."),
                                   verbose_name = _(u"Static vars"))
    scheme_name = models.CharField(max_length = 100, null = True, blank = True, 
                                   help_text = _(u"Set the unique name to associate the view of a callback url."),
                                   verbose_name = _(u"Scheme name"))
    js = models.ForeignKey(u"Js", help_text = _(u"Set the Js to associate with the UrlAjax."),
                             verbose_name = _(u"Js"))
    view = models.ForeignKey(u"ViewAjax", help_text = _(u"Set the view to associate with the UrlAjax."),
                             verbose_name = _(u"View"))
    creation_date = models.DateTimeField(auto_now_add = True, help_text = _(u"Establishment date"), verbose_name = _(u"Creation date"))
    last_update = models.DateTimeField(auto_now = True, help_text = _(u"Last update"), verbose_name = _(u"Last update"))
    
    @property
    def view_path(self):
        """
        It returns view's view_path
        """
        if self.scheme_name is None or self.scheme_name == "":
            return "%s" % self.view.view_path
        else:
            return "%s" % self.scheme_name
    
    def __unicode__(self):
        return u"%s" % (self.name)
    
    def check_static_vars(self,pub_extended,node): 
        """
        DEPRECATED: There aren't NODES or PAGES associated to urlajax
        This function check if a UrlAjax has static vars
        """
        if self.static_vars == "":
            self.static_vars = {'upy_context':{}}
        else:
            self.static_vars = literal_eval(self.static_vars)
        self.static_vars['upy_context']['PUB_EXTENDED'] = pub_extended
        self.static_vars['upy_context']['NODE'] = node
        self.static_vars['upy_context']['PAGE'] = None
    
    class Meta:
        verbose_name = _(u"UrlAjax")
        verbose_name_plural = _(u"UrlAjax")
        ordering = ['name',]   