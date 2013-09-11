def set_meta(request):
    """
    This context processor returns meta informations contained in cached files. 
    If there aren't cache it calculates dictionary to return
    """
    context_extras = {}
    if not request.is_ajax() and hasattr(request, 'upy_context') and request.upy_context['PAGE']:
        context_extras['PAGE'] = request.upy_context['PAGE']
        context_extras['NODE'] = request.upy_context['NODE']
    return context_extras
