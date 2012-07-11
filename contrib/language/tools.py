from django.template import RequestContext
from django.template.loader import render_to_string

class ChangeLangMod(object):
    def __init__(self, request, type_as, publication, separator = None):
        self.request = request
        self.type_as = type_as # one of this: as_select, as_string, as_flag
        self.publication = publication
        self.separator = separator
        
    def get_form(self):
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
        
        
