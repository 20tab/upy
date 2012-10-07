from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from upy.contrib.tree.utility import UPYRobotTXT,UPYSitemap
from upy.contrib.g11n.models import Publication,get_current_publication
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.utils import simplejson


def upy_render(request, upy_context, vars_dictionary):
    """
    It renders template defined in upy_context's page passed in arguments
    """
    page = upy_context['PAGE']
    return render_to_response(page.template.file_name, vars_dictionary, context_instance=RequestContext(request))

def view_404(request, url = None):
    """
    It returns a 404 http response
    """
    return render_to_response("404.html", {"PAGE_URL": request.get_full_path()},context_instance=RequestContext(request))

def view_500(request, url = None):
    """
    it returns a 500 http response
    """
    return render_to_response("500.html", context_instance=RequestContext(request))
    
def view_page_disable(request,message):
    """
    If a page is disabled it renders a disabled message template
    """
    return render_to_response("page_disabled.html", {'message':message},context_instance=RequestContext(request))
def view_publication_disable(request,message):
    """
    If publication is disabled it renders publication_disabled.html template
    """
    return render_to_response("publication_disabled.html", {'message':message}, context_instance=RequestContext(request))

def sitemap(request):
    """
    It returns sitemap.xml as http response
    """
    upysitemap = UPYSitemap(request)
    return HttpResponse(upysitemap._do_sitemap(), content_type = "text/xml")

def robots(request):
    """
    It returns robots.txt as http response
    """
    upyrobottxt = UPYRobotTXT(request)
    return HttpResponse(upyrobottxt._do_robotstxt(), content_type = "text")


def favicon(request):
    """
    It returns favicon's location
    """
    favicon = "/upy_static/images/favicon.ico"
    try:
        publication = get_current_publication()
        if publication.favicon:
            favicon = publication.favicon
            if favicon.__class__.__name__ == "FieldFile":
                favicon = favicon.url
        return HttpResponseRedirect(favicon)
    except:
        return HttpResponseRedirect(favicon)
    
    
@csrf_protect
def render_page(request):
    """
        TO DO
    """
    raise ValueError("UPY_ROUTING not implemented. Implement this view or set USE_UPY_ROUTING = False in config.py")
"""
    try:
        publication = request.upy_context['PUBLICATION']
        page = request.upy_context['PAGE']
        node = request.upy_context['NODE']
        app = __import__("%s.%s" % (page.view.app_name,page.view.module_name))
        
        if hasattr(app, page.view.module_name):
            view = getattr(app, page.view.module_name)
            if hasattr(view, page.view.func_name):
                abs_url = node.absolute_url(publication)
                url = replace(abs_url[0],page.regex,"")
                value_regex = replace(request.get_full_path(),url,"")
                arguments = [request,page.template.file_name]
                if value_regex:
                    arguments.append(value_regex)
                elif page.regex and page.regex[-1] == "*":
                    arguments.append(None)
                if page.static_vars:
                    del page.static_vars["template_name"]
                    for static in page.static_vars.values():
                        arguments.append(static)
                return getattr(view, page.view.func_name)(*arguments)
        
    except Exception,e:
        print e
        return view_404(request)
"""
@csrf_exempt    
def get_languages(request):
    """
    It returns all languages enabled in this project as a list of dictionaries in a json data
    """
    if request.is_ajax():
        publications = Publication.objects.all()
        language_list = []
        for pub in publications:
            languages = pub.languages.all()
            for lang in languages:
                language_list.append({"pub": pub.pk,"pub_name":pub.name,"lang": u"%s" % lang.pk,"name_lang":lang.alias})
        data = simplejson.dumps(language_list)
        return HttpResponse(data)