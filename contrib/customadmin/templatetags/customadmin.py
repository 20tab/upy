from django.template import Library
from upy.contrib.customadmin.models import CustomApp

register = Library()

@register.filter
def add_app_icons(app_list, autocomplete):
    """
    It returns a list of applications to view in admin's interface (index.html). This filter is called only if you want view
    icons mode.
    """
    app_icon_list = CustomApp.objects.all()
    app_list_ok = []
    
    for appicon in app_icon_list:
        try:
            app_temp = [x for x in app_list if x.get('name').lower() == appicon.application.lower()][0]
            app_temp['image'] = appicon.image
            app_temp['verbose_app_name'] = appicon.verbose_app_name
            app_list_ok.append(app_temp)
            #app_list_ok.extend([x for x in app_list if x.get('name') == appicon.application])
        except IndexError, e:
            print "Error in customadmin.templatetags.add_app_icons: ", e, "; application: ", appicon.application
            pass # probabilmente e' stata inserita nella lista di applicazioni con icona una applicazione
                    # che non e' tra quelle registrate nell'admin, quindi poco male...
      
    if autocomplete:  
        app_list_ok_name = [x.get('name') for x in app_list_ok]
        app_list_name = [x.get('name') for x in app_list]
        app_out_name = list(set(app_list_name)-set(app_list_ok_name)) 
        app_out_list = [x for x in app_list if x.get('name') in app_out_name]
        
        for app_out in app_out_list:
            app_out['image'] = None
            app_out['verbose_app_name'] = app_out.get('name')
        
        app_list_ok.extend(app_out_list)
        
    return app_list_ok


@register.filter
def custom_app_list(app_list, autocomplete):
    """
    It returns a list of applications chosen to view in admin's interface (index.html).
    """
    app_icon_list = CustomApp.objects.all()
    app_list_ok = []
    
    for appicon in app_icon_list:
        try:
            app_temp = [x for x in app_list if x.get('name').lower() == appicon.application.lower()][0]
            app_temp['show_models'] = appicon.show_models
            app_temp['verbose_app_name'] = appicon.verbose_app_name
            app_list_ok.append(app_temp)
            #app_list_ok.extend([x for x in app_list if x.get('name') == appicon.application])
        except IndexError, e:
            print "Error in customadmin.templatetags.add_app_icons: ", e, "; application: ", appicon.application
            pass # probabilmente e' stata inserita nella lista di applicazioni con icona una applicazione
            # che non e' tra quelle registrate nell'admin, quindi poco male...
    
    if autocomplete:
        app_list_ok_name = [x.get('name') for x in app_list_ok]
        app_list_name = [x.get('name') for x in app_list]
        app_out_name = list(set(app_list_name)-set(app_list_ok_name)) 
        app_out_list = [x for x in app_list if x.get('name') in app_out_name]
        
        for app_out in app_out_list:
            app_out['show_models'] = True
            app_out['verbose_app_name'] = app_out.get('name')
    
        app_list_ok.extend(app_out_list)
       
    return app_list_ok
