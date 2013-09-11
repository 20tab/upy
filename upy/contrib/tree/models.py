from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from django.contrib.auth.models import Group
from ast import literal_eval
import os
from upy.models import UpyModel
from upy.fields import NullTrueField


class Node(MPTTModel, UpyModel):
    """
    This is the class that defines tree's nodes.
    """
    name = models.CharField(max_length=50, help_text=_(u"Identifying name of the associated page."),
                            verbose_name=_(u"Name"))
    page = models.ForeignKey(u"Page", null=True, blank=True, help_text=_(u"Set the page for the referenced node."),
                             verbose_name=_(u"Page"))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children',
                            help_text=_(u"Set the parent node for this node if it isn't root."),
                            verbose_name=_(u"Parent"))
    position = models.PositiveSmallIntegerField(u'Position', default=0)
    is_index = NullTrueField(_('Is index node?'), default=None, unique=True)
    hide_in_navigation = models.BooleanField(help_text=_(u"Check it to hide the page in this node in the navigation."),
                                             verbose_name=_(u"Hide in navigation"))
    hide_in_url = models.BooleanField(
        _(u'Hide in url'),
        help_text=_(u"Check it to hide the node in url path (only if node hasn't a page)."))
    show_if_logged = models.BooleanField(
        help_text=_(u"Check it if this node must be showed only for logged user or group."),
        verbose_name=_(u"Show if logged"))
    groups = models.ManyToManyField(Group, null=True, blank=True,
                                    help_text=_(u"List of groups to use with 'show if logged' parameter."),
                                    verbose_name=_(u"Groups"), related_name='node_groups')
    value_regex = models.CharField(max_length=50, null=True, blank=True,
                                   help_text=_(u"Set the value to respect the regex of the associated page."),
                                   verbose_name=_(u"Value regex"))
    changefreq = models.CharField(max_length=50, null=True, blank=True, choices=(("always", "always"),
                                                                                 ("hourly", "hourly"),
                                                                                 ("daily", "daily"),
                                                                                 ("weekly", "weekly"),
                                                                                 ("monthly", "monthly"),
                                                                                 ("yearly", "yearly"),
                                                                                 ("never", "never")),
                                  help_text=_(u"The chengefreq attribute for sitemap.xml"),
                                  verbose_name=_(u"Changefreq"))
    priority = models.CharField(max_length=50, choices=(("0.1", "0.1"),
                                                        ("0.2", "0.2"),
                                                        ("0.3", "0.3"),
                                                        ("0.4", "0.4"),
                                                        ("0.5", "0.5"),
                                                        ("0.6", "0.6"),
                                                        ("0.7", "0.7"),
                                                        ("0.8", "0.8"),
                                                        ("0.9", "0.9"),
                                                        ("1.0", "1.0"),),
                                default="0.5",
                                help_text=_(u"The priority attribute for sitemap.xml"),
                                verbose_name=_(u"Priority"))
    robots = models.ManyToManyField(u"Robot", null=True, blank=True,
                                    help_text=_(u"List of robots to communicate that this node is disallowed."),
                                    verbose_name=_(u"Robots"))
    disallow = models.BooleanField(help_text=_(u"Check it to disallow the page in this node in the file robots.txt."),
                                   verbose_name=_(u"Disallow"))

    @property
    def page_name(self):
        """
        It returns page's name of this node
        """
        if self.page:
            return self.page.name
        return ""

    @property
    def view_path(self):
        """
        It returns page's view_path
        """
        if self.page:
            return self.page.view_path
        return ""

    @property
    def slug(self):
        """
        It returns node's slug
        """
        if self.is_root_node():
            return ""
        if self.slugable and self.parent.parent:
            if not self.page.regex or (self.page.regex and not self.page.show_regex) or self.is_leaf_node():
                return u"{0}/{1}".format(self.parent.slug, self.page.slug)
            elif self.page.regex and self.value_regex and self.page.show_regex:
                return u'{0}/{1}/{2}'.format(self.parent.slug, self.page.slug, self.value_regex)
            elif not self.hide_in_url:
                return u'{0}/{1}'.format(self.parent.slug, self.name)
        elif self.slugable:
            if not self.page.regex or (self.page.regex and not self.page.show_regex) or self.is_leaf_node():
                return u"{0}".format(self.page.slug)
            elif self.page.regex and self.value_regex and self.page.show_regex:
                return u'{0}/{1}'.format( self.page.slug, self.value_regex)
            elif not self.hide_in_url:
                return u'{0}'.format(self.name)
        return ""

    @property
    def slugable(self):
        """
        A node is slugable in following cases:
        1 - Node doesn't have children.
        2 - Node has children but its page doesn't have a regex.
        3 - Node has children, its page has regex but it doesn't show it.
        4 - Node has children, its page shows his regex and node has a default value for regex.
        5 - Node hasn't a page but it ins't hidden in url.
        """
        if self.page:
            if self.is_leaf_node():
                return True
            if not self.is_leaf_node() and not self.page.regex:
                return True
            if not self.is_leaf_node() and self.page.regex and not self.page.show_regex:
                return True
            if not self.is_leaf_node() and self.page.regex and self.page.show_regex and self.value_regex:
                return True
        elif not self.is_leaf_node() and not self.hide_in_url:
            return True
        return False

    def get_pattern(self):
        """
        It returns its url pattern
        """
        if self.is_root_node():
            return ""
        else:
            parent_pattern = self.parent.get_pattern()
            if parent_pattern != "":
                parent_pattern = u"{}".format(parent_pattern)
            if not self.page and not self.is_leaf_node():
                if self.hide_in_url:
                    return u'{0}'.format(parent_pattern)
                else:
                    return u'{0}{1}'.format(parent_pattern, self.name)
            else:
                if self.is_leaf_node() and self.page.regex and self.page.show_regex:
                    return u'{0}{1}/{2}'.format(parent_pattern, self.page.slug, self.page.regex)
                elif self.is_leaf_node() and (not self.page.regex or not self.page.show_regex):
                    return u'{0}{1}/'.format(parent_pattern, self.page.slug)
                elif not self.is_leaf_node() and self.page.regex and self.page.show_regex:
                    return u'{0}{1}/{2}/'.format(parent_pattern, self.page.slug, self.page.regex)
                else:
                    return u'{0}{1}/'.format(parent_pattern, self.page.slug)

    def get_absolute_url(self):
        """
        It returns simply a link as string
        """
        return u"{0}".format(self.slug)

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
        return u"{0} ({1})".format(self.name, page_name)

    class Meta:
        verbose_name = _(u"Node")
        verbose_name_plural = _(u"Nodes")
        ordering = ['tree_id', 'lft']


