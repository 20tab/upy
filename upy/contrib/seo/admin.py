from django.contrib import admin
from upy.contrib.seo.models import TransSite, TransNode, TransPage
from upy.contrib.tabbed_translation.admin import TransAdmin


class TransSiteAdmin(TransAdmin):
    """
    This is the option class for PublicationG11n Admin
    """
    list_display = ('title', 'author',)
    list_filter = ('author',)
    save_on_top = True
    fieldsets = (
        ('', {'fields': ('default',)}),
        ('', {'fields': (
            ('title', 'description'), ('keywords', 'author'),
            ('content_type','robots'),
            ('generator', ),),
            'classes': ('trans-fieldset',)},),
    )


class TransNodeAdmin(TransAdmin):
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


class TransPageAdmin(TransAdmin):
    """
    This is the option class for PageG11n Admin
    """
    list_display = ('page',)
    list_per_page = 100
    fieldsets = (('', {'fields': ('page',)}), ('', {
        'fields': (
            ('title', 'description'), ('keywords', 'author'),
            ('content_type', 'robots'),),
        'classes': ('trans-fieldset',), }))
    save_on_top = True


admin.site.register(TransSite, TransSiteAdmin)
admin.site.register(TransNode, TransNodeAdmin)
admin.site.register(TransPage, TransPageAdmin)