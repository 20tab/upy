from django.template import Library
from upy.contrib.highlighter import Highlighter
from django.utils.html import strip_tags

register = Library()

@register.filter
def highlight(text, q, max_length = 200, nchars_before = 0):
    text = strip_tags(text)
    highlight = Highlighter(q,max_length=max_length)
    return highlight.highlight(text,nchars_before=nchars_before)
