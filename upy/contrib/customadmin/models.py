"""
It contains customadmin's models. It's used to customize admin's interface
"""
from upy.contrib.tree.models import _
from django.db import models
from upy.contrib.colors.fields import ColorField
from upy.contrib.image.models import PositionImage
from django.conf import settings
from upy.utils import clean_cache 
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

def list_apps():
    """
    it returns a list of tuples with the name of all installed apps with admin's registration.
    """
    list_apps = []
    for app in settings.INSTALLED_APPS:
        if app not in ['django.contrib.contenttypes',
                        'django.contrib.sessions',
                        'django.contrib.messages',
                        'django.contrib.admin',
                        'django.contrib.sitemaps',
                        'mptt',  
                        'imagekit',
                        'upy',
                        'upy.contrib.ckeditor',
                        'upy.contrib.colors',
                        'upy.contrib.language']:
            try:
                CustomApp.objects.get(application=app.split(".")[-1].title())
            except:
                list_apps.append([app.split(".")[-1].title()]*2)
    return list_apps 
class CustomAdmin(models.Model):
    """
    This object define parameters to customize admin layout. It has sense if you use only a record 
    of this class. Infact base template use the first occurence find in the database
    """
    branding = models.CharField(max_length = 200, null = True, blank = True, 
                                default = u"upyproject.com", 
                                help_text = _(u"Set branding"), 
                                verbose_name = _(u"Branding"))
    branding_link = models.CharField(max_length = 200, null = True, blank = True, 
                                     default = u"www.upyproject.com", 
                                     help_text = _(u"Set branding's link"), 
                                     verbose_name = _(u"Branding link"))
    branding_image = models.FilePathField(path=settings.RELATIVE_STATIC_ROOT, null = True, blank = True, 
                                          match="\.jpg|\.jpeg|.png|\.gif", recursive=True, 
                                          help_text = _(u"Set brand's image."), 
                                          verbose_name = _(u"Branding image"))
    is_default = models.CharField(max_length = 50, choices = (("default","Default"),), null = True, blank = True, unique = True, help_text = _(u"Select it if you want use this as default customization."), verbose_name = _(u"Is default"))
    
    bg_header = ColorField(max_length = 200, null = True, blank = True, 
                           help_text = _(u"Set header's background color."), 
                           verbose_name = _(u"BG Header"))
    sitename_font = models.CharField(max_length = 200, null = True, blank = True, 
                                     help_text = _(u"Set sitename font."), 
                                     verbose_name = _(u"Sitename font"))
    sitename_font_size = models.CharField(max_length = 200, null = True, blank = True, 
                                          help_text = _(u"Set sitename font size."), 
                                          verbose_name = _(u"Sitename font size"))
    sitename_font_weight = models.CharField(max_length = 200, null = True, blank = True, 
                                            help_text = _(u"Set sitename font weight."), 
                                            verbose_name = _(u"Sitename font weight"))
    table_title_bg = ColorField(max_length = 200, null = True, blank = True, 
                                help_text = _(u"Set the background of title in tables."), 
                                verbose_name = _(u"BG table title "))
    table_title_color = ColorField(max_length = 200, null = True, blank = True, 
                                   help_text = _(u"Set the color of title in tables."), 
                                   verbose_name = _(u"Table title color"))
    h2_color = ColorField(max_length = 200, null = True, blank = True, 
                          help_text = _(u"Set h2 color."), verbose_name = _(u"H2 color"))
    h2_size = models.CharField(max_length = 200, null = True, blank = True, 
                               help_text = _(u"Set h2 size."), verbose_name = _(u"H2 size"))
    h3_color = ColorField(max_length = 200, null = True, blank = True, 
                          help_text = _(u"Set h3 color."), verbose_name = _(u"H3 color"))
    h3_size = models.CharField(max_length = 200, null = True, blank = True, 
                               help_text = _(u"Set h3 size."), verbose_name = _(u"H3 size"))
    link_color = ColorField(max_length = 200, null = True, blank = True, 
                            help_text = _(u"Set link's color"), verbose_name = _(u"Link color"))
    link_hover_color = ColorField(max_length = 200, null = True, blank = True, 
                                  help_text = _(u"Set link's color when hover"), 
                                  verbose_name = _(u"Link hover color"))
    html_head = models.TextField(null = True, blank = True, 
                                help_text = _(u"Set other html code to put in HEAD section. "), 
                                verbose_name = _(u"Html head"))
    css_code = models.TextField(null = True, blank = True, 
                                help_text = _(u"Set the css code. "), 
                                verbose_name = _(u"Css code"))
    use_css_code = models.BooleanField(help_text = _(u"Check it if you want use css code to extends style."), 
                                       verbose_name = _(u"Use css code"))
    use_log_sidebar = models.BooleanField(default = False, help_text = _(u"Check it if you want use log sidebar in index template."), 
                                       verbose_name = _(u"Use log sidebar"))
    view_mode = models.CharField(max_length = 250, null = True, blank = True, 
                                 choices = (('use_custom_app',_('use_custom_app')),
                                            ('use_app_icons',_('use_app_icons'))), 
                                 help_text = _(u"Choose the view mode"), 
                                 verbose_name = _(u"View mode"))
    autocomplete_app_list = models.BooleanField(default = True, 
        help_text = _(u"Check it if you want complete the custom app list with the default app list."), 
        verbose_name = _(u"Autocomplete App list"))
    
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
        return self.branding_image.replace(settings.RELATIVE_STATIC_ROOT,settings.STATIC_URL).replace("//","/") 
    
    def save(self, *args, **kwargs):
        appicons = CustomApp.objects.all()
        if self.view_mode == "use_app_icons" and not appicons:
            for app in list_apps():
                new_app = CustomApp(application=app[0],verbose_app_name=app[1])
                new_app.save()
        clean_cache(settings.UPYCACHE_DIR,"meta")
        super(CustomAdmin,self).save( *args, **kwargs)
    
    def delete(self):
        clean_cache(settings.UPYCACHE_DIR,"meta")
        super(CustomAdmin,self).delete()
    
    def __unicode__(self):
        return u"%s" % (self.branding)
    
    class Meta:
        verbose_name = _(u"Custom Admin")
        verbose_name_plural = _(u"Custom Admin")
        ordering = ['branding']
        
