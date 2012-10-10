from upy.contrib.g11n.models import Language,Publication

def getDefaultLanguage():
    """
    Get default language and return the tuple to use in the settings.py, DEFAULT_LANGUAGES
    """
    try:
        publication = Publication.objects.get(is_default="default")
        if publication and publication.default_language:
            return publication.default_language
        return None
    except:
        return None
    
def getLanguageList():
    """
    This function get the Language List from the DB and return the tuple to
    use in the settings.py, LANGUAGES
    """
    language_list = Language.objects.all()
    return_list = []
    for language in language_list:
        return_list.append((language.code, language.name))
    return return_list