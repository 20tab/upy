from django.template import RequestContext
from django.template.loader import render_to_string

class ChangeLangMod(object):
    """
    ChangeLangMod is a module used to create a form to change language in your browser. Constructor accepts following parameters:
    - request
    - type_as, a string included in one of this: as_select, as_string, as_flag. This chooses the right template.
    - publication
    - separator: a string used to separate languages in form.
    """
    def __init__(self, request, type_as, publication, separator = None,redirect_to=None, current_disabled = True):
        if type_as in ['as_select', 'as_string', 'as_flag']:
            self.request = request
            self.type_as = type_as # one of this: as_select, as_string, as_flag
            self.publication = publication
            self.separator = separator
            self.redirect_to = redirect_to
            self.current_disabled = current_disabled
        else:
            raise ValueError('Error in upy.contrib.language.ChangeLangMod. type_as "%s" is not found in __init__ function' % type_as)

    def get_form(self):
        """
        It returns a string, that represent a form, to print in your template.
        """
        languages = self.publication.languages.all()
        return render_to_string("language_%s.html" % self.type_as, 
                                    {"mod":self,
                                     "languages": languages}, 
                                    context_instance=RequestContext(self.request))
        
        
