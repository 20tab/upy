from django.conf import settings
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationBaseModelAdmin
from django.contrib.admin.options import InlineModelAdmin


class TransAdmin(TranslationAdmin):

    def __init__(self, *args, **kwargs):
        super(TransAdmin,self).__init__(*args, **kwargs)
        self.tab_patch_fieldsets()
        self._patch_prepopulated_fields()

    def tab_patch_fieldsets(self):
        fieldsets = []
        if self.fieldsets:
            self.fieldsets = list(self.fieldsets)
            for fs in self.fieldsets:
                if 'classes' in fs[1].keys() and 'trans-fieldset' in fs[1]['classes']:
                    for lang in settings.LANGUAGES:
                        fieldset = [lang[1]]
                        fields = []
                        for f in fs[1]['fields']:
                            if len(f) == 1:
                                fields.append(tuple(["%s_%s" % (f[0],lang[0].replace("-", "_"))]))
                            else:
                                group = []
                                for ff in list(f):
                                    group.append("%s_%s" % (ff,lang[0].replace("-", "_")))
                                fields.append(tuple(group))
                        fieldset.append({'fields':fields,
                                         'classes':('translatable',)})
                        fieldsets.append(fieldset)
                else:
                    fieldsets.append(fs)
        self.fieldsets = fieldsets

    def _patch_prepopulated_fields(self):
        prepopulated_fields = {}
        for dest, sources in self.prepopulated_fields.items():
            if dest in self.trans_opts.fields:
                for lang in settings.LANGUAGES:
                    key = "%s_%s" % (dest,lang[0].replace("-", "_"))
                    values = []
                    for source in sources:
                        if source in self.trans_opts.fields:
                            values.append("%s_%s" % (source,lang[0].replace("-", "_")))
                        else:
                            values.append(source)
                    prepopulated_fields[key] = values
            else:
                key = dest
                values = []
                if hasattr(settings,"MODELTRANSLATION_DEFAULT_LANGUAGE"):
                    lang = settings.MODELTRANSLATION_DEFAULT_LANGUAGE
                else:
                    lang = settings.LANGUAGES[0][0]
                for source in sources:
                    if source in self.trans_opts.fields:
                        values.append("%s_%s" % (source,lang))
                    else:
                        values.append(source)
                prepopulated_fields[key] = values
        self.prepopulated_fields = prepopulated_fields

    class Media:
        js = (
            settings.JQUERY_LIB,
            settings.JQUERYUI_LIB,
            '/static/tabbed_translation/js/tabbed_translation.js',
        )
        css = {

            'screen': (
                settings.JQUERYUI_CSSLIB,
            ),
        }
        

class TransInlineModelAdmin(TranslationBaseModelAdmin, InlineModelAdmin):
    
    def __init__(self,*args,**kwargs):
        super(TransInlineModelAdmin,self).__init__(*args,**kwargs)
        self.tab_patch_fieldsets()
    
    def get_formset(self, request, obj=None, **kwargs):
        kwargs = self._do_get_form_or_formset(request, obj, **kwargs)
        return super(TransInlineModelAdmin, self).get_formset(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if self.declared_fieldsets:
            return self._do_get_fieldsets_pre_form_or_formset()
        form = self.get_formset(request, obj).form
        fieldsets = self._do_get_fieldsets_post_form_or_formset(request, form, obj)
        return fieldsets

    def tab_patch_fieldsets(self):
        fieldsets = []
        if self.fieldsets:
            self.fieldsets = list(self.fieldsets)
            for fs in self.fieldsets:
                if 'classes' in fs[1].keys() and 'trans-fieldset' in fs[1]['classes']:
                    for lang in settings.LANGUAGES:
                        fieldset = [lang[1]]
                        fields = []
                        for f in fs[1]['fields']:
                            if len(f) == 1:
                                fields.append(tuple(["%s_%s" % (f[0],lang[0].replace("-", "_"))]))
                            else:
                                group = []
                                for ff in list(f):
                                    group.append("%s_%s" % (ff,lang[0].replace("-", "_")))
                                fields.append(tuple(group))
                        fieldset.append({'fields':fields,
                                         'classes':('translatable',)})
                        fieldsets.append(fieldset)
                else:
                    fieldsets.append(fs)
        self.fieldsets = fieldsets

    class Media:
        js = (
            settings.JQUERY_LIB,
            settings.JQUERYUI_LIB,
            '/static/tabbed_translation/js/tabbed_translation.js',
        )
        css = {

            'screen': (
                settings.JQUERYUI_CSSLIB,
            ),
        }


class TransStackedInline(TransInlineModelAdmin, admin.StackedInline):
    pass