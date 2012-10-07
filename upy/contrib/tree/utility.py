from django.conf.urls.defaults import url
from django.conf import settings
from django.template import RequestContext
from django.template.loader import render_to_string
from upy.contrib.tree.models import PublicationExtended,UrlAjax
from upy.utils import today
from django.template.defaultfilters import slugify
   
def getUrlList():
    """
    This function get the Page List from the DB and return the tuple to
    use in the urls.py, urlpatterns
    """
    """
    IF YOU WANT REBUILD YOUR STRUCTURE UNCOMMENT THE FOLLOWING LINE
    """
    #Node.rebuild()
    
    publications = PublicationExtended.objects.all()
    set_to_return = []
    set_login_required = []
    set_url = []
    struct_tmp = []
    
    for urlajax in UrlAjax.objects.all():
        regex = r'^%s/%s$' % (urlajax.slug, urlajax.regex)
        regex_path = '%s/%s' % (urlajax.slug, urlajax.regex)
        view = u'%s.%s.%s' % (urlajax.view.app_name,urlajax.view.module_name,urlajax.view.func_name)
        """
        check_static_vars add UPY_CONTEXT to urlajax
        """
        #urlajax.check_static_vars(pub_extended,pub_extended.index_node)
        app_url = url(regex, view, urlajax.static_vars, urlajax.scheme_name)
        set_to_return.append(app_url)
        set_url.append(regex_path)
    
    for pub_extended in publications:
        publication = pub_extended.publication
        if settings.MULTI_PUBLICATION:
            publication_url = "%s/" % slugify(publication.url)
        else:
            publication_url = ''
        if pub_extended.index_node:
            regex = r'^%s$' % publication_url
            regex_path = '%s' % publication_url
            page = pub_extended.index_node.page
            view = page.view
            view = u'%s.%s.%s' % (view.app_name,view.module_name,view.func_name)
            """
            check_static_vars add UPY_CONTEXT to page
            """
            page.check_static_vars(pub_extended,pub_extended.index_node)
            app_url = url(regex, view, page.static_vars, page.scheme_name)
            set_to_return.append(app_url)
            set_url.append(regex_path)
            if pub_extended.index_node.protected:
                set_login_required.append(regex)
        
        current_struct = pub_extended.tree_structure
        
        if current_struct not in struct_tmp:
            struct_tmp.append(current_struct)
            nodes = current_struct.tree_root.get_descendants()
            
                    
            for node in nodes:
                if node.page:
                    page = node.page
                    view = page.view
                    regex = r'^%s%s%s/%s$' % (publication_url, node.treeslug, page.slug, page.regex)
                    regex_path = '%s%s%s/%s' % (publication_url, node.treeslug, page.slug, page.regex)
                    if node.protected:
                        set_login_required.append(regex)
                    view = u'%s.%s.%s' % (view.app_name,view.module_name,view.func_name)
                    """
                    check_static_vars add UPY_CONTEXT to page
                    """
                    page.check_static_vars(pub_extended,node)
                    app_url = url(regex, view, page.static_vars, page.scheme_name)
                    set_to_return.append(app_url)
                    set_url.append(regex_path)    
    return set_to_return, set_login_required, set_url

class UrlSitemap():
    """
    It defines sitemap url's structure to make sitemap.xml file
    """
    def __init__(self, loc, lastmod = None, changefreq = None, priority = None):
        self.loc = loc
        self.lastmod = lastmod
        self.changefreq = changefreq
        self.priority = priority
        

class UPYSitemap():
    """
    It creates sitemap.xml
    """
    def __init__(self,request):
        self.request = request
        
    def _do_sitemap(self):
        host = self.request.get_host()
        publications = PublicationExtended.objects.all()
        set_to_return = []
        struct_tmp = []
        for pub_extended in publications:
            publication = pub_extended.publication
            if pub_extended.index_node:
                if settings.MULTI_DOMAIN is False and settings.MULTI_PUBLICATION is True:
                    regex = r'%s' % (publication.url)
                else:
                    regex = r''
                url_sitemap = UrlSitemap(loc = regex)
                set_to_return.append(url_sitemap)
            
            
            current_struct = pub_extended.tree_structure
            if current_struct not in struct_tmp:
                struct_tmp.append(current_struct)
                nodes = current_struct.tree_root.get_descendants()
                
                for node in nodes:
                    if node.page:
                        page = node.page
                        if settings.MULTI_DOMAIN is False and settings.MULTI_PUBLICATION is True:
                            regex = r'%s/%s%s/%s' % (publication.url, node.treeslug, page.slug, page.regex)
                        else:
                            regex = r'%s%s/%s' % (node.treeslug, page.slug, page.regex)
                            
                        url_sitemap = UrlSitemap(loc = regex)
                        if node.changefreq:
                            url_sitemap.changefreq = node.changefreq
                        if node.priority:
                            url_sitemap.priority = node.priority
                        set_to_return.append(url_sitemap)
        
        
        tpl_str = render_to_string('sitemap.tpl.html', 
                              {'set' : set_to_return, 'host' : host, 'today': today(),}, context_instance=RequestContext(self.request))
        
        return tpl_str
    
class UPYRobotTXT():
    """
    It creates robots.txt
    """
    def __init__(self,request):
        self.request = request
        
    def _do_robotstxt(self):
        publications = PublicationExtended.objects.all()
        set_robot = {}
        struct_tmp = []
        for pub_extended in publications:
            publication = pub_extended.publication
            publication_url = ''
            if settings.MULTI_DOMAIN is False and settings.MULTI_PUBLICATION is True:
                publication_url = '%s/' % publication.url
            
            current_struct = pub_extended.tree_structure
            if current_struct not in struct_tmp:
                struct_tmp.append(current_struct)
                nodes = current_struct.tree_root.get_descendants()
                
                for node in nodes:
                    if node.page and node.disallow:
                        page = node.page
                        regex = r'%s/%s%s/%s' % (publication_url, node.treeslug, page.slug, page.regex)
                        
                        for robot in node.robots.all():
                            if robot.name_id in set_robot.keys():
                                set_robot[robot.name_id].append(regex)
                            else:
                                set_robot[robot.name_id] =[regex,]
                        
        
        
        tpl_str = render_to_string('robots.tpl.html', 
                              {'set' : set_robot,}, context_instance=RequestContext(self.request))
        
        return tpl_str