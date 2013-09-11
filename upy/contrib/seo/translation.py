from modeltranslation.translator import translator, TranslationOptions
from upy.contrib.seo.models import TransSite, TransNode, TransPage


class SiteTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'keywords', 'author', 'content_type', 'robots', 'generator')


class NodeTranslationOptions(TranslationOptions):
    fields = ('alias', 'title')


class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'keywords', 'author', 'content_type', 'robots')

translator.register(TransSite, SiteTranslationOptions)
translator.register(TransNode, NodeTranslationOptions)
translator.register(TransPage, PageTranslationOptions)