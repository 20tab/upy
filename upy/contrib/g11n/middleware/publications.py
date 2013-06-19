from upy.contrib.g11n.g11n_threading import deactivate,activate
from django.core.urlresolvers import resolve,Resolver404
from django.conf.urls import handler404
from django.utils.importlib import import_module
from upy.contrib.g11n.models import Publication
from django.conf import settings

class SetCurrentPublicationMiddleware(object):
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
            current_publication = match.kwargs['upy_context']['PUB_EXTENDED'].publication 
            #Se la richiesta arriva da un nodo di tree allora prendo la corrente
            activate(current_publication)
            request.upy_context = match.kwargs['upy_context']
        elif match:
            try:
                current_publication = Publication.objects.select_related().get(url = request.get_host())
            except Publication.DoesNotExist:
                if not settings.MULTI_DOMAIN:
                    try:
                        current_publication = Publication.objects.select_related().get(default=True)
                    except Publication.DoesNotExist:
                        current_publication = None
                else:
                    current_publication = None
            activate(current_publication)
            
        

    def process_response(self, request, response):
        try:
            match = resolve(request.path)
        except Resolver404:
            pass
        else:
            if match and 'upy_context' in match.kwargs:
                deactivate()
        return response