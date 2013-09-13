from django.conf import settings

if settings.USE_UPY_SEO and len(settings.LANGUAGES) > 1:
    from modeltranslation.translator import translator, TranslationOptions
    from upy.contrib.seo.models import MetaSite, MetaNode, MetaPage

    class SiteTranslationOptions(TranslationOptions):
        fields = ('title', 'description', 'keywords', 'author', 'content_type', 'robots', 'generator')

    class NodeTranslationOptions(TranslationOptions):
        fields = ('alias', 'title')

    class PageTranslationOptions(TranslationOptions):
        fields = ('title', 'description', 'keywords', 'author', 'content_type', 'robots')

    translator.register(MetaSite, SiteTranslationOptions)
    translator.register(MetaNode, NodeTranslationOptions)
    translator.register(MetaPage, PageTranslationOptions)