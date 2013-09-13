"""
Admin's option for all model defined in customadmin app.
"""
from django.contrib import admin
from django import forms
from upy.contrib.customadmin.models import CustomAdmin, CustomApp, CustomLink, _, \
    list_apps, list_models, CustomModel, all_apps
from upy.contrib.sortable.admin import PositionAdmin
from upy.utils import upy_re_match
from django.conf import settings
from upy.contrib.image.admin import AdminThumbnail, ColorBoxPositionAdmin


def cleaning_color_picker(form, fields):
    """
    It cleans all color fields defined in CustomAdmin model
    """
    chk = True
    for field in fields:

        if form.cleaned_data[field] and not upy_re_match(r'^[0-9a-fA-F]+$',
                                                         "%s" % form.cleaned_data[field]):
            chk = False
            form._errors[field] = form.error_class(
                [_(u'You must compile this field with hexadecimal characters')])
        if form.cleaned_data[field] and len(form.cleaned_data[field]) != 6:
            chk = False
            form._errors[field] = form.error_class(
                [_(u'You must compile this field with six hexadecimal characters')])
    return form, chk


class CustomAdminForm(forms.ModelForm):
    """
    It ovverrides CustomAdmin modelform
    """

    def clean(self):
        cleaned_data = super(CustomAdminForm, self).clean()
        view_mode = cleaned_data['view_mode']
        autocomplete_app_list = cleaned_data['autocomplete_app_list']
        autocomplete_models_list = cleaned_data['autocomplete_models_list']
        if view_mode and not autocomplete_app_list:
            try:
                CustomApp.objects.get(application__iexact="Customadmin")
            except CustomApp.DoesNotExist:
                msg_view_mode = _(u"You have to define Customadmin in your CustomApp if you use a custom view_mode...")
                msg_autocomplete_app_list = _(
                    u"...or at least enable autocomplete_app_list which will include Customadmin too.")
                self._errors["view_mode"] = self.error_class([msg_view_mode])
                self._errors["autocomplete_app_list"] = self.error_class([msg_autocomplete_app_list])
                # These fields are no longer valid. Remove them from the
                # cleaned data.
                del cleaned_data["view_mode"]
                del cleaned_data["autocomplete_app_list"]
                #raise forms.ValidationError(_("You have to define Customadmin in your CustomApp 
                #if you use a custom view_mode without autocomplete_app_list"))  
        elif view_mode and not autocomplete_models_list:
            try:
                CustomModel.objects.get(model__iexact=CustomAdmin._meta.verbose_name_plural)
            except CustomModel.DoesNotExist:
                msg_view_mode = _(
                    u"You have to define Customadmin in your CustomModel if you use a custom view_mode...")
                msg_autocomplete_models_list = _(
                    u"...or at least enable autocomplete_models_list which will include Customadmin too.")
                self._errors["view_mode"] = self.error_class([msg_view_mode])
                self._errors["autocomplete_models_list"] = self.error_class([msg_autocomplete_models_list])
                # These fields are no longer valid. Remove them from the
                # cleaned data.
                del cleaned_data["view_mode"]
                del cleaned_data["autocomplete_models_list"]
                #raise forms.ValidationError(_("You have to define Customadmin in your CustomApp 
                #if you use a custom view_mode without autocomplete_app_list"))
        self, chk = cleaning_color_picker(self, ['bg_header', 'table_title_bg',
                                                 'table_title_color', 'h2_color',
                                                 'h3_color', 'link_color',
                                                 'link_hover_color'])
        if not chk:
            raise forms.ValidationError(_("Some values are not hexadecimal string"))
        return cleaned_data


