from django.conf import settings
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.utils.safestring import mark_safe
from upy.utils import compare_dicts,filter_files,clean_cache
import time

class Menu(object):
    """
    This class provides some tools to create and render tree structure menu in according to nodes' structure
    created for your application.
    It takes some arguments:
    - request: simply http request
    - root: the root of menu (it's hidden in menu string)
    - upy_context: it contains informations about current language, publication, page and node
    - menu_depth: it's depth level for menu introspection
    - view_hidden: if True then hidden nodes will be show
    - g11n_depth: check g11n_depth in contrib.g11n.models documentation
    """
    def __init__(self, request, root, upy_context, menu_depth = 0, view_hidden = False, g11n_depth = "publication_default"):
        self.request = request
        self.upy_context = upy_context 
        self.root = root
        self.menu_depth = menu_depth
        self.view_hidden = view_hidden
        self.g11n_depth = g11n_depth
        
    def __do_menu(self, menu_as, current_linkable = False, class_current = "", 
                chars = "", before_1 = "", after_1 = "", before_all = "", 
                after_all = "", render = True):
        """
        If there is a file in cache for current node's menu it returns this file, 
        else it calculates it and save file in cache
        """
        dict_cache = {'current_linkable':current_linkable, 
                    'class_current':class_current, 
                    'chars':chars, 
                    'before_1':before_1, 
                    'after_1':after_1,
                    'before_all':before_all,
                    'after_all':after_all,
                    'menu_depth': self.menu_depth,
                    'view_hidden': self.view_hidden,
                    'g11n_depth': self.g11n_depth
                    }
        str_groups = ""
        if self.request.user.__dict__:
            str_groups = ["%s" % g.pk for g in self.request.user.groups.all()]
            str_groups = "-%s" % "e".join(str_groups)   
        else:
            str_groups = "-nouser"
        
        for filename in filter_files(settings.UPYCACHE_DIR,
                                    u"menu-%s-%s-%s%s-%s" % (self.root.pk,
                                                        self.upy_context['NODE'].pk,
                                                        menu_as,str_groups,
                                                        self.request.LANGUAGE_CODE)):
            tempfile = open(u'%s%s' % (settings.UPYCACHE_DIR,filename))
            json = simplejson.loads(tempfile.read())
            if filename and compare_dicts(json,dict_cache):
                return mark_safe(json['menu'])
            else:
                clean_cache(settings.UPYCACHE_DIR,"menu")
                clean_cache(settings.UPYCACHE_DIR,"breadcrumb")

        nodes = self.root.get_descendants()
        if not settings.MULTI_DOMAIN and settings.MULTI_PUBLICATION:
            full_path = self.request.get_full_path()
            publication_url = "/%s" % full_path.split('/')[1]
        else:
            publication_url = ""
        list_nodes = []
        for node in nodes:
            if node.show_if_logged and self.request.user:
                if not node.groups.all():
                    node.hide_in_navigation = True
                else:
                    list_user_groups = str_groups.replace("-","").split("e")
                    for grp in node.groups.all():
                        if "%s" % grp.pk not in list_user_groups:
                            node.hide_in_navigation = True
                    
            try:
                node_g11n = node.g11n
            except:
                node_g11n = None
            else:
                if not node_g11n:
                    node.alias = node.name
                else:
                    node.alias = node_g11n.alias
            if node.page:
                if not node.value_regex:
                    node.url = "%s/%s%s/" % (publication_url, node.treeslug, node.page.slug)
                else:
                    node.url = "%s/%s%s/%s" % (publication_url, node.treeslug, node.page.slug,node.value_regex)
            else:
                node.url = None
            list_nodes.append(node)
        if not render:
            return list_nodes
        
        if self.menu_depth != 0:
            relative_depth = self.menu_depth + self.root.level
        else:
            relative_depth = 0
        
        menutpl = render_to_string('menu_%s.tpl.html' % menu_as, 
                              {'NODE': self.upy_context['NODE'], 'nodes' : list_nodes, 'chars' : chars, 'current_linkable' : current_linkable,
                               'menu_depth' : relative_depth, 'class_current' : class_current,
                               'view_hidden' : self.view_hidden, 'before_1' : before_1,
                               'after_1' : after_1, 'before_all' : before_all, 'after_all' : after_all,
                               }, context_instance=RequestContext(self.request))

        
        with open(u'%smenu-%s-%s-%s%s-%s-%s.json' % (settings.UPYCACHE_DIR,self.root.pk,self.upy_context['NODE'].pk,menu_as,str_groups,self.request.LANGUAGE_CODE,int(time.time())),"w") as file_menu:
            dict_cache['menu'] = menutpl
            data = simplejson.dumps(dict_cache)
            file_menu.write(data)
            
        return menutpl
        

    def as_ul(self, current_linkable = False, class_current = "active_link", 
                before_1 = "", after_1 = "", before_all = "", after_all = ""):
        """
        It returns menu as ul
        """
        return self.__do_menu("as_ul", current_linkable, class_current, 
                            before_1 = before_1, after_1 = after_1, before_all = before_all, after_all = after_all)
    
    def as_p(self, current_linkable = False, class_current = "active_link"):
        """
        It returns menu as p
        """
        return self.__do_menu("as_p", current_linkable, class_current)

    def as_string(self, chars, current_linkable = False, class_current = "active_link"):
        """
        It returns menu as string
        """
        return self.__do_menu("as_string", current_linkable, class_current, chars)

    def as_tree(self):
        """
        It returns a menu not cached as tree
        """
        return self.__do_menu("", render = False)


