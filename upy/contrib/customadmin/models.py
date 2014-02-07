"""
It contains customadmin's models. It's used to customize admin's interface
"""
from upy.contrib.tree.models import _
from django.db import models
from upy.contrib.colors.fields import ColorField
from upy.contrib.sortable.models import PositionModel
from django.conf import settings
from imagekit.models import ImageSpecField, ProcessedImageField
from pilkit.processors import ResizeToFit
from upy.fields import NullTrueField


def verifyApp(app):
    return app in ['django.contrib.contenttypes',
                   'django.contrib.sessions',
                   'django.contrib.messages',
                   'django.contrib.admin',
                   'django.contrib.sitemaps',
                   'mptt',
                   'imagekit',
                   'upy',
                   'south',
                   'upy.contrib.inspect',
                   'modeltranslation',
                   'upy.contrib.tabbed_translation',
                   'upy.contrib.cked',
                   'upy.contrib.colors',
                   'upy.contrib.rosetta']


def all_apps():
    """
    it returns a list of tuples with the name of all installed apps with admin's registration.
    """
    list_apps = []
    for app in settings.INSTALLED_APPS:
        if not verifyApp(app):
            list_apps.append([app, app.split(".")[-1].title()])
    return list_apps


def list_apps():
    """
    it returns a list of tuples with the name of all installed apps with admin's registration.
    """
    list_apps = []
    for app in settings.INSTALLED_APPS:
        if not verifyApp(app):
            try:
                CustomApp.objects.get(application=app.split(".")[-1].title())
            except:
                list_apps.append([app.split(".")[-1].title()] * 2)
    return list_apps


def list_models():
    """
    It returns a list of tuple with the name of all models in installed apps
    """
    list_models = []
    for app in settings.INSTALLED_APPS:
        if not verifyApp(app):
            list_models_app = []
            try:
                all_models = models.get_models(models.get_app(app.split(".")[-1]))
            except:
                pass#app doesn't have model.py module
            for m in all_models:
                try:
                    CustomModel.objects.get(app=app, model=m.__name__)
                except:
                    list_models_app.append([m._meta.verbose_name_plural] * 2)
            list_models.append((app.split(".")[-1].title(), list_models_app))
    return list_models


