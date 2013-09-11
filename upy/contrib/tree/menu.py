from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class Menu(object):
    """
    This class provides some tools to create and render tree structure menu in according to nodes' structure
    created for your application.
    It takes some arguments:
    - request: simply http request
    - root: the root of menu (it's hidden in menu string)
    - upy_context: it contains informations about current page and node
    - menu_depth: it's depth level for menu introspection
    - view_hidden: if True then hidden nodes will be shown
    - g11n_depth: check g11n_depth in contrib.g11n.models documentation
    """

    def __init__(self, request, root, upy_context, menu_depth=0, view_hidden=False):
        self.request = request
        self.upy_context = upy_context
        self.root = root
        self.menu_depth = menu_depth
        self.view_hidden = view_hidden

    def __do_menu(self, menu_as, current_linkable=False, class_current="",
                  chars="", before_1="", after_1="", before_all="",
                  after_all="", render=True):
        """
        If there is a file in cache for current node's menu it returns this file, 
        else it calculates it and save file in cache
        """
        dict_cache = {'current_linkable': current_linkable,
                      'class_current': class_current,
                      'chars': chars,
                      'before_1': before_1,
                      'after_1': after_1,
                      'before_all': before_all,
                      'after_all': after_all,
                      'menu_depth': self.menu_depth,
                      'view_hidden': self.view_hidden
        }
        str_groups = ""
        if self.request.user.__dict__:
            str_groups = ["%s" % g.pk for g in self.request.user.groups.all()]
            str_groups = "-%s" % "e".join(str_groups)
        else:
            str_groups = "-nouser"

        nodes = self.root.get_descendants()
        list_nodes = []
        for node in nodes:
            if node.slugable:
                if node.show_if_logged and self.request.user:
                    if not node.groups.all():
                        node.hide_in_navigation = True
                    else:
                        list_user_groups = str_groups.replace("-", "").split("e")
                        for grp in node.groups.all():
                            if "%s" % grp.pk not in list_user_groups:
                                node.hide_in_navigation = True

                try:
                    node.alias = node.transnode.alias
                except:
                    node.alias = node.name
                if node.page:
                    node.url = node.slug
                else:
                    node.url = None
                list_nodes.append(node)
        if not render:
            return list_nodes

        if self.menu_depth != 0:
            relative_depth = self.menu_depth + self.root.level
        else:
            relative_depth = 0

        return render_to_string('menu_%s.tpl.html' % menu_as,
                                {'NODE': self.upy_context['NODE'], 'nodes': list_nodes, 'chars': chars,
                                 'current_linkable': current_linkable,
                                 'menu_depth': relative_depth, 'class_current': class_current,
                                 'view_hidden': self.view_hidden, 'before_1': before_1,
                                 'after_1': after_1, 'before_all': before_all, 'after_all': after_all,
                                }, context_instance=RequestContext(self.request))

    def as_ul(self, current_linkable=False, class_current="active_link",
              before_1="", after_1="", before_all="", after_all=""):
        """
        It returns menu as ul
        """
        return self.__do_menu("as_ul", current_linkable, class_current,
                              before_1=before_1, after_1=after_1, before_all=before_all, after_all=after_all)

    def as_p(self, current_linkable=False, class_current="active_link"):
        """
        It returns menu as p
        """
        return self.__do_menu("as_p", current_linkable, class_current)

    def as_string(self, chars, current_linkable=False, class_current="active_link"):
        """
        It returns menu as string
        """
        return self.__do_menu("as_string", current_linkable, class_current, chars)

    def as_tree(self):
        """
        It returns a menu not cached as tree
        """
        return self.__do_menu("", render=False)


class Breadcrumb(object):
    """
    This class provides some tools to create and render tree structure breadcrumb in according to nodes' structure
    created for your application.
    It takes some arguments:
    - request: simply http request
    - leaf: the the leaf of breadcrumb (it's hidden in menu string)
    - upy_context: it contains informations about current page and node
    - view_hidden: if True then hidden nodes will be show
    - g11n_depth: check g11n_depth in contrib.g11n.models documentation
    """

    def __init__(self, request, leaf, upy_context, view_hidden=False):
        self.request = request
        self.leaf = leaf
        self.upy_context = upy_context
        self.view_hidden = view_hidden

    def __do_menu(self, menu_as, show_leaf, current_linkable, class_current, chars="", render=True):
        """
        If there is a file in cache for current node's breadcrumb it returns this file, 
        else it calculates it and save file in cache
        """
        dict_cache = {'current_linkable': current_linkable,
                      'class_current': class_current,
                      'chars': chars,
                      'show_leaf': show_leaf,
                      'view_hidden': self.view_hidden
        }

        str_groups = ""
        if self.request.user.__dict__:
            str_groups = ["%s" % g.pk for g in self.request.user.groups.all()]
            str_groups = "-%s" % "e".join(str_groups)
        else:
            str_groups = "-nouser"

        nodes = self.leaf.get_ancestors()[1:]
        list_nodes = list(nodes)
        if show_leaf:
            list_nodes.append(self.leaf)

        for node in list_nodes:
            if node.slugable:
                if node.show_if_logged and self.request.user:
                    if not node.groups.all():
                        node.hide_in_navigation = True
                    else:
                        list_user_groups = str_groups.replace("-", "").split("e")
                        for grp in node.groups.all():
                            if "%s" % grp.pk not in list_user_groups:
                                node.hide_in_navigation = True

                try:
                    node.alias = node.transnode.alias
                except:
                    node.alias = node.name
                if node.page:
                    if not node.value_regex:
                        node.url = node.slug
                else:
                    node.url = None

        if not render:
            return list_nodes

        menutpl = render_to_string('breadcrumb_%s.tpl.html' % menu_as,
                                   {'NODE': self.upy_context['NODE'], 'nodes': list_nodes, 'chars': chars,
                                    'current_linkable': current_linkable,
                                    'class_current': class_current,
                                    'view_hidden': self.view_hidden}, context_instance=RequestContext(self.request))

        return mark_safe(menutpl)

    def as_ul(self, show_leaf=True, current_linkable=False, class_current="active_link"):
        """
        It returns breadcrumb as ul
        """
        return self.__do_menu("as_ul", show_leaf, current_linkable, class_current)

    def as_p(self, show_leaf=True, current_linkable=False, class_current="active_link"):
        """
        It returns breadcrumb as p
        """
        return self.__do_menu("as_p", show_leaf, current_linkable, class_current)

    def as_string(self, chars, show_leaf=True, current_linkable=False, class_current="active_link"):
        """
        It returns breadcrumb as string
        """
        return self.__do_menu("as_string", show_leaf, current_linkable, class_current, chars)

    def as_tree(self):
        """
        It returns a menu not cached as tree
        """
        return self.__do_menu("", render=False)