class Breadcrumb(object):
    """
    This class provides some tools to create and render tree structure breadcrumb in according to nodes' structure
    created for your application.
    It takes some arguments:
    - request: simply http request
    - leaf: the the leaf of breadcrumb (it's hidden in menu string)
    - upy_context: it contains informations about current language, publication, page and node
    - view_hidden: if True then hidden nodes will be show
    - g11n_depth: check g11n_depth in contrib.g11n.models documentation
    """
    def __init__(self, request, leaf, upy_context, view_hidden = False, g11n_depth = "publication_default"):
        self.request = request
        self.leaf = leaf
        self.upy_context = upy_context
        self.view_hidden = view_hidden
        self.g11n_depth = g11n_depth
        
    def __do_menu(self, menu_as, show_leaf, current_linkable, class_current, chars = ""):
        """
        If there is a file in cache for current node's breadcrumb it returns this file, 
        else it calculates it and save file in cache
        """
        dict_cache = {'current_linkable':current_linkable, 
                'class_current':class_current, 
                'chars':chars, 
                'show_leaf':show_leaf,
                'view_hidden': self.view_hidden,
                'g11n_depth': self.g11n_depth
                }
        
        str_groups = ""
        if self.request.user.__dict__:
            str_groups = ["%s" % g.pk for g in self.request.user.groups.all()]
            str_groups = "-%s" % "e".join(str_groups)   
        else:
            str_groups = "-nouser"
        
        for filename in filter_files(settings.UPYCACHE_DIR,u"breadcrumb-%s-%s-%s%s-%s" % (self.leaf.pk,self.upy_context['NODE'].pk,menu_as,str_groups,self.request.LANGUAGE_CODE)):
            tempfile = open(u'%s%s' % (settings.UPYCACHE_DIR,filename))
            json = simplejson.loads(tempfile.read())
            if filename and compare_dicts(json,dict_cache):
                return mark_safe(json['breadcrumb'])
            else:
                clean_cache(settings.UPYCACHE_DIR,"menu")
                clean_cache(settings.UPYCACHE_DIR,"breadcrumb")
        nodes = self.leaf.get_ancestors()[1:]
        list_nodes = list(nodes)
        if show_leaf:
            list_nodes.append(self.leaf)

        if settings.MULTI_DOMAIN is False and settings.MULTI_PUBLICATION is True:
            full_path = self.request.get_full_path()
            publication_url = "/%s" % full_path.split('/')[1]
        else:
            publication_url = ""
        for node in list_nodes:
            if node.show_if_logged and self.request.user:
                if not node.groups.all():
                    node.hide_in_navigation = True
                else:
                    list_user_groups = str_groups.replace("-","").split("e")
                    for grp in node.groups.all():
                        if "%s" % grp.pk not in list_user_groups:
                            node.hide_in_navigation = True
                    
            try:
                node_g11n = node.g11n
            except:
                node_g11n = None
            else:
                if not node_g11n:
                    node.alias = node.name
                else:
                    node.alias = node_g11n.alias
            if node.page:
                if not node.value_regex:
                    node.url = "%s/%s%s/" % (publication_url, node.treeslug, node.page.slug)
                else:
                    node.url = "%s/%s%s/%s" % (publication_url, node.treeslug, node.page.slug,node.value_regex)
            else:
                node.url = None
            
        menutpl = render_to_string('breadcrumb_%s.tpl.html' % menu_as, 
                              {'NODE': self.upy_context['NODE'], 'nodes' : list_nodes, 'chars' : chars, 'current_linkable' : current_linkable,
                               'class_current' : class_current,
                               'view_hidden' : self.view_hidden}, context_instance=RequestContext(self.request))
                
        with open(u'%sbreadcrumb-%s-%s-%s%s-%s-%s.json' % (settings.UPYCACHE_DIR,self.leaf.pk,self.upy_context['NODE'].pk,menu_as,str_groups,self.request.LANGUAGE_CODE,int(time.time())),"w") as file_menu:
            dict_cache['breadcrumb'] = menutpl
            data = simplejson.dumps(dict_cache)
            file_menu.write(data)
        return mark_safe(menutpl)
        

    def as_ul(self, show_leaf = True, current_linkable = False, class_current = "active_link"):
        """
        It returns breadcrumb as ul
        """
        return self.__do_menu("as_ul", show_leaf, current_linkable, class_current)
    
    def as_p(self, show_leaf = True, current_linkable = False, class_current = "active_link"):
        """
        It returns breadcrumb as p
        """
        return self.__do_menu("as_p", show_leaf, current_linkable, class_current)

    def as_string(self, chars, show_leaf = True, current_linkable = False, class_current = "active_link"):
        """
        It returns breadcrumb as string
        """
        return self.__do_menu("as_string", show_leaf, current_linkable, class_current, chars)
