from django.core.urlresolvers import resolve, Resolver404
from django.conf.urls import handler404
from django.utils.importlib import import_module

class SetUpyContextMiddleware(object):
    """
    This middleware activates current publication in current thread.
    In process_response it deactivates current publication.
    """
    def process_request(self, request):
        try:
            match = resolve(request.path)
        except Resolver404:
            match = None
            try:
                return import_module(handler404)
            except:
                pass
        if match and 'upy_context' in match.kwargs:
            request.upy_context = match.kwargs['upy_context']
