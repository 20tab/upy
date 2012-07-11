"""
Contains the WSGI middleware that controls if project runs in MULTI_DOMAIN mode
"""
import django.core.handlers.wsgi
from django.template.defaultfilters import slugify
from django.conf import settings
from django.core import urlresolvers 

djangoapp = django.core.handlers.wsgi.WSGIHandler()

def application(env, start_response):
    if settings.MULTI_DOMAIN:
        host = env['HTTP_HOST']
        path = env['PATH_INFO']
        if _is_valid_path("/"+slugify(host) + path):
            env['PATH_INFO'] = "/" +slugify(host) + path
        elif _is_valid_path("/"+slugify(host) + path + "/"):
            env['PATH_INFO'] = "/" +slugify(host) + path + "/"
    return djangoapp(env,start_response)


#se multidomain aggiunge prima dello slug lo slugify dell'url della pubblicazione
#modificare url del templatetags e reverse per le viste con il monkey patching


def _is_valid_path(path, urlconf=None):
    """
    Returns True if the given path resolves against the default URL resolver,
    False otherwise.

    This is a convenience method to make working with "is this a match?" cases
    easier, avoiding unnecessarily indented try...except blocks.
    """
    try:
        urlresolvers.resolve(path, urlconf)
        return True
    except urlresolvers.Resolver404:
        return False