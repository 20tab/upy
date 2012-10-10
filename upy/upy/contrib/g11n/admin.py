from django.contrib import admin
from upy.contrib.g11n.models import _,PublicationG11n,Publication,Language
from django.forms.models import BaseInlineFormSet
from django.conf import settings


class G11nAdmin(admin.ModelAdmin):
    """
    Base Admin for G11n Models
    """
    fieldsets = ((_(u"Globalization"),{
                    'fields':(('publication','language'),),
                    'classes': ('collapse',)}),)
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "publication":
            if Publication.get_default():
                kwargs['initial'] = Publication.get_default().pk
        if db_field.name == "language":
            if Language.get_default():
                kwargs['initial'] = Language.get_default().pk
        return super(G11nAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
      

class CyclePublication(object):
    """
    It returns a list of tuples with all combinations made with languages and publications. 
    All G11nModel classes inherit an admin's form with prepopulated language and publications.
    """
    positions = {}
    
    def __init__(self, is_publication = False):
        cont = 0
        if is_publication:
            for lang in Language.objects.all():
                self.positions['%s' % cont] = (None,lang)
                cont = cont + 1
        else:
            for publication in Publication.objects.all():
                for lang in publication.languages.all():
                    self.positions['%s' % cont] = (publication,lang)
                    cont = cont + 1
        

class G11nInlineFormset(BaseInlineFormSet):
    """
    This is the formset inherited in G11nInlineModel classes
    """
    def __init__(self, data=None, files=None, instance=None,
                 save_as_new=False, prefix=None, queryset=None):
        
        super(G11nInlineFormset, self).__init__(data, files, instance,
                 save_as_new, prefix, queryset) 
        cycle_publications = CyclePublication(instance.__class__.__name__ == "Publication")
        cont = 0
        if not data and cycle_publications.positions:
            for form in self.forms:
                (publication, lang) = cycle_publications.positions['%s' % cont]
                
                if instance.__class__.__name__ != "Publication": 
                    form.fields['publication'].initial = publication
                form.fields['language'].initial = lang
                cont  = cont + 1
                form.empty_permitted = True
                     
            
class G11nStackedInlineAdmin(admin.StackedInline):
    """
    It defines a StackedInlineAdmin for all G11nModelInline
    """
    def __init__(self, parent_model, admin_site):
        super(G11nStackedInlineAdmin,self).__init__(parent_model, admin_site)
        if self.parent_model._meta.object_name == "Publication":
            max_num = Language.objects.count()
        else:
            max_num = 0
            for publication in Publication.objects.all():
                max_num += publication.languages.all().count()
        self.max_num = max_num
        self.extra = max_num

        
    formset = G11nInlineFormset
    template = "admin/g11n_tabs_stacked.html"
    class Media: 
        css = {"all" : ("/upy_static/css/upy-stacked-tabs.css",)}
        js = (settings.JQUERY_LIB,
              '/upy_static/js/upy-admin-g11ninline.js',
              '/upy_static/js/upy-admin-g11ntabsinline.js',
              )
        
class G11nTabularInlineAdmin(admin.TabularInline):
    """
    It defines a TabularInlineAdmin for all G11nModelInline
    """
    def __init__(self, parent_model, admin_site):
        super(G11nTabularInlineAdmin,self).__init__(parent_model, admin_site)
        if self.parent_model._meta.object_name == "Publication":
            max_num = Language.objects.count()
        else:
            max_num = 0
            for publication in Publication.objects.all():
                max_num += publication.languages.all().count()
        self.max_num = max_num
        self.extra = max_num

    formset = G11nInlineFormset
    class Media: 
        js = ('/upy_static/js/upy-admin-g11ninline.js',)
    
class PublicationG11nInline(G11nStackedInlineAdmin):
    """
    It's admin's options for inline PublicationG11nModel 
    """
    model = PublicationG11n
    fieldsets = (('', {'fields': 
                       (('title', 'description'),
                        ('keywords','author'),
                        ('content_type','enabled'),
                        ('disabled_message',),
                       ('robots','generator')),
        },),) + G11nAdmin.fieldsets
        
class PublicationOption(admin.ModelAdmin): 
    """
    This is the option class for Publication Admin
    """
    list_display = ('name','url','is_default') 
    list_editable = ('url','is_default') 
    list_filter = ('name', 'languages',)
    fieldsets = (('',{'fields': (('name','url','favicon'),),}),
                 (_('Checking'),{'fields': (('enabled', 'is_default'),),}),
                 (_('Languages'),{'fields': (( 'languages','default_language',),),}),)
    
    inlines = [PublicationG11nInline,]
    save_on_top = True
    class Meta: 
        model = Publication
    class Media: 
        js = (settings.JQUERY_LIB,
              '/upy_static/js/upy-admin-publication.js',)
        
class PublicationG11nOption(G11nAdmin): 
    """
    This is the option class for PublicationG11n Admin
    """
    list_display = ('title', 'author','enabled','publication','language') 
    list_filter = ('author', 'enabled',)
    save_on_top = True
    fieldsets = (('', {'fields': 
                       ('title', 'description','keywords','author',
                        'content_type','enabled','disabled_message',
                        'robots','generator',),
        },),) + G11nAdmin.fieldsets
    
    class Meta: 
        model = PublicationG11n
        
class LanguageOption(admin.ModelAdmin): 
    """
    This is the option class for Language Admin
    """
    list_display = ('name', 'code', 'alias',) 
    list_editable = ('code', 'alias',) 
    class Meta: 
        model = Language
        
admin.site.register(Publication, PublicationOption)
#admin.site.register(PublicationG11n, PublicationG11nOption)
admin.site.register(Language, LanguageOption)