class CustomAdmin(models.Model):
    """
    This object define parameters to customize admin layout. It has sense if you use only a record 
    of this class. Infact base template use the first occurence find in the database
    """
    branding = models.CharField(max_length=200, null=True, blank=True,
                                default=u"upyproject.com",
                                help_text=_(u"Set branding"),
                                verbose_name=_(u"Branding"))
    branding_link = models.CharField(max_length=200, null=True, blank=True,
                                     default=u"www.upyproject.com",
                                     help_text=_(u"Set branding's link"),
                                     verbose_name=_(u"Branding link"))
    branding_image = models.FilePathField(path=settings.RELATIVE_STATIC_ROOT, null=True, blank=True,
                                          match="\.jpg|\.jpeg|.png|\.gif", recursive=True,
                                          help_text=_(u"Set brand's image."),
                                          verbose_name=_(u"Branding image"))
    default = NullTrueField(_(u"Default"), help_text=_(u"Select it if you want use this as default customization."),
                            unique=True)
    default_app_image = ProcessedImageField(verbose_name=_(u"Default app image"),
                                            help_text=_(u"Insert a default application image"), null=True, blank=True,
                                            upload_to='customadmin')
    default_model_image = ProcessedImageField(verbose_name=_(u"Default model image"),
                                              help_text=_(u"Insert a default model image"), null=True, blank=True,
                                              upload_to='customadmin')

    app_image = ImageSpecField([ResizeToFit(128, 128)], source='default_app_image',
                               options={'quality': 90})  #format='JPEG',
    model_image = ImageSpecField([ResizeToFit(50, 50)], source='default_model_image', options={'quality': 90})

    bg_header = ColorField(max_length=200, null=True, blank=True,
                           help_text=_(u"Set header's background color."),
                           verbose_name=_(u"BG Header"))
    sitename_font = models.CharField(max_length=200, null=True, blank=True,
                                     help_text=_(u"Set sitename font."),
                                     verbose_name=_(u"Sitename font"))
    sitename_font_size = models.CharField(max_length=200, null=True, blank=True,
                                          help_text=_(u"Set sitename font size."),
                                          verbose_name=_(u"Sitename font size"))
    sitename_font_weight = models.CharField(max_length=200, null=True, blank=True,
                                            help_text=_(u"Set sitename font weight."),
                                            verbose_name=_(u"Sitename font weight"))
    table_title_bg = ColorField(max_length=200, null=True, blank=True,
                                help_text=_(u"Set the background of title in tables."),
                                verbose_name=_(u"BG table title "))
    table_title_color = ColorField(max_length=200, null=True, blank=True,
                                   help_text=_(u"Set the color of title in tables."),
                                   verbose_name=_(u"Table title color"))
    h2_color = ColorField(max_length=200, null=True, blank=True,
                          help_text=_(u"Set h2 color."), verbose_name=_(u"H2 color"))
    h2_size = models.CharField(max_length=200, null=True, blank=True,
                               help_text=_(u"Set h2 size."), verbose_name=_(u"H2 size"))
    h3_color = ColorField(max_length=200, null=True, blank=True,
                          help_text=_(u"Set h3 color."), verbose_name=_(u"H3 color"))
    h3_size = models.CharField(max_length=200, null=True, blank=True,
                               help_text=_(u"Set h3 size."), verbose_name=_(u"H3 size"))
    link_color = ColorField(max_length=200, null=True, blank=True,
                            help_text=_(u"Set link's color"), verbose_name=_(u"Link color"))
    link_hover_color = ColorField(max_length=200, null=True, blank=True,
                                  help_text=_(u"Set link's color when hover"),
                                  verbose_name=_(u"Link hover color"))
    html_head = models.TextField(null=True, blank=True,
                                 help_text=_(u"Set other html code to put in HEAD section. "),
                                 verbose_name=_(u"Html head"))
    css_code = models.TextField(null=True, blank=True,
                                help_text=_(u"Set the css code. "),
                                verbose_name=_(u"Css code"))
    use_css_code = models.BooleanField(help_text=_(u"Check it if you want use css code to extends style."),
                                       verbose_name=_(u"Use css code"), default=False)
    use_log_sidebar = models.BooleanField(default=False,
                                          help_text=_(u"Check it if you want use log sidebar in index template."),
                                          verbose_name=_(u"Use log sidebar"))
    view_mode = models.CharField(max_length=250, null=True, blank=True,
                                 choices=(('use_custom_app', _('Use custom app system')),
                                          ('use_app_icons', _("Use apps' icons system")),
                                          ('use_app_and_model_icons', _("Use apps and models icons system")),
                                          ('use_model_icons',
                                           _("Use models' icons system in index group models by app")),
                                          ('use_total_model_icons',
                                           _("Use models' icons system in index ungroup models by app"))),
                                 help_text=_(u"Choose the view mode"),
                                 verbose_name=_(u"View mode"))
    autocomplete_app_list = models.BooleanField(default=True,
                                                help_text=_(
                                                    u"Check it if you want complete the custom app list with the default app list."),
                                                verbose_name=_(u"Autocomplete App"))
    autocomplete_models_list = models.BooleanField(default=True,
                                                   help_text=_(
                                                       u"Check it if you want complete the custom models list with the default models list."),
                                                   verbose_name=_(u"Autocomplete model"))

    @property
    def customization(self):
        """
        It returns branding if defined, else image, else only his primary key.
        """
        if self.branding:
            return self.branding
        elif self.branding_image:
            res = self.branding_image.split("/")[-1]
            return res
        else:
            return self.pk

    @property
    def branding_image_url(self):
        return self.branding_image.replace(settings.RELATIVE_STATIC_ROOT, settings.STATIC_URL).replace("//", "/")

    def save(self, *args, **kwargs):
        appicons = CustomApp.objects.all()
        if self.view_mode == "use_app_icons" and not appicons:
            for app in list_apps():
                new_app = CustomApp(application=app[0], verbose_app_name=app[1])
                new_app.save()
        super(CustomAdmin, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"%s" % (self.branding)

    class Meta:
        verbose_name = _(u"Custom Admin")
        verbose_name_plural = _(u"Custom Admin")
        ordering = ['branding']


class CustomApp(PositionModel):
    """
    This object links the installed_apps with an icon to use if CustomAdmin.use_app_icons is True
    """
    application = models.CharField(max_length=250,
                                   unique=True, help_text=_(u"Select the application"),
                                   verbose_name=_(u"Application"))
    verbose_app_name = models.CharField(max_length=250, unique=True,
                                        help_text=_(u"Write the verbose name to show"),
                                        verbose_name=_(u"Verbose app name"))
    image = models.ImageField(_(u'Image'), null=True, blank=True, upload_to='upyimage')
    thumb = ImageSpecField([ResizeToFit(80, 80)],
                           source='image',
                           format='png')
    show_models = models.BooleanField(
        default=True,
        help_text=_(u"If use_app_icons is False in Customadmin, you can choose wheter or not show the model list."),
        verbose_name=_(u"Show models")
    )

    def __unicode__(self):
        return self.application

    class Meta:
        verbose_name = _(u"Custom App")
        verbose_name_plural = _(u"Custom Apps")
        ordering = ['position']


class CustomLink(PositionModel):
    """
    This object links the installed_apps with an icon to use 
    if CustomAdmin.use_app_icons is True
    """
    link_url = models.CharField(max_length=250, default="/admin/",
                                help_text=_(u"Select the url you want to link"),
                                verbose_name=_(u"Link Url"))
    verbose_url_name = models.CharField(max_length=250, unique=True,
                                        help_text=_(u"Write the verbose name to show"),
                                        verbose_name=_(u"Verbose url name"))
    image = models.ImageField(_(u'Image'), null=True, blank=True, upload_to='upyimage')
    thumb = ImageSpecField([ResizeToFit(80, 80)], source='image', format='png')

    def __unicode__(self):
        return self.link_url

    class Meta:
        verbose_name = _(u"Custom Link")
        verbose_name_plural = _(u"Custom Link")
        ordering = ['position']


class CustomModel(PositionModel):
    """
    This object links models in installed_apps with an icon to use
    if CustomAdmin.view_mode == "use_model_icons" or CustomAdmin.view_mode == "use_inner_model_icons"
    """
    app = models.CharField(max_length=250,
                           help_text=_(u"Select an appplication"),
                           verbose_name=_(u"App"))
    model = models.CharField(max_length=250,
                             help_text=_(u"Select a model"),
                             verbose_name=_(u"Model"))
    image = models.ImageField(_(u'Image'), null=True, blank=True, upload_to='upyimage')
    thumb = ImageSpecField([ResizeToFit(50, 50)],
                           source='image',
                           format='png')

    def __unicode__(self):
        return self.model

    class Meta:
        verbose_name = _(u"Custom Model")
        verbose_name_plural = _(u"Custom Models")
        unique_together = ('app', 'model')
        ordering = ['position']
 