class Page(UpyModel):
    """
    This is the class that defines a page of the structure.
    """
    name = models.CharField(max_length=50, unique=True, help_text=_(u"Identifying page's name."),
                            verbose_name=_(u"Name"))
    slug = models.SlugField(max_length=50, help_text=_(u"Identifying page's url."),
                            verbose_name=_(u"Slug"))
    regex = models.CharField(max_length=150, null=True, blank=True, help_text=_(
        u"Set the regular expression that completes the url (e.g. \"(?P<element_id>\d+)\")."),
                             verbose_name=_(u"Regex"))
    show_regex = models.BooleanField(_(u'Show regex'), default=True,
                                     help_text=_(u'If it\'s checked the regex will be shown in urlpattern'))
    static_vars = models.TextField(
        null=True, blank=True,
        help_text=_(
            u"""Set the dictionary of static parameters of the page in a regular format:
            {\"param1\":value1, \"param2\":value2}."""),
        verbose_name=_(u"Static vars")
    )
    scheme_name = models.CharField(max_length=100, null=True, blank=True,
                                   help_text=_(u"Set the unique name to associate the view of a callback url."),
                                   verbose_name=_(u"Scheme name"))
    template = models.ForeignKey(u"Template", help_text=_(u"Set the template to associate with the page."),
                                 verbose_name=_(u"Template"))
    view = models.ForeignKey(u"View", help_text=_(u"Set the view to associate with the page."),
                             verbose_name=_(u"View"))
    presentation_type = models.CharField(max_length=150, null=True, blank=True,
                                         choices=(("StaticPage", "StaticPage"), ("Custom", "Custom"),),
                                         help_text=_(u"Select the presentation type."),
                                         verbose_name=_(u"Presentation type"))

    @property
    def view_path(self):
        """
        It returns view's view path
        """
        if self.scheme_name is None or self.scheme_name == "":
            return self.view.view_path
        else:
            return self.scheme_name

    def get_absolute_url(self):
        """
        It returns absolute url defined by node related to this page
        """
        try:
            node = Node.objects.select_related().filter(page=self)[0]
            return node.get_absolute_url()
        except Exception, e:
            raise ValueError(u"Error in {0}.{1}: {2}".format(self.__module__, self.__class__.__name__, e))
            return u""

    def check_static_vars(self, node):
        """
        This function check if a Page has static vars
        """
        if self.static_vars == "" and hasattr(self, "template"):
            self.static_vars = {'upy_context': {'template_name': self.template.file_name, }}
        elif hasattr(self, "template"):
            self.static_vars = literal_eval(self.static_vars)
            self.static_vars['upy_context']['template_name'] = self.template.file_name
        self.static_vars['upy_context']['NODE'] = node
        self.static_vars['upy_context']['PAGE'] = self

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u"Page")
        verbose_name_plural = _(u"Pages")
        ordering = ['name']


