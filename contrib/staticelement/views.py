from django.template import RequestContext
from django.template.loader import render_to_string

def render_staticelement(request, staticelement, use_alias = False, use_html = True, tag_header = u'div', class_header = u'section_head',tag_alias = u'h2', tag_content = u'div', class_content = u'section_content'):
    """
    It renders staticelement passed in arguments and returns a html string
    """
    try:
        staticelement = staticelement.g11n
        return render_to_string("upy_staticelement.html", {"staticelement": staticelement,
                                                    "use_alias": use_alias,
                                                    "use_html": use_html,
                                                    "tag_header": tag_header,
                                                    "class_header": class_header,
                                                    "tag_alias": tag_alias,
                                                    "tag_content": tag_content,
                                                    "class_content": class_content}, 
                             context_instance=RequestContext(request))
    except:
        return _(u"The static element with the name '%s' don't have a g11n instance. Add it." % staticelement.name)