from django.contrib import admin
from django import forms
from upy.contrib.tree.models import *
from django.utils.translation import ugettext_lazy as _
from upy.contrib.tree.tree_admin import TreeEditor
from upy.contrib.g11n.admin import G11nTabularInlineAdmin,G11nStackedInlineAdmin,G11nAdmin,PublicationOption
from django.conf import settings
from django.template.loader import render_to_string
import re

class PublicationExtendedInline(admin.TabularInline):
    """
    Inline admin for PublicationExtended model
    """
    model = PublicationExtended
    fk_name = 'publication'
    can_delete = False 
    max_num = 1 


class PublicationAdmin(PublicationOption):
    """
    Admin's options for Publication model
    """
    list_display = PublicationOption.list_display
    inlines = [PublicationExtendedInline,] + PublicationOption.inlines
    save_on_top = True

 
class CssTreeStructurePositionInline(admin.TabularInline):
    """
    Inline admin for CssTreeStructurePosition model
    """
    model = CssTreeStructurePosition
    extra = 3    
class JsTreeStructurePositionInline(admin.TabularInline):
    """
    Inline admin for JsTreeStructurePosition model
    """
    model = JsTreeStructurePosition
    extra = 3    

class TreeStructureOption(admin.ModelAdmin): 
    """
    This is the option class for TreeStructure Admin
    """
    list_display = ('name', 'tree_root', 'description',) 
    list_editable = ('tree_root', 'description',) 
    list_filter = ('tree_root',)
    save_on_top = True
    inlines = [CssTreeStructurePositionInline,JsTreeStructurePositionInline,]
    fieldsets = (('', {'fields':('name','tree_root','description')}),)
    class Meta: 
        model = TreeStructure

class NodeG11nInline(G11nTabularInlineAdmin):
    """
    Admin's options for NodeG11n model used as inline
    """
    model = NodeG11n
    fieldsets = (('', {'fields':('alias','title')}),) + G11nAdmin.fieldsets
        
class NodeForm(forms.ModelForm):
    """
    Admin's form for Node model. It cleans slug, parent and page fields
    """
    class Meta:
        model = Node

    def clean(self): 
        page = self.cleaned_data['page']
        parent = self.cleaned_data['parent']
        slug = None
        if parent:
            slug = parent.complete_slug
            if page:
                if slug:
                    slug += "/%s" % page.slug 
                else:
                    slug = page.slug
        if self.instance == parent:
            raise forms.ValidationError(_("A node may not be made a child of itself."))
        if parent:
            basenode = parent.basenode
            for node in basenode.get_descendants(include_self=False):
                if slug == node.complete_slug and node.pk != self.instance.pk:
                    raise forms.ValidationError(_("You cannot use two same slugs in same nodes of the same structure"))
                if node.page and node.page == page and node.pk != self.instance.pk:
                    raise forms.ValidationError(_("You can use page only in one node of the same structure"))
        return self.cleaned_data   

    
class NodeOption(TreeEditor): 
    """
    This is the option class for Node Admin
    """
    def page_info(self):
        """
        It's renders an html to show through jQuery with page informations
        """
        html = render_to_string("page_info.html",{'node':self})
        return html
    page_info.short_description = _(u"Info page")
    page_info.allow_tags = True 
    
    list_display = ('pk', 'name', 'page', page_info, 'presentation_type','hide_in_navigation', 'protected') 
    list_per_page = 900 #we should have all objects on one page 
    list_editable = ('name',) 
    fieldsets = (('',{'fields': (('page','name','parent',),('hide_in_navigation','hide_in_url','protected'),('value_regex','show_if_logged','groups'),),}),
                 (_('Sitemap configuration'),{'fields': (('changefreq', 'priority'),),}),
                 (_('Robots configuration'),{'fields': (('robots','disallow'),),}),)
    inlines = [NodeG11nInline,]
    form = NodeForm
    actions = ['hide_selected','protect_selected']
    
    save_on_top = True
    
    def parent_id(self,obj): 
        return obj.parent and obj.parent.id or '0' 
    
    def hide_selected(self, request, queryset):
        """
        It marks as hidden all selected nodes
        """
        queryset.update(hide_in_navigation=True)
    hide_selected.short_description = _("Mark selected nodes as hidden")     
    
    def protect_selected(self, request, queryset):
        """
        It marks as protected all selected nodes
        """
        queryset.update(protected=True)
    protect_selected.short_description = _("Mark selected nodes as protected")     
    
    class Meta: 
        ordering = ['tree_id', 'lft']
        model = Node 
    
    class Media: 
        css = {"all" : ("/upy_static/css/page_info.css",)}
        js = (settings.JQUERY_LIB,
              '/upy_static/js/upy-admin-node.js',)

   
