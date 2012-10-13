from django.contrib import admin
from django.conf import settings
from upy.contrib.staticelement import models as se_models
from upy.contrib.ckeditor.widgets import CKEditorWidget
from django import forms
from project import config

STATICELEMENT_CKE_CONFIG = None
if settings.STATICELEMENT_CKE_CONFIG:
    STATICELEMENT_CKE_CONFIG = settings.STATICELEMENT_CKE_CONFIG

class StaticElementCategoryOption(admin.ModelAdmin):
    """
    Admin's options for StaticElementCategory model
    """
    list_display = ('name',)
    class Meta:
        model = se_models.StaticElementCategory

if config.USE_UPY_G11N:
    from upy.contrib.g11n.admin import G11nAdmin,G11nStackedInlineAdmin
    class CKEditorFormMC(forms.ModelForm):
        """
        It's add a CKEditor widget to textarea fields
        """
        html = forms.CharField(
            widget=CKEditorWidget(config=STATICELEMENT_CKE_CONFIG)
        )
        class Meta:
            model = se_models.StaticElementG11n
    class StaticElementG11nOption(G11nAdmin):
        """
        Admin's options for StaticElementG11n model
        """
        list_display = ('id','alias', 'staticelement', 'language')
        list_display_links = ['id']
        list_editable = ('alias','language',)
        list_filter = ('language',)
        fieldsets = (('', {'fields': 
                           ('alias', 'html',),
            },),) + G11nAdmin.fieldsets
        form = CKEditorFormMC
        class Meta:
            model = se_models.StaticElementG11n
    
    class StaticElementG11nInline(G11nStackedInlineAdmin):
        """
        Admin's options for StaticElementG11n model used inline
        """
        fieldsets = (('', {'fields': 
                           ('alias', 'html'),
            },),) + G11nAdmin.fieldsets
        model = se_models.StaticElementG11n
        form = CKEditorFormMC
    
    class StaticElementOption(admin.ModelAdmin):
        """
        Admin's options for StaticElement model
        """
        list_display = ('name','category')
        list_display_link = ('name',)
        list_editable = ('category',)
        list_filter = ('category',)
        inlines = [StaticElementG11nInline,]
        save_on_top = True
        class Meta:
            model = se_models.StaticElement
    
    #admin.site.register(se_models.StaticElementG11n, StaticElementG11nOption)
else:
    
    class CKEditorForm(forms.ModelForm):
        html = forms.CharField(
            widget=CKEditorWidget(config=STATICELEMENT_CKE_CONFIG)
        )
        class Meta:
            model = se_models.StaticElement
    
    class StaticElementOption(admin.ModelAdmin):
        """
        Admin's options for StaticElementCategory model
        """
        list_display = ('name','alias','category')
        list_display_link = ('name',)
        list_editable = ('alias','category',)
        list_filter = ('category',)
        fieldsets = (('', {'fields': 
                           (('name',),('alias',),('html',)),
            },),)
        save_on_top = True
        form = CKEditorForm
        class Meta:
            model = se_models.StaticElement
        
        
admin.site.register(se_models.StaticElement, StaticElementOption)
admin.site.register(se_models.StaticElementCategory, StaticElementCategoryOption)

