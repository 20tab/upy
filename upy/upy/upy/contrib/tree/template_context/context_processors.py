from upy.utils import clean_path
from django.conf import settings
from django.utils import simplejson
import os

class MetaContent(object): 
    """
    MetaContent class define an object that contain informations about page or publication. 
    These informations are included in template.
    """
    def __init__(self):
        self.title = ""
        self.description = ""
        self.keywords = ""
        self.author = ""
        self.content_type = ""
        self.robots = ""
        self.generator = ""

    def fill_content(self, metaObject):
        """
        This method fills MetaContent with informations contained in metaObjetc
        """
        self.title = metaObject.title
        self.description = metaObject.description
        self.keywords = metaObject.keywords
        self.author = metaObject.author
        self.content_type = metaObject.content_type
        self.robots = metaObject.robots
        try: #perche' Page non ha generator
            self.generator = metaObject.generator            
        except:
            self.generator = ''
    
    
    def check_attr(self,item):
        """
        It checks if item is defined in self object
        """
        if hasattr(self,item):
            if not getattr(self, item) or getattr(self, item) == "":
                return False
        return True
         
    def jsonToMeta(self,json):
        """
        It sets all item in a json to self
        """
        for k,v in json.items():
            setattr(self,k,v)
    
         
    def get_fields(self):
        """
        It returns this object as a dictionary
        """
        return self.__dict__
    
    def __str__(self):
        return "%s" % self.title
        

def g11n(request):
    """
    This context processor returns meta informations contained in cached files. 
    If there aren't cache it calculates dictionary to return
    """
    context_extras = {}
    if not request.is_ajax() and hasattr(request ,'upy_context') and request.upy_context['PAGE']:
        page = request.upy_context['PAGE']
        node = request.upy_context['NODE']
        context_extras['PAGE'] = page
        context_extras['NODE'] = node
        pub_extended = request.upy_context['PUB_EXTENDED']
        context_extras['PUBLICATION'] = pub_extended.publication
        
        publication = pub_extended.publication
        
                                
        context_extras['ROOT'] = pub_extended.root
        
        filename="meta-%s-%s-%s.json" % (publication.pk,page.pk,node.pk)
        if os.path.exists("%s%s" % (settings.UPYCACHE_DIR,filename)):
            file_cache = open(u'%s%s' % (settings.UPYCACHE_DIR,filename))
            json = simplejson.loads(file_cache.read())
            meta_temp = MetaContent()
            meta_temp.jsonToMeta(json['META'])
            context_extras['META'] = meta_temp
            context_extras['MEDIA_CSS'] = json['MEDIA_CSS']
            context_extras['MEDIA_JS_HEADER'] = json['MEDIA_JS_HEADER']
            context_extras['MEDIA_JS_FOOTER'] = json['MEDIA_JS_FOOTER']
            return context_extras
        
        cache_json = {}
        
        try:
            context_extras['ROOT'] = pub_extended.root
            struct_js = pub_extended.tree_structure.js.all().order_by("jstreestructureposition")
            struct_css = [clean_path(css) for css in pub_extended.tree_structure.css.all().order_by("csstreestructureposition")]
            context_extras['STRUCT_CSS'] = struct_css
            
        except Exception, e:
            print "Error in %s: %s" %(__file__,e)
        finally:
            if page:
                page_js = page.template.js.all().order_by("jstemplateposition")
                page_css = [clean_path(css) for css in page.template.css.all().order_by("csstemplateposition")]
                context_extras['PAGE_CSS'] = page_css
    
                all_js_header = []
                all_js_footer = []
                for js in struct_js:
                    if js.html_position == "header":
                        all_js_header.append(js.url)
                    else:
                        all_js_footer.append(js.url)
    
                for js in page_js:
                    if js.html_position == "header":
                        all_js_header.append(js.url)
                    else:
                        all_js_footer.append(js.url)
                
                
                all_js_header_set = []
                for js in all_js_header:
                    if not js in all_js_header_set:
                        all_js_header_set.append(js)
                        
                all_js_footer_set = []
                
                for js in all_js_footer:
                    if not js in all_js_footer_set:
                        all_js_footer_set.append(js)
    
                context_extras['MEDIA_JS_HEADER'] = all_js_header_set
                context_extras['MEDIA_JS_FOOTER'] = all_js_footer_set
                cache_json['MEDIA_JS_HEADER'] = all_js_header_set
                cache_json['MEDIA_JS_FOOTER'] = all_js_footer_set
                
                
                all_css_set = []
                all_css_set_res = []
                all_css_set.extend(page_css)
                all_css_set.extend(struct_css)
                for css in all_css_set:
                    if not css in all_css_set_res:
                        all_css_set_res.append(css.url)
                context_extras['MEDIA_CSS'] = all_css_set_res
                cache_json['MEDIA_CSS'] = all_css_set_res
                
                meta_temp = MetaContent()
                
                if not page.g11n and not publication.g11n:
                    context_extras['META'] = "Error: No Meta Content Available."
                elif page.g11n is None:
                    meta_temp.fill_content(publication.g11n)
                    context_extras['META'] = meta_temp
                    cache_json['META'] = meta_temp.get_fields()
                elif publication.g11n is None:
                    meta_temp.fill_content(page.g11n)
                    context_extras['META'] = meta_temp
                    cache_json['META'] = meta_temp.get_fields()
                else:                        
                    attr_list = ('title', 'description', 'keywords', 'author', 'content_type', 'robots', 'generator',)
                    
                    for item in attr_list:
                        if hasattr(page.g11n, item):
                            setattr(meta_temp, item, getattr(page.g11n, item))
                    
                    for item in attr_list:
                        if hasattr(publication.g11n, item) and not meta_temp.check_attr(item):
                            setattr(meta_temp, item, getattr(publication.g11n, item))
                    
                cache_json['META'] = meta_temp.get_fields()
                context_extras['META'] = meta_temp
        try:
            filename="meta-%s-%s-%s.json" % (publication.pk,page.pk,node.pk)
            with open(u'%s%s' % (settings.UPYCACHE_DIR,filename),"w") as file_cache:
                data = simplejson.dumps(cache_json)
                file_cache.write(data)
        except Exception, e:
            print "Exception in upy.contrib.tree.template_context.context_processors at line 206: ", e
        
    return context_extras
    