def list_apps():
    """
    It returns a list of application contained in PROJECT_APPS
    """
    list_apps = []
    for app in [x for x in settings.PROJECT_APPS if x not in ['south', ]]:
        list_apps.append([app.split(".")[-1]] * 2)
    return list_apps


class Template(UpyModel):
    """
    This is the class that defines a template
    """
    name = models.CharField(max_length=100, help_text=_(u"Set the template's name."), verbose_name=_(u"Name"))
    app_name = models.CharField(max_length=100, help_text=_(u"Set the application's name of the view."),
                                default=settings.PROJECT_APP_DEFAULT, choices=list_apps(), verbose_name=_(u"App name"))
    file_name = models.CharField(max_length=150, help_text=_(u"Set the template's file name."),
                                 verbose_name=_(u"File name"))
    input_vars = models.TextField(null=True, blank=True,
                                  help_text=_(u"Set the variables required by template (separated with ,)."),
                                  verbose_name=_(u"Input vars"))

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        tmpl_path = u'%s/templates/' % self.app_name
        if settings.USE_GLOBAL_TEMPLATES_DIR:
            tmpl_path = u'%s/templates/%s/' % (settings.PROJECT_PATH, self.app_name)
        if not os.path.exists(tmpl_path):
            os.makedirs(tmpl_path)
        index_tpl_name = u"%sindex.html" % tmpl_path
        file_tpl_name = u'%s%s' % (tmpl_path, self.file_name)

        if not os.path.exists(index_tpl_name): #non sovrascrivo l'index se gia esiste
            file_tpl = open(index_tpl_name, "w")
            str_to_write = u"{% extends \"base.html\" %}\n{% load i18n %}\n\n{% block body %}\n\n{% block main_content %}\n"
            for var in self.input_vars.split(","):
                if var != "":
                    str_to_write += u"%s: {{%s}}<br/>\n" % (var, var)
            str_to_write += u"{% endblock main_content %}\n\n{% endblock body %}"
            file_tpl.write(str_to_write)
            file_tpl.close()

        if not os.path.exists(file_tpl_name): #non sovrascrivo il file se gia esiste
            file_tpl = open(file_tpl_name, "w")
            str_to_write = u"{% extends \"index.html\" %}\n{% load i18n %}\n\n{% block main_content %}\n"
            for var in self.input_vars.split(","):
                if var != "":
                    str_to_write += u"%s: {{%s}}<br/>\n" % (var, var)
            str_to_write += u"{% endblock main_content %}"
            file_tpl.write(str_to_write)
            file_tpl.close()
        super(Template, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u"Template")
        verbose_name_plural = _(u"Templates")
        ordering = ['name']


