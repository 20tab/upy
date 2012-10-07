from upy.contrib.tree.views import view_page_disable, view_publication_disable
from django.http import HttpResponseRedirect
import re
from project import urls as my_urls
from django.conf import settings 
from django.template.defaultfilters import slugify            

class EnabledMiddleware(object):
    """
    This middleware checks if the page requested is enabled. If it's disabled then
    return a disabled view
    """
    def process_request(self,request):
        if not request.is_ajax() and hasattr(request,'upy_context'):
            publication = request.upy_context['PUB_EXTENDED'].publication
            if (publication and not publication.enabled) or (publication and publication.g11n and not publication.g11n.enabled):
                return view_publication_disable(request,publication.g11n.disabled_message)
            page = request.upy_context['PAGE']
            if page and page.g11n and not page.g11n.enabled:
                return view_page_disable(request,page.g11n.disabled_message)
    

                   
class RequireLoginMiddleware(object):
    """
    This middleware checks if current page is protected by login 
    """
    def __init__(self):
        self.urls = tuple([re.compile(url) for url in my_urls.LOGIN_REQUIRED_URLS])
        self.require_login_path = getattr(settings, 'LOGIN_URL', '/accounts/login/')
    
    def process_request(self, request):
        for url in self.urls:
            if url.match(request.path[1:]) and request.user.is_anonymous():
                path = request.path
                if settings.MULTI_DOMAIN:
                    host = slugify(request.get_host())
                    path = path.replace("/%s" % host,"")
                return HttpResponseRedirect('%s?next=%s' % (self.require_login_path, path))