try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local
    
th_active = local()

def activate(publication):
    """
    Fetches the publication and installs it as the current 
    publication object for the current thread.
    """
    th_active.value = publication

def deactivate():
    """
    Deinstalls the currently active publication object
    """
    if hasattr(th_active, "value"):
        del th_active.value
        
def get_publication():
    """
    Returns the currently selected publication.
    """
    try:
        return getattr(th_active,'value',None)
    except Exception, e:
        raise e
