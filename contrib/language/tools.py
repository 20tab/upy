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
    def __init__(self, request, type_as, publication, separator = None):
        if type_as in ['as_select', 'as_string', 'as_flag']:
            self.request = request
            self.type_as = type_as # one of this: as_select, as_string, as_flag
            self.publication = publication
            self.separator = separator
        else:
            raise ValueError('Error in upy.contrib.language.ChangeLangMod. type_as "%s" is not found in __init__ function' % type_as)

    def get_form(self):
        """
        It returns a string, that represent a form, to print in your template.
        """
        if self.type_as == u"as_flag":
            languages = self.publication.languages.all()
            return render_to_string("language_%s.html" % self.type_as, 
                                    {"separator": self.separator,
                                     "languages": languages}, 
                                    context_instance=RequestContext(self.request))
        else:
            return render_to_string("language_%s.html" % self.type_as, 
                                    {"separator": self.separator}, 
                                    context_instance=RequestContext(self.request))
        
        
