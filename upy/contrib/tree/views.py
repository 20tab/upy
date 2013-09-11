from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from upy.contrib.tree.utility import UPYRobotTXT, UPYSitemap


def upy_render(request, upy_context, vars_dictionary):
    """
    It renders template defined in upy_context's page passed in arguments
    """
    page = upy_context['PAGE']
    return render_to_response(page.template.file_name, vars_dictionary, context_instance=RequestContext(request))


def view_404(request, url=None):
    """
    It returns a 404 http response
    """
    res = render_to_response("404.html", {"PAGE_URL": request.get_full_path()},
                             context_instance=RequestContext(request))
    res.status_code = 404
    return res


def view_500(request, url=None):
    """
    it returns a 500 http response
    """
    res = render_to_response("500.html", context_instance=RequestContext(request))
    res.status_code = 500
    return res


def sitemap(request):
    """
    It returns sitemap.xml as http response
    """
    upysitemap = UPYSitemap(request)
    return HttpResponse(upysitemap._do_sitemap(), content_type="text/xml")


def robots(request):
    """
    It returns robots.txt as http response
    """
    upyrobottxt = UPYRobotTXT(request)
    return HttpResponse(upyrobottxt._do_robotstxt(), content_type="text")


def favicon(request):
    """
    It returns favicon's location
    """
    favicon = "/upy_static/images/favicon.ico"
    try:

        return HttpResponseRedirect(favicon)
    except:
        return HttpResponseRedirect(favicon)
