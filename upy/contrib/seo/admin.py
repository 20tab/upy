from django.contrib import admin
from upy.contrib.seo.models import MetaSite, MetaNode, MetaPage
from django.conf import settings

if settings.USE_UPY_SEO and len(settings.LANGUAGES) > 1:
    from upy.contrib.tabbed_translation.admin import TransAdmin as MetaAdmin
else:
    MetaAdmin = admin.ModelAdmin


class MetaSiteAdmin(MetaAdmin):
    """
    This is the option class for PublicationG11n Admin
    """
    list_display = ('title', 'author',)
    list_filter = ('author',)
    save_on_top = True
    fieldsets = (
        ('', {'fields': ('default', 'favicon')}),
        ('', {'fields': (
            ('title', 'description'), ('keywords', 'author'),
            ('content_type', 'robots'),
            ('generator', ), ('html_head',)),
            'classes': ('trans-fieldset',)},),
    )


class MetaNodeAdmin(MetaAdmin):
    """
    This is the option class for NodeG11n Admin
    """
    list_display = ('alias', 'title', 'node',)
    list_editable = ('title', 'node',)
    list_per_page = 100
    fieldsets = (
        ('', {'fields': ('node',)}),
        ('', {
            'fields': (('alias', 'title'),),
            'classes': ('trans-fieldset',)
        }),
    )
    save_on_top = True


class MetaPageAdmin(MetaAdmin):
    """
    This is the option class for PageG11n Admin
    """
    list_display = ('page',)
    list_per_page = 100
    fieldsets = (('', {'fields': ('page',)}), ('', {
        'fields': (
            ('title', 'description'), ('keywords', 'author'),
            ('content_type', 'robots'), ('html_head',)),
        'classes': ('trans-fieldset',), }))
    save_on_top = True


admin.site.register(MetaSite, MetaSiteAdmin)
admin.site.register(MetaNode, MetaNodeAdmin)
admin.site.register(MetaPage, MetaPageAdmin)