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


@register.filter
def uRange(value):
    """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|uRange %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    """
    return xrange( value )