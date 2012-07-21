from django.contrib import admin
from upy.contrib.newsletter.models import Dispatcher, Contact, Newsletter, List, Attachment
from django import forms
from django.utils.translation import ugettext_lazy as _
from upy.utils import now
from upy.contrib.ckeditor.widgets import CKEditorWidget

class SendDateForm(forms.ModelForm):
    """
    This form clean a dispatcher and set send_date parameter to now() if it doesn't exists
    """
    class Meta:
        model = Dispatcher

    def clean_send_date(self):
        send_date = self.cleaned_data['send_date']
        if not send_date:
            send_date = now()
            #raise forms.ValidationError(_("The date cannot be in the past!"))
        return send_date

class ContactOption(admin.ModelAdmin):
    """
    Admin's options for Contact model
    """
    list_display = ('email','name','surname','confirmed','subscribed')
    fieldsets = (('', {'fields': 
                       (('name', 'surname',),('email', 'secret_key',),('confirmed','subscribed'),),
        },),)
    list_filter = ('confirmed','subscribed')
    save_on_top = True
    search_fields = ('name','surname','email',)
    class Meta:
        model = Contact  
    
class ListOption(admin.ModelAdmin):
    """
    Admin's options for List model
    """
    list_display = ('name','priority','test','description')
    list_editable = ('priority','description','test')
    fieldsets = (('', {'fields': 
                       (('name', 'publication', 'priority','test'),('description',),('contacts',),),
        },),)
    list_filter = ('priority',)
    filter_horizontal = ('contacts',)
    save_on_top = True
    search_fields = ('name',)
    class Meta:
        model = List  
        
class AttachmentOption(admin.ModelAdmin):
    """
    Admin's options for Attachment model
    """
    list_display = ('name','attached_file')
    fieldsets = (('', {'fields': 
                       (('name', 'attached_file',),),
        },),)
    save_on_top = True
    search_fields = ('name',)
    class Meta:
        model = Attachment 
        
class NLForm(forms.ModelForm):
    """
    This form change default widget to textarea input with CKEditor widget
    """
    body_text = forms.CharField(label = _(u"Body text"),widget=forms.Textarea(attrs={'cols': 80, 'rows': 15}), required = False, help_text = _(u"Set body in text format"))
    body_html = forms.CharField(widget=CKEditorWidget(config={'height': 300,'width': 800,}))
    class Meta:
        model = Newsletter
       
class NewsletterOption(admin.ModelAdmin):
    """
    Admin's options for Newsletter model
    """
    list_display = ('subject','sent','body_text')
    fieldsets = (('', {'fields': 
                       (('subject', 'sent',),('body_text','body_html'),('attachments',)),
        },),)
    list_filter = ('sent',)
    form = NLForm
    save_on_top = True
    search_fields = ('subject',)
    class Meta:
        model = Newsletter
        
class DispatcherOption(admin.ModelAdmin):
    """
    Admin's options for Dispatcher model
    """
    list_display = ('newsletter','send_date', 'sent_date', 'contact_list', 'priority', 'status',)
    #list_editable = ('send_date',)
    fieldsets = (('', {'fields': 
                       (('contact_list', 'newsletter',),('last_mail_sent','status','send_date'),),
        },),)
    list_filter = ('status','user_create')
    save_on_top = True
    form = SendDateForm
    class Meta:
        model = Dispatcher
    def save_model(self, request, obj, form, change):
        obj.user_create = request.user
        obj.save() 
        
    actions = ['stop_selected','revoke_selected','restart_selected','continue_selected']
    
    def stop_selected(self, request, queryset):
        """
        Stop all processing selected dispatchers
        """
        queryset.update(status='stopped')
    stop_selected.short_description = _("Stop selected dispatchers")     
    
    def revoke_selected(self, request, queryset):
        """
        Revoke all selected dispatchers
        """
        queryset.update(status='deleted')
    revoke_selected.short_description = _("Revoke selected dispatchers") 
    
    def restart_selected(self, request, queryset):
        """
        Restart all selected dispatchers
        """
        for q in queryset:
            q.status = 'waiting'
            q.save()
    restart_selected.short_description = _("Restart selected dispatchers now") 
    
    def continue_selected(self, request, queryset):
        """
        Continue all selected dispatchers
        """
        queryset.update(status='processing')
    continue_selected.short_description = _("Continue selected dispatchers")   
            
admin.site.register(Contact, ContactOption)
admin.site.register(List, ListOption)
admin.site.register(Attachment, AttachmentOption)
admin.site.register(Newsletter, NewsletterOption)
admin.site.register(Dispatcher, DispatcherOption)