class NodeG11nOption(G11nAdmin): 
    """
    This is the option class for NodeG11n Admin
    """
    list_display = ('alias', 'title', 'node', 'publication', 'language') 
    list_editable = ('title','node','publication', 'language')
    list_per_page = 100 #we sould have all objects on one page 
    fieldsets = (('', {'fields':('alias','title','node')}),) + G11nAdmin.fieldsets
    save_on_top = True
       
    class Meta: 
        model = NodeG11n 
    
class PageG11nOption(G11nAdmin): 
    """
    This is the option class for PageG11n Admin
    """
    list_display = ('page', 'publication', 'language') 
    list_editable = ('publication', 'language')
    list_per_page = 100 #we sould have all objects on one page 
    fieldsets = (('', {'fields':('page',)}),('Options',{
        'fields': ('title', 'description','keywords','author','content_type','enabled','disabled_message','robots'),
        'classes': ('collapse',),})) + G11nAdmin.fieldsets
    save_on_top = True
    
    class Meta: 
        model = PageG11n 

class PageG11nInline(G11nStackedInlineAdmin):
    """
    Admin's options for PageG11n model used as inline
    """
    model = PageG11n
    fieldsets = (('',{
        'fields': (('title', 'description'),('keywords','author'),('content_type','enabled'),('disabled_message',),('robots',),),
        },),) + G11nAdmin.fieldsets
class PageAdminForm(forms.ModelForm):
    """
    Admin's Page form. It cleans regex field
    """
    def clean_regex(self): 
        regex = self.cleaned_data['regex']
        match_list = re.findall(r"\<(.*?)\>",regex)
        
        for word in match_list:
            if match_list.count(word) > 1:
                raise forms.ValidationError(_("Thera are some variables in regex with the same name. It's not permitted."))
        return regex 
        
    class Meta:
        model = Page
    static_vars = forms.RegexField(required = False, widget = forms.Textarea(attrs = {"cols": '80', "rows": '4'}), regex = '^(\{((?:"\w+"|\'\w+\'):(?:"\w+"|\'\w+\'),?\s?)+\})*$', help_text = _(u"Set the dictionary of static parameters of the page in a regular format: {\"param1\":\"value1\", \"param2\":\"value2\"}."))

class PageOption(admin.ModelAdmin): 
    """
    This is the option class for Page Admin
    """
    list_display = ('name', 'slug','regex','presentation_type','template','view') 
    list_editable= ('slug','regex','presentation_type','template','view') 
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PageG11nInline,]
    search_fields = ('name', 'template__name', 'view__name')
    save_on_top = True
    form = PageAdminForm
    fieldsets = (('', {'fields': 
                       (('name', 'slug',),
                       ('regex', 'scheme_name',),
                       ('static_vars',),
                       ('template','view'),
                       ('presentation_type',))
        },),)
    class Meta: 
        model = Page

class TemplateAdminForm(forms.ModelForm):
    """
    Admin's form for Template
    """
    input_vars = forms.RegexField(required = False, widget = forms.Textarea(attrs = {"cols": '80', "rows": '4'}), regex = '^(\w*(,)?|(, )?)*$', help_text = _(u"Set the variables required by template (separated with ,)."))
    class Meta:
        model = Template
class CssTemplatePositionInline(admin.TabularInline):
    """
    Admin's options for CssTemplatePosition model used as inline
    """
    model = CssTemplatePosition
    extra = 3    
class JsTemplatePositionInline(admin.TabularInline):
    """
    Admin's options for JsTemplatePosition model used as inline
    """
    model = JsTemplatePosition
    extra = 3    
    
class TemplateOption(admin.ModelAdmin): 
    """
    This is the option class for Template Admin
    """
    list_display = ('name', 'app_name', 'file_name',) 
    list_editable = ('app_name', 'file_name',) 
    fieldset = (('',{'fields': ('name', 'file_name', 'app_name', 'input_vars',),}))
    list_filter = ('app_name',)
    save_on_top = True
    form = TemplateAdminForm
    inlines = [CssTemplatePositionInline,JsTemplatePositionInline,]
    class Meta: 
        model = Template
    class Media: 
        js = (settings.JQUERY_LIB,
              '/upy_static/js/upy-admin-template.js',)


