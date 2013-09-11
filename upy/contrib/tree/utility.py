from django.conf.urls import url
from django.conf import settings
from django.template import RequestContext
from django.template.loader import render_to_string
from upy.contrib.tree.models import Node, UrlAjax
from datetime import date


def getUrlList():
    """
    This function get the Page List from the DB and return the tuple to
    use in the urls.py, urlpatterns
    """
    """
    IF YOU WANT REBUILD YOUR STRUCTURE UNCOMMENT THE FOLLOWING LINE
    """
    #Node.rebuild()

    set_to_return = []
    set_url = []

    for urlajax in UrlAjax.objects.select_related().all():
        regex = r'^{0}/{1}$'.format(urlajax.slug, urlajax.regex)
        regex_path = '{0}/{1}'.format(urlajax.slug, urlajax.regex)
        view = u'%s.%s.%s' % (urlajax.view.app_name, urlajax.view.module_name, urlajax.view.func_name)
        app_url = url(regex, view, urlajax.static_vars, urlajax.scheme_name)
        set_to_return.append(app_url)
        set_url.append(regex_path)

    roots = Node.objects.filter(parent__isnull=True)
    for root in roots:
        nodes = root.get_descendants()
        for node in nodes:
            if node.page:
                page = node.page
                view = page.view
                regex = r'^{0}$'.format(node.get_absolute_url())
                print "REGEX: ", regex
                regex_path = '{0}'.format(node.get_pattern())

                view = u'{0}.{1}.{2}'.format(view.app_name, view.module_name, view.func_name)
                """
                check_static_vars add UPY_CONTEXT to page
                """
                page.check_static_vars(node)
                app_url = url(regex, view, page.static_vars, page.scheme_name)
                set_to_return.append(app_url)
                set_url.append(regex_path)
                if node.is_index:
                    regex = r'^$'
                    regex_path = ''
                    app_url = url(regex, view, page.static_vars, page.scheme_name)
                    set_to_return.append(app_url)
                    set_url.append(regex_path)

    return set_to_return, set_url


class UrlSitemap():
    """
    It defines sitemap url's structure to make sitemap.xml file
    """

    def __init__(self, loc, lastmod=None, changefreq=None, priority=None):
        self.loc = loc
        self.lastmod = lastmod
        self.changefreq = changefreq
        self.priority = priority


class UPYSitemap():
    """
    It creates sitemap.xml
    """

    def __init__(self, request):
        self.request = request

    def _do_sitemap(self):
        host = self.request.get_host()
        set_to_return = []
        for root in Node.objects.filter(parent__isnull=True):
            for node in root.get_descendants():
                if node.page:
                    regex = r'%s' % node.slug
                    url_sitemap = UrlSitemap(loc=regex)
                    if node.changefreq:
                        url_sitemap.changefreq = node.changefreq
                    if node.priority:
                        url_sitemap.priority = node.priority
                    set_to_return.append(url_sitemap)
                if node.is_index:
                    regex = r''
                    url_sitemap = UrlSitemap(loc=regex)
                    set_to_return.append(url_sitemap)
        tpl_str = render_to_string('sitemap.tpl.html',
                                   {'set': set_to_return, 'host': host, 'today': date.today(), },
                                   context_instance=RequestContext(self.request))

        return tpl_str


class UPYRobotTXT():
    """
    It creates robots.txt
    """

    def __init__(self, request):
        self.request = request

    def _do_robotstxt(self):
        set_robot = {}
        disallow_all = settings.DIDALLOW_ALL_ROBOTS
        struct_tmp = []
        if not disallow_all:
            for root in Node.objects.filter(parent__isnull=True):
                for node in root.get_descendants():
                    if node.page and node.disallow:
                        regex = r'{0}'.format(node.slug)

                        for robot in node.robots.all():
                            if robot.name_id in set_robot.keys():
                                set_robot[robot.name_id].append(regex)
                            else:
                                set_robot[robot.name_id] = [regex, ]
        tpl_str = render_to_string('robots.tpl.html',
                                   {'set': set_robot, 'disallow_all': disallow_all},
                                   context_instance=RequestContext(self.request))

        return tpl_str