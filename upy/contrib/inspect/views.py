from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db import models
from upy.contrib.inspect.utils import InspectModel
from upy.contrib.g11n.models import G11nBase


@login_required
def browse(request):
    apps = []
    for ap in models.get_apps():
        item = {
                'name':ap.__name__.replace('.models',''),
                'value': ap.__name__,
                'models':[u"%s" % model.__name__ for model in models.get_models(ap)],
                'class':ap.__name__.replace('.models','').replace('.','-')
                }
        apps.append(item) 
    
    model_res = g11n_model = display_as = app = None
    if request.POST:
        model_name=request.POST['model'].replace('.models','')
        app = '.'.join(request.POST['model'].split('.')[:-1])
        model = models.get_model(model_name.split('.')[-2],model_name.split('.')[-1])
        model_res = InspectModel(model)
        display_as = request.POST['display_as']
        
        if issubclass(model,G11nBase):
            g11n_model = model.G11nMeta.g11n
        
    if request.user.is_superuser:
        return render_to_response('upy_inspect_browse.html',
                                  {'apps':apps,
                                   'model':model_res,
                                   'g11n_model':g11n_model,
                                   'display_as':display_as,
                                   'app':app},
                          context_instance=RequestContext(request))
    raise Http404