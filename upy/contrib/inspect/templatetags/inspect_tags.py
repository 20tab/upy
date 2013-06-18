from django.template import Library

register = Library()

@register.filter
def inspect_doc(model,field):
    try:
        func = getattr(model,field,None)
        return func.__doc__
    except:
        return ""