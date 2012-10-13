from upy.contrib.staticpage.models import StaticPage
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

def render_staticpage(request, upy_context, use_alias = False, use_html = True, tag_header = u'div', class_header = u'section_head',tag_alias = u'h2', tag_content = u'div', class_content = u'section_content'):
    """
    It renders staticpage included in upy_context and returns a html string
    """
    try:
        staticpage = StaticPage.g11nobjects.get(page=upy_context['PAGE']) 
        return render_to_string("upy_staticpage.html", {"staticpage": staticpage,
                                            "use_alias": use_alias,
                                            "use_html": use_html,
                                            "tag_header": tag_header,
                                            "class_header": class_header,
                                            "tag_alias": tag_alias,
                                            "tag_content": tag_content,
                                            "class_content": class_content}, 
                     context_instance=RequestContext(request))
    except:
        return _(u"Static page with the name '%s' not found in database. Add it." % upy_context['PAGE'].slug)
    