class CustomApp(PositionImage):
    """
    This object links the installed_apps with an icon to use if CustomAdmin.use_app_icons is True
    """
    application = models.CharField(max_length = 250, 
                                   unique=True, help_text = _(u"Select the application"), 
                                   verbose_name = _(u"Application"))
    verbose_app_name = models.CharField(max_length = 250, unique=True, 
                                        help_text = _(u"Write the verbose name to show"), 
                                        verbose_name = _(u"Verbose app name")) 
    image = ImageSpecField([ResizeToFit(128, 128)], 
                           image_field='original_image', 
                           format='png')
    show_models = models.BooleanField(default=True, 
        help_text = _(u"If use_app_icons is False in Customadmin, you can choose wheter or not show the model list."), 
        verbose_name = _(u"Show models"))
    '''
    tengo questo commento in attesa di sviluppare il resize dinamico
        
    display_width = models.PositiveIntegerField(default = 0)
    display_height = models.PositiveIntegerField(default = 0)
    #app_group = ManyToMany to a group. Future feature to regroup apps in different boxes.
       
    
    def save(self, *args, **kwargs):
        
        print "QQQQQQQQQQQQQQQQQQQQQq sono in customadmin.models.AppIcon.save - prima"
        print "111", dir(self.display_image)
        #print self.display_image.height
        #print self.display_image.width
        print "222", self.display_image._process_content
        print "333", dir(self.display_image._process_content)
        print "444", self.display_image._process_content.im_class
        print "555", self.display_image._process_content.im_func
        print "666", self.display_image._process_content.im_self
        print "777", dir(self.display_image._process_content.im_func)
        print "888", self.display_image._process_content.im_func.func_code
        print "999", self.display_image._process_content.im_func.func_name
        #if self.display_width > 0 : self.display_image.processors[0].width = self.display_width
        #if self.display_height > 0: self.display_image.processors[0].height = self.display_height
        super(AppIcon,self).save( *args, **kwargs)
    '''
    
    def __unicode__(self):
        return u"%s" % (self.application)
    
    class Meta:
        verbose_name = _(u"Custom App")
        verbose_name_plural = _(u"Custom Apps")
        ordering = ['position']
        
class CustomLink(PositionImage):
    """
    This object links the installed_apps with an icon to use 
    if CustomAdmin.use_app_icons is True
    """
    link_url = models.CharField(max_length = 250, default="/admin/", 
                                help_text = _(u"Select the url you want to link"), 
                                verbose_name = _(u"Link Url"))
    verbose_url_name = models.CharField(max_length = 250, unique=True, 
                                        help_text = _(u"Write the verbose name to show"), 
                                        verbose_name = _(u"Verbose url name")) 
    image = ImageSpecField([ResizeToFit(128, 128)], image_field='original_image', format='png')

    
    def __unicode__(self):
        return u"%s" % (self.link_url)
    
    class Meta:
        verbose_name = _(u"Custom Link")
        verbose_name_plural = _(u"Custom Link")
        ordering = ['position']