class AbsView(UpyModel):
    """
    This is the class that defines a view
    """
    name = models.CharField(max_length=100, help_text=_(u"Set the view's name."), verbose_name=_(u"Name"))
    app_name = models.CharField(max_length=100, help_text=_(u"Set the application's name of the view."),
                                default=settings.PROJECT_APP_DEFAULT, choices=list_apps(), verbose_name=_(u"App name"))
    func_name = models.CharField(max_length=100, help_text=_(u"Set the view's function name."),
                                 verbose_name=_(u"Func name"))
    input_vars = models.TextField(null=True, blank=True, help_text=_(u"Set the input variables required by view."),
                                  verbose_name=_(u"Input vars"))
    output_vars = models.TextField(null=True, blank=True,
                                   help_text=_(u"Set the json list of output variables required by template."),
                                   verbose_name=_(u"Output vars"))

    @property
    def view_path(self):
        """
        It returns view_path as string like: 'app_name.module_mane.func_name'
        """
        return u"{0}.{1}.{2}".format(self.app_name, self.module_name, self.func_name)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not os.path.exists(u'{0}/'.format(self.app_name)):
            os.makedirs(u'{0}/'.format(self.app_name))
        file_view_name = u'{0}/{1}.py'.format(self.app_name, self.module_name)

        found = False
        if os.path.exists(file_view_name):
            file_view = open(file_view_name, "r")
            for l in file_view.readlines():
                if l[:3] == "def":
                    cont = len(self.func_name)
                    if l[4:cont + 4] == self.func_name:
                        found = True
            file_view.close()
        if not found:
            file_view = open(file_view_name, "a")
            upy_context_string = ", upy_context"
            if self.__class__.__name__ == "ViewAjax":
                upy_context_string = ""
            str_to_write = u"\ndef %s(request%s" % (self.func_name, upy_context_string)
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
                    str_to_write += "    {0} = \"{1} to initialize\"\n".format(obj_tuple[1], obj_tuple[1])

            str_to_write += "    return main_render(request{0}".format(upy_context_string)
            if self.output_vars != "" and self.output_vars:
                str_to_write += ", {0}".format(self.output_vars)
            else:
                str_to_write += ",{}"
            str_to_write += ")\n"
            file_view.write(str_to_write)
            file_view.close()
        super(AbsView, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class View(AbsView):
    """
    It defines view object and it's used to write view definition in views.py module 
    """
    module_name = models.CharField(max_length=100, default=u"views", help_text=_(u"Set the module's name of the view."),
                                   verbose_name=_(u"Module name"))

    class Meta:
        verbose_name = _(u"View")
        verbose_name_plural = _(u"Views")
        ordering = ['name']


class ViewAjax(AbsView):
    """
    It defines view object for views called by jQuery through ajax calls 
    and it's used to write view definition in viewsajax.py module 
    """
    module_name = models.CharField(max_length=100, default=u"viewsajax",
                                   help_text=_(u"Set the module's name of the view."),
                                   verbose_name=_(u"Module name"))

    class Meta:
        verbose_name = _(u"ViewAjax")
        verbose_name_plural = _(u"ViewAjax")
        ordering = ['name']


class Robot(UpyModel):
    """
    It defines robots definition for search engines
    """
    name_id = models.CharField(
        max_length=250,
        help_text=_(
            u"""Short name for the robot. Check the robots' list at
            <a target='_blank' href='http://www.robotstxt.org/db.html'>All Robots</a>"""),
        verbose_name=_(u"Name id")
    )
    name = models.CharField(max_length=250, help_text=_(u"Full name for the robot"),
                            verbose_name=_(u"Name"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u"Robot")
        verbose_name_plural = _(u"Robots")
        ordering = ['name']


class UrlAjax(UpyModel):
    """
    This is the class that defines an Url Ajax.
    """
    name = models.CharField(max_length=50, unique=True, help_text=_(u"Identifying UrlAjax's name."),
                            verbose_name=_(u"Name"))
    slug = models.CharField(max_length=50, unique=True, help_text=_(u"Identifying UrlAjax's url."),
                            verbose_name=_(u"Slug"))
    regex = models.CharField(max_length=150, null=True, blank=True, help_text=_(
        u"Set the regular expression that completes the url (e.g. \"(?P<element_id>\d+)\")."),
                             verbose_name=_(u"Regex"))
    static_vars = models.TextField(
        null=True, blank=True,
        help_text=_(
            u"""Set the dictionary of static parameters of the UrlAjax in a regular format:
            {\"param1\":value1, \"param2\":value2}."""),
        verbose_name=_(u"Static vars")
    )
    scheme_name = models.CharField(max_length=100, null=True, blank=True,
                                   help_text=_(u"Set the unique name to associate the view of a callback url."),
                                   verbose_name=_(u"Scheme name"))
    view = models.ForeignKey(u"ViewAjax", help_text=_(u"Set the view to associate with the UrlAjax."),
                             verbose_name=_(u"View"))

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

    class Meta:
        verbose_name = _(u"UrlAjax")
        verbose_name_plural = _(u"UrlAjax")
        ordering = ['name', ]