class CustomAdminAdmin(admin.ModelAdmin):
    """
    Admin's options for CustomAdmin model
    """
    list_display = ('customization', 'branding', 'branding_link',
                    'default', 'view_mode', 'autocomplete_app_list', 'autocomplete_models_list')
    list_editable = ('branding', 'branding_link', 'default', 'view_mode')
    fieldsets = ((_('Branding'), {'fields':
                                      (('branding', 'branding_link'),
                                       ('branding_image', 'default')),
    },),
                 (_('View Option'), {'fields':
                                         (('view_mode', 'use_log_sidebar'),
                                          ('autocomplete_app_list', 'autocomplete_models_list')),
                 },),
                 (_('Images'), {'fields':
                                    (('default_app_image', 'default_model_image',),),
                 },),
                 (_('Style'), {'fields':
                                   (('bg_header',), ('sitename_font', 'sitename_font_size',
                                                     'sitename_font_weight'), ('table_title_bg', 'table_title_color'),
                                    ('h2_color', 'h2_size'), ('h3_color', 'h3_size'),
                                    ('link_color', 'link_hover_color'),
                                   ),
                 },),
                 (_('Code'), {'fields':
                                  (('html_head',), ('use_css_code',), ('css_code',)),
                 },),
    )
    form = CustomAdminForm
    save_on_top = True

    class Meta:
        model = CustomAdmin

    class Media:
        js = ('/upy_static/customadmin/js/customadmin.js',)


class CustomAppForm(forms.ModelForm):
    """
    It overrides admin form for CustomApp model
    """

    def __init__(self, *args, **kwargs):
        super(CustomAppForm, self).__init__(*args, **kwargs)
        listapps = list_apps()
        if self.instance:
            listapps.append([self.instance.application] * 2)
        self.fields['application'].widget = forms.Select(choices=listapps)

    class Meta:
        model = CustomApp


class CustomAppAdmin(ColorBoxPositionAdmin):
    """
    Admin's options for CustomApp model
    """
    admin_thumbnail = AdminThumbnail(image_field='thumb')
    list_display = ('position', 'application', 'verbose_app_name',
                    'show_models', 'image', 'admin_thumbnail',)
    list_editable = ['position', 'verbose_app_name', 'image']
    list_display_links = ['application', ]
    prepopulated_fields = {'verbose_app_name': ('application',)}

    fieldsets = ((_('Icons'), {'fields':
                                   (('application', 'verbose_app_name'),
                                    ('image',), ('show_models',),),
    },),
    )
    save_on_top = True
    form = CustomAppForm

    class Meta:
        model = CustomApp


class CustomLinkAdmin(ColorBoxPositionAdmin):
    """
    Admin's options for CustomLink model
    """
    admin_thumbnail = AdminThumbnail(image_field='thumb')
    list_display = ('position', 'link_url', 'verbose_url_name', 'admin_thumbnail',)
    list_editable = ['position', 'verbose_url_name', ]
    list_display_links = ['link_url', ]
    prepopulated_fields = {'verbose_url_name': ('link_url',)}

    fieldsets = ((_('Icons'), {'fields':
                                   (('link_url', 'verbose_url_name'), ('image',),),
    },),
    )
    save_on_top = True

    class Meta:
        model = CustomLink


class CustomModelForm(forms.ModelForm):
    """
    It overrides admin form for CustomModel model
    """

    def __init__(self, *args, **kwargs):
        super(CustomModelForm, self).__init__(*args, **kwargs)
        listmodels = list_models()
        listapps = all_apps()
        print listapps
        if self.instance.pk:
            listmodels.append([self.instance.model] * 2)
        self.fields['model'].widget = forms.Select(choices=listmodels)
        self.fields['app'].widget = forms.Select(choices=listapps)

    class Meta:
        model = CustomModel


class CustomModelAdmin(ColorBoxPositionAdmin):
    """
    Admin's options for CustomModel model
    """
    admin_thumbnail = AdminThumbnail(image_field='thumb')
    list_display = ('position', 'app', 'model', 'image', 'admin_thumbnail',)
    list_editable = ['position', 'image']
    list_display_links = ['model', ]
    list_filter = ('app',)
    fieldsets = ((_('Icons'), {'fields':
                                   (('app', 'model',),
                                    ('image',),),
    },),
    )
    save_on_top = True
    form = CustomModelForm

    class Meta:
        model = CustomModel

    class Media:
        js = ColorBoxPositionAdmin.Media.js + ('/upy_static/customadmin/js/custommodel.js',)


admin.site.register(CustomAdmin, CustomAdminAdmin)
admin.site.register(CustomApp, CustomAppAdmin)
admin.site.register(CustomLink, CustomLinkAdmin)
admin.site.register(CustomModel, CustomModelAdmin)
