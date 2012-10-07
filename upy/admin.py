"""
Contains some classes to extend ModelAdmin, with some other functionalities
"""
from django.contrib import admin

class ButtonLink(object):
    """
    It defines a button that you can locate near the history button in change_form.html as a link
    """
    def __init__(self, short_description, link, css_id=None, css_class=None):
        """
        Use it to create a ButtonableLink. It takes following parameters:
        'short_description' is what you want display in this link,
        'link' is the value of this link,
        'css_id' is the id selector,
        'css_class' is the class selector
        """
        self.short_description = short_description
        self.link = link
        self.css_id = css_id
        self.css_class = css_class
        
class ButtonForm(object):
    """
    It defines a button that you can locate near the history button in change_form.html as a form
    """
    def __init__(self, name, submit_value, form_action, input_dict, form_method="post", css_class=None):
        """
        Use it to create a ButtonableForm. It takes following parameters:
        'name' is the form's name,
        'submit_value' is the button's value,
        'form_action' is the form's action,
        'form_method' is the form's method,
        'css_class' is the class selector
        """
        self.name = name
        self.submit_value = submit_value
        self.form_action = form_action
        self.form_method = form_method
        self.input_dict = input_dict  #{'name':'value',}
        self.css_class = css_class
        
class ButtonableModelAdmin(admin.ModelAdmin):
    """
    Use this admin only if you want apply custom button on the change_form template in admin panel.
    """
    buttons_link=[]
    buttons_form=[]
    def change_view(self, request, object_id, form_url = '',extra_context={}): 
        """
        It adds ButtonLinks and ButtonForms to extra_context used in the change_form template
        """
        extra_context['buttons_link']=self.buttons_link
        extra_context['buttons_form']=self.buttons_form
        extra_context['button_object_id']=object_id  
        return super(ButtonableModelAdmin, self).change_view(request, object_id, form_url,extra_context)
    
class HiddenModelAdmin(admin.ModelAdmin):
     def get_model_perms(self, *args, **kwargs):
        perms = admin.ModelAdmin.get_model_perms(self, *args, **kwargs)
        perms['list_hide'] = True
        return perms