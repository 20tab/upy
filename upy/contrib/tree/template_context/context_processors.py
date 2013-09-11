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
        page = request.upy_context['PAGE']
        node = request.upy_context['NODE']
        context_extras['PAGE'] = page
        context_extras['NODE'] = node
        pub_extended = request.upy_context['PUB_EXTENDED']
        context_extras['PUBLICATION'] = pub_extended.publication

        publication = pub_extended.publication

        context_extras['ROOT'] = pub_extended.root

        try:
            context_extras['ROOT'] = pub_extended.root

        except Exception, e:
            print "Error in %s: %s" % (__file__, e)
        finally:
            if page:
                meta_temp = MetaContent()

                if not page.g11n and not publication.g11n:
                    context_extras['META'] = "Error: No Meta Content Available."
                elif page.g11n is None:
                    meta_temp.fill_content(publication.g11n)
                    context_extras['META'] = meta_temp
                elif publication.g11n is None:
                    meta_temp.fill_content(page.g11n)
                    context_extras['META'] = meta_temp
                else:
                    attr_list = ('title', 'description', 'keywords', 'author', 'content_type', 'robots', 'generator',)

                    for item in attr_list:
                        if hasattr(page.g11n, item):
                            setattr(meta_temp, item, getattr(page.g11n, item))

                    for item in attr_list:
                        if hasattr(publication.g11n, item) and not meta_temp.check_attr(item):
                            setattr(meta_temp, item, getattr(publication.g11n, item))

                context_extras['META'] = meta_temp

    return context_extras
