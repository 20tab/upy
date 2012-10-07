"""
Contains some common filter as utilities
"""
from django.template import Library
register = Library()

@register.filter
def euro(value):
    """
    Transforms a number in euro format
    """
    try:
        val = u"%.2f" % (float(value))
    except:
        return u''
    return val.replace('.', ',')

@register.filter
def comma2dot(value):
    """
    Replaces comma with dot in a string
    """
    val = unicode(value).split()
    if not val:
        return value
    return val[0].replace(',', '.')