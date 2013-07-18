from django.contrib import admin
from django.conf import settings
from upy.contrib.g11n.admin import G11nAdmin,G11nStackedInlineAdmin
from upy.contrib.cked.widgets import CKEditorWidget
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
    

class StaticPageG11nAdmin(G11nAdmin):
    """
    Admin's options for StaticPageG11n model
    """
    list_display = ('id','alias', 'language')
    list_display_links = ['id']
    list_editable = ('alias','language',)
    list_filter = ('language',)
    fieldsets = (('', {'fields': 
                       ('alias', 'html',),
        },),) + G11nAdmin.fieldsets
    

class StaticPageG11nInline(G11nStackedInlineAdmin):
    """
    Admin's options for StaticPageG11n model used inline
    """
    fieldsets = (('', {'fields': 
                       ('alias', 'html'),
        },),) + G11nAdmin.fieldsets

class StaticPageAdmin(admin.ModelAdmin):
    """
    Admin's options for StaticPage model
    """
    
    list_display = ('page',)
    list_display_link = ('page',)
    save_on_top = True


class StaticPageCategoryAdmin(admin.ModelAdmin):
    """
    Admin's options for StaticPageCategory model
    """
    list_display = ('name',)