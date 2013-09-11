from upy.contrib.seo.models import TransPage, TransSite


class MetaContent(object):
    """
    MetaContent class define an object that contain informations about page or publication. 
    These informations are included in template.
    """

    def __init__(self):
        self.title = ""
        self.description = ""
        self.keywords = ""
        self.author = ""
        self.content_type = ""
        self.robots = ""
        self.generator = ""

    def fill_content(self, metaObject):
        """
        This method fills MetaContent with informations contained in metaObjetc
        """
        self.title = metaObject.title
        self.description = metaObject.description
        self.keywords = metaObject.keywords
        self.author = metaObject.author
        self.content_type = metaObject.content_type
        self.robots = metaObject.robots
        try:#perche' Page non ha generator
            self.generator = metaObject.generator
        except:
            self.generator = ''

    def check_attr(self, item):
        """
        It checks if item is defined in self object
        """
        if hasattr(self, item):
            if not getattr(self, item) or getattr(self, item) == "":
                return False
        return True

    def jsonToMeta(self, json):
        """
        It sets all item in a json to self
        """
        for k, v in json.items():
            setattr(self, k, v)

    def get_fields(self):
        """
        It returns this object as a dictionary
        """
        return self.__dict__

    def __str__(self):
        return "%s" % self.title


def set_meta(request):
    """
    This context processor returns meta informations contained in cached files. 
    If there aren't cache it calculates dictionary to return
    """
    context_extras = {}
    if not request.is_ajax() and hasattr(request, 'upy_context') and request.upy_context['PAGE']:
        try:
            site = TransSite.objects.get(default=True)
        except TransSite.DoesNotExist:
            site = None
        try:
            page = TransPage.objects.get(page=request.upy_context['PAGE'])
        except TransPage.DoesNotExist:
            page = None
        meta_temp = MetaContent()
        attr_list = ('title', 'description', 'keywords', 'author', 'content_type', 'robots', 'generator',)
        if page :
            for item in attr_list:
                if hasattr(page, item):
                    setattr(meta_temp, item, getattr(page, item))
        if site:
            for item in attr_list:
                if hasattr(site, item) and not meta_temp.check_attr(item):
                    setattr(meta_temp, item, getattr(site, item))
        context_extras['META'] = meta_temp
    return context_extras
