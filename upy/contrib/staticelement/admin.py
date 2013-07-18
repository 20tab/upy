from django.contrib import admin
from django.conf import settings
from upy.contrib.staticelement import models as se_models
from upy.contrib.cked.widgets import CKEditorWidget
from django import forms
from upy.contrib.g11n.admin import G11nAdmin,G11nStackedInlineAdmin

STATICELEMENT_CKE_CONFIG = None
if settings.STATICELEMENT_CKE_CONFIG:
    STATICELEMENT_CKE_CONFIG = settings.STATICELEMENT_CKE_CONFIG

class StaticElementCategoryAdmin(admin.ModelAdmin):
    """
    Admin's options for StaticElementCategory model
    """
    list_display = ('name',)

class CKEditorFormMC(forms.ModelForm):
    """
    It's add a CKEditor widget to textarea fields
    """
    html = forms.CharField(
        widget=CKEditorWidget(config=STATICELEMENT_CKE_CONFIG)
    )
    class Meta:
        model = se_models.StaticElement
class StaticElementG11nAdmin(G11nAdmin):
    """
    Admin's options for StaticElementG11n model
    """
    list_display = ('id','alias', 'language')
    list_display_links = ['id']
    list_editable = ('alias','language',)
    list_filter = ('language',)
    fieldsets = (('', {'fields': 
                       ('alias', 'html',),
        },),) + G11nAdmin.fieldsets

class StaticElementG11nInline(G11nStackedInlineAdmin):
    """
    Admin's options for StaticElementG11n model used inline
    """
    fieldsets = (('', {'fields': 
                       ('alias', 'html'),
        },),) + G11nAdmin.fieldsets

class StaticElementG11nBaseAdmin(admin.ModelAdmin):
    """
    Admin's options for StaticElement model
    """
    list_display = ('name',)
    list_display_link = ('name',)
    save_on_top = True
  
class CKEditorForm(forms.ModelForm):
    html = forms.CharField(
        widget=CKEditorWidget(config=STATICELEMENT_CKE_CONFIG)
    )

class StaticElementAdmin(admin.ModelAdmin):
    """
    Admin's options for StaticElementCategory model
    """
    list_display = ('name','alias')
    list_display_link = ('name',)
    list_editable = ('alias',)
    fieldsets = (('', {'fields': 
                       (('name',),('alias',),('html',)),
        },),)
    save_on_top = True
        
        
        


