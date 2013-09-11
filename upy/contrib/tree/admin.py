from django.contrib import admin
from django import forms
from upy.contrib.tree.models import *
from django.utils.translation import ugettext_lazy as _
from upy.contrib.tree.tree_admin import TreeEditor
from django.conf import settings
from django.template.loader import render_to_string
import re


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
        if self.instance == parent:
            raise forms.ValidationError(_("A node may not be made a child of itself."))
        if parent:
            slug = parent.slug
            if page:
                if slug:
                    slug += "/%s" % page.slug
                else:
                    slug = page.slug
            basenode = parent.get_root()
            if page: # check the slug validity only if this is a page node with its own slug 
                for node in basenode.get_descendants(include_self=False):
                    if slug == node.slug and node.pk != self.instance.pk:
                        raise forms.ValidationError(_(
                            "You cannot use the same slug (/{0}) in two different nodes of the same structure".format(
                                slug)))
                    if node.page and node.page == page and node.pk != self.instance.pk:
                        raise forms.ValidationError(_("You can use page only in one node of the same structure"))
        return self.cleaned_data


class NodeAdmin(TreeEditor):
    """
    This is the option class for Node Admin
    """

    def page_info(self):
        """
        It's renders an html to show through jQuery with page informations
        """
        html = render_to_string("page_info.html", {'node': self})
        return html

    page_info.short_description = _(u"Info page")
    page_info.allow_tags = True

    list_display = ('pk', 'name', 'page', page_info, 'presentation_type', 'hide_in_navigation', 'is_index')
    list_per_page = 900 #we should have all objects on one page 
    list_editable = ('name',)
    fieldsets = (('', {'fields': (('page', 'name', 'parent',), ('is_index', 'hide_in_navigation', 'hide_in_url',),
                                  ('value_regex', 'show_if_logged', 'groups'),), }),
                 (_('Sitemap configuration'), {'fields': (('changefreq', 'priority'),), }),
                 (_('Robots configuration'), {'fields': (('robots', 'disallow'),), }),)
    form = NodeForm
    actions = ['hide_selected', 'protect_selected']

    save_on_top = True

    def parent_id(self, obj):
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
        css = {"all": ("/upy_static/css/page_info.css",)}
        js = (settings.JQUERY_LIB,
              '/upy_static/js/upy-admin-node.js',)


class PageAdminForm(forms.ModelForm):
    """
    Admin's Page form. It cleans regex field
    """

    def clean_regex(self):
        regex = self.cleaned_data['regex']
        match_list = re.findall(r"\<(.*?)\>", regex)

        for word in match_list:
            if match_list.count(word) > 1:
                raise forms.ValidationError(
                    _("Thera are some variables in regex with the same name. It's not permitted."))
        return regex

    class Meta:
        model = Page

    static_vars = forms.RegexField(
        required=False, widget=forms.Textarea(attrs={"cols": '80', "rows": '4'}),
        regex='^(\{((?:"\w+"|\'\w+\'):(?:"\w+"|\'\w+\'),?\s?)+\})*$',
        help_text=_(
            u"""Set the dictionary of static parameters of the page in a regular format:
            {\"param1\":\"value1\", \"param2\":\"value2\"}."""
        )
    )


class PageAdmin(admin.ModelAdmin):
    """
    This is the option class for Page Admin
    """
    list_display = ('name', 'slug', 'regex', 'presentation_type', 'template', 'view')
    list_editable = ('slug', 'regex', 'presentation_type', 'template', 'view')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'template__name', 'view__name')
    save_on_top = True
    form = PageAdminForm
    fieldsets = (('', {'fields':
                           (('name', 'slug',),
                            ('regex', 'show_regex'), ('scheme_name',),
                            ('static_vars',),
                            ('template', 'view'),
                            ('presentation_type',))
    },),)

    class Meta:
        model = Page


class TemplateAdminForm(forms.ModelForm):
    """
    Admin's form for Template
    """
    input_vars = forms.RegexField(required=False, widget=forms.Textarea(attrs={"cols": '80', "rows": '4'}),
                                  regex='^(\w*(,)?|(, )?)*$',
                                  help_text=_(u"Set the variables required by template (separated with ,)."))

    class Meta:
        model = Template


class TemplateAdmin(admin.ModelAdmin):
    """
    This is the option class for Template Admin
    """
    list_display = ('name', 'app_name', 'file_name',)
    list_editable = ('app_name', 'file_name',)
    fieldsets = (('', {'fields': ('name', 'file_name', 'app_name', 'input_vars',), }),)
    list_filter = ('app_name',)
    save_on_top = True
    form = TemplateAdminForm

    class Meta:
        model = Template

    class Media:
        js = (settings.JQUERY_LIB,
              '/upy_static/js/upy-admin-template.js',)


class ViewAdminForm(forms.ModelForm):
    """
    Admin's form for View model
    """
    func_name = forms.RegexField(required=True, regex='^(\w*)$', help_text=_(u"Set the func_name in a regular format."))
    output_vars = forms.RegexField(
        required=False, widget=forms.Textarea(attrs={"cols": '80', "rows": '4'}),
        regex='^(\{((?:"\w+"|\'\w+\'):\s?\w+,?\s?)+\})*$',
        help_text=_(
            u"""Set the dictionary of output variables of the view required by template in a regular format:
            {\"param1\":value1, \"param2\":value2}."""
        )
    )
    input_vars = forms.RegexField(required=False, widget=forms.Textarea(attrs={"cols": '80', "rows": '4'}),
                                  regex='^(\w*,*)*$',
                                  help_text=_(u"Set the input variables for the view (separated with ,)."))

    class Meta:
        model = View


class ViewAdmin(admin.ModelAdmin):
    """
    This is the option class for View Admin
    """
    list_display = ('name', 'app_name', 'module_name', 'func_name',)
    list_editable = ('app_name', 'module_name',)
    list_filter = ('app_name', 'module_name', )
    fieldsets = (
    ('', {'fields': (('name', 'app_name'), ('func_name', 'module_name'), ('input_vars', 'output_vars',),), }),)
    save_on_top = True
    form = ViewAdminForm

    class Meta:
        model = View

    class Media:
        js = (settings.JQUERY_LIB,
              '/upy_static/js/upy-admin-view.js',)


class RobotAdmin(admin.ModelAdmin):
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

    slug = forms.RegexField(required=True, regex='^[-\w/]+$', help_text=_(u"Identifying UrlAjax's url."))
    static_vars = forms.RegexField(
        required=False, widget=forms.Textarea(attrs={"cols": '80', "rows": '4'}),
        regex='^(\{((?:"\w+"|\'\w+\'):\w+,?\s?)+\})*$',
        help_text=_(
            u"""Set the dictionary of static parameters of the page in a regular format:
            {\"param1\":value1, \"param2\":value2}."""
        )
    )


class UrlAjaxAdmin(admin.ModelAdmin):
    """
    This is the option class for UrlAjax Admin
    """
    list_display = ('name', 'slug', 'view')
    list_editable = ('slug', 'view')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'view__name')
    save_on_top = True
    form = UrlAjaxAdminForm

    class Meta:
        model = UrlAjax


admin.site.register(Node, NodeAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(ViewAjax, ViewAdmin)
admin.site.register(Robot, RobotAdmin)
admin.site.register(UrlAjax, UrlAjaxAdmin)