class ViewAdminForm(forms.ModelForm):
    """
    Admin's form for View model
    """
    func_name = forms.RegexField(required = True, regex = '^(\w*)$', help_text = _(u"Set the func_name in a regular format."))
    output_vars = forms.RegexField(required = False, widget = forms.Textarea(attrs = {"cols": '80', "rows": '4'}), regex = '^(\{((?:"\w+"|\'\w+\'):\s?\w+,?\s?)+\})*$', help_text = _(u"Set the dictionary of output variables of the view required by template in a regular format: {\"param1\":value1, \"param2\":value2}."))
    input_vars = forms.RegexField(required = False, widget = forms.Textarea(attrs = {"cols": '80', "rows": '4'}), regex = '^(\w*,*)*$', help_text = _(u"Set the input variables for the view (separated with ,)."))
    class Meta:
        model = View
    
class ViewOption(admin.ModelAdmin): 
    """
    This is the option class for View Admin
    """
    list_display = ('name', 'app_name', 'module_name', 'func_name',) 
    list_editable = ('app_name', 'module_name',) 
    list_filter = ('app_name', 'module_name', )
    prepopulated_fields = {'func_name': ('name',)}
    fieldsets = (('',{'fields': (('name', 'app_name'), ('func_name','module_name'),('input_vars','output_vars',),),}),)
    save_on_top = True
    form = ViewAdminForm
    class Meta: 
        model = View
   

class CssOption(admin.ModelAdmin): 
    """
    This is the option class for Css Admin
    """
    list_display = ('name', 'file_name',) 
    list_editable = ('file_name',) 
    save_on_top = True
    fieldsets = (('',{'fields': ('name', 'file_name','description'),}),)
    class Meta: 
        model = Css

class UrlAjaxInline(admin.StackedInline):
    """
    Admin's options for UrlAjax model used as inline
    """
    prepopulated_fields = {'slug': ('name',)}
    model = UrlAjax
    extra = 1
class JsOption(admin.ModelAdmin): 
    """
    This is the option class for Js Admin
    """
    list_display = ('name', 'file_name','html_position') 
    list_editable = ('file_name','html_position') 
    save_on_top = True
    fieldsets = (('',{'fields': ('name', 'file_name','html_position','description'),}),)
    inlines = [UrlAjaxInline,]
    class Meta: 
        model = Js

class RobotOption(admin.ModelAdmin): 
    """
    This is the option class for Robot Admin
    """
    list_display = ('name', 'name_id',) 
    list_editable = ('name_id',) 
    save_on_top = True
    class Meta: 
        model = Robot        

class UrlAjaxAdminForm(forms.ModelForm):
    """
    Admin's form for UrlAjax model
    """
    class Meta:
        model = UrlAjax
    slug = forms.RegexField(required = True,  regex = '^[-\w/]+$', help_text = _(u"Identifying UrlAjax's url."))
    static_vars = forms.RegexField(required = False, widget = forms.Textarea(attrs = {"cols": '80', "rows": '4'}), regex = '^(\{((?:"\w+"|\'\w+\'):\w+,?\s?)+\})*$', help_text = _(u"Set the dictionary of static parameters of the page in a regular format: {\"param1\":value1, \"param2\":value2}."))

class UrlAjaxOption(admin.ModelAdmin): 
    """
    This is the option class for UrlAjax Admin
    """
    list_display = ('name', 'slug','view') 
    list_editable= ('slug','view') 
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name','view__name')
    save_on_top = True
    form = UrlAjaxAdminForm
    
    class Meta: 
        model = UrlAjax

admin.site.unregister(Publication)
admin.site.register(Publication,PublicationAdmin)
admin.site.register(TreeStructure, TreeStructureOption)
admin.site.register(Node, NodeOption)
#admin.site.register(NodeG11n, NodeG11nOption)
admin.site.register(Page, PageOption)
#admin.site.register(PageG11n, PageG11nOption)
admin.site.register(Template, TemplateOption)
admin.site.register(View, ViewOption)
admin.site.register(ViewAjax, ViewOption)
admin.site.register(Robot, RobotOption)
admin.site.register(Css,CssOption)
admin.site.register(Js, JsOption)
#admin.site.register(CssTreeStructurePosition)
#admin.site.register(JsTreeStructurePosition)
#admin.site.register(CssTemplatePosition)
#admin.site.register(JsTemplatePosition)
admin.site.register(UrlAjax,UrlAjaxOption)
