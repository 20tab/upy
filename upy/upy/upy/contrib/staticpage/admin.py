from django.contrib import admin
from django.conf import settings
from upy.contrib.g11n.admin import G11nAdmin,G11nStackedInlineAdmin
from upy.contrib.staticpage.models import StaticPage, StaticPageG11n, StaticPageCategory
from upy.contrib.ckeditor.widgets import CKEditorWidget
from django import forms

STATICPAGE_CKE_CONFIG = None
if settings.STATICPAGE_CKE_CONFIG:
    STATICPAGE_CKE_CONFIG = settings.STATICPAGE_CKE_CONFIG


class CKEditorForm(forms.ModelForm):
    """
    It's add a CKEditor widget to textarea fields
    """
    html = forms.CharField(
        widget=CKEditorWidget(config=STATICPAGE_CKE_CONFIG)
    )
    class Meta:
        model = StaticPageG11n

class StaticPageG11nOption(G11nAdmin):
    """
    Admin's options for StaticPageG11n model
    """
    list_display = ('id','alias', 'staticpage', 'language')
    list_display_links = ['id']
    list_editable = ('alias','language',)
    list_filter = ('language',)
    fieldsets = (('', {'fields': 
                       ('alias', 'html',),
        },),) + G11nAdmin.fieldsets
    form = CKEditorForm
    class Meta:
        model = StaticPageG11n

class StaticPageG11nInline(G11nStackedInlineAdmin):
    """
    Admin's options for StaticPageG11n model used inline
    """
    fieldsets = (('', {'fields': 
                       ('alias', 'html'),
        },),) + G11nAdmin.fieldsets
    model = StaticPageG11n
    form = CKEditorForm

class StaticPageOption(admin.ModelAdmin):
    """
    Admin's options for StaticPage model
    """
    
    list_display = ('page','category',)
    list_display_link = ('page',)
    list_editable = ('category',)
    list_filter = ('category',)
    inlines = [StaticPageG11nInline,]
    save_on_top = True
    class Meta:
        model = StaticPage

class StaticPageCategoryOption(admin.ModelAdmin):
    """
    Admin's options for StaticPageCategory model
    """
    list_display = ('name',)
    class Meta:
        model = StaticPageCategory 
        
        
admin.site.register(StaticPage, StaticPageOption)
#admin.site.register(StaticPageG11n, StaticPageG11nOption)
admin.site.register(StaticPageCategory, StaticPageCategoryOption)

