from django.core.management.base import NoArgsCommand, CommandError
from upy.contrib.g11n.models import *
from django.utils.importlib import  import_module
from django.db import models
from django.conf import settings

class Command(NoArgsCommand):
    """
    It validates all models that are G11nBase subclass.
    """
    help="Validates all models that are G11nBase subclass."  
    def handle(self, *args, **options):
        for app_name in settings.INSTALLED_APPS: #controlla tutte le app in INSTALLED_APP
            try:
                import_module('.management', app_name)# Prova ad importare l'applicazione
            except ImportError, exc:
                msg = exc.args[0]
                if not msg.startswith('No module named') or 'management' not in msg: #se non ci riesce lancia eccezione
                    raise        
        for app in models.get_apps(): # cicla tutte le applicazioni
            for m in models.get_models(app): # per ogni modello nell'applicazione corrente
                
                if issubclass(m,G11nModel):# se e' subclass di G11nModel deve controllare che estende una classe astratta e non conreta
                    for base in m.__bases__:
                        if issubclass(base,G11nModel) and not base._meta.abstract:
                            raise CommandError("Error in %s.%s . G11nModel can extend only abstract Model" % (m.__module__,m.__name__))
                elif issubclass(m,G11nBase): # se il modello e' sottoclasse di G11nBase
                    if not hasattr(m.G11nMeta,"g11n"):  #controlla che abbia il parametro g11n nella meta class G11nMeta
                        raise CommandError("Error in %s.%s . G11nMeta must have field with the name g11n" % (m.__module__,m.__name__))
                    elif not hasattr(m.G11nMeta,"fieldname"): #controlla che abbia il parametro fieldname nella meta class G11nMeta
                        raise CommandError("Error in %s.%s . G11nMeta must have field with the name fieldname" % (m.__module__,m.__name__))
                    elif not m.G11nMeta.g11n:#controlla che il parametro g11n non sia nullo nella meta class G11nMeta
                        raise CommandError("Error in %s. %s is a G11nBase model and it needs a meta class G11nMeta." % (m.__module__,m.__name__))
                    elif not hasattr(app,m.G11nMeta.g11n): #controlla che esista il modello definito nel parametro g11n della meta class G11nMeta
                        raise CommandError("Error in %s Model with the name %s doesn't exists." % (m.__module__,m.G11nMeta.g11n))
                    else:
                        g11nmodel = getattr(app, m.G11nMeta.g11n) #importa il modello ereditato da G11nModel
                        if not issubclass(g11nmodel, G11nModel): #controlla che effettivamente sia un G11nModel
                            raise CommandError("Error in %s . %s is not a G11nModel subclass." % (m.__module__,g11nmodel.__name__))
                        
                        else: #se G11nBase passa la validazione e siamo in un G11nModel allora controlla le sue configurazioni
                            foreign_keys = []
                            
                            properties = []
                            for k,v in m.__dict__.items():
                                if type(v) == property:
                                    properties.append(k)
                            
                            for field in g11nmodel._meta.fields: #per ogni field del g11nmodel
                                if field.get_internal_type() == "ForeignKey" and m.__name__ == field.rel.to.__name__: 
                                    # se il field e' una FK il nome del modello G11nBase == al nome del modello al quale g11nmodel si riferisce per questo field
                                    foreign_keys.append(field)# aggiunge alla lista questo campo   
                                    if m.G11nMeta.fieldname != field.name: 
                                        #se il nome del field definito nella meta class G11nMeta != dal nome di questo campo allora lancia eccezione
                                        raise CommandError("Error in %s.%s . G11nMeta.fieldname must be like a field's name in %s." % (m.__module__,m.__name__,g11nmodel.__name__))
                                if field.name in properties:
                                    raise CommandError("Error in %s . %s has the property '%s' with the same name of a %s's attribute." % (m.__module__,m.__name__,field.name,g11nmodel.__name__))
                            if not foreign_keys:# se la lista e' vuota, significa che il g11nmodel non ha una FK verso il G11nBase
                                raise CommandError("Error in %s . %s has not a field related to %s." % (m.__module__,g11nmodel.__name__,m.__name__))
        print "0 errors found in all G11nBase models"