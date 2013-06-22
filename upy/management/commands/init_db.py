from django.core.management.base import NoArgsCommand
from upy.contrib.g11n.models import Publication,Language,PublicationG11n
from upy.contrib.tree.models import PublicationExtended,TreeStructure,Node
from upy.contrib.customadmin.models import CustomAdmin
from django.conf import settings

def nameproj():
    """
    It asks to user the project's name
    """
    q = raw_input("Project name: ")
    if q != "":
        return q
    else:
        print "Write project's name please!"
        return nameproj()

class Command(NoArgsCommand):
    """
    It validates all models that are G11nBase subclass.
    """
    help="Initializes db with default instances"  
    def handle(self, *args, **options):
        projname = nameproj()
        self.stdout.write("Creating instances...")
        
        if settings.USE_UPY_G11N:
            try:
                publication = Publication.objects.get(default=True)
                self.stdout.write("Default Publication already exists!")
                return
            except:
                self.stdout.write("Creating language")
                try:
                    language = Language.objects.get(name=getattr(settings,'LANGUAGE_DEFAULT_PARAM','italian'),
                                    code=getattr(settings,'LANGUAGE_CODE','it-it'),
                                    alias=getattr(settings,'LANGUAGE_DEFAULT_ALIAS','IT'))
                except:
                    
                    language = Language(name=getattr(settings,'LANGUAGE_DEFAULT_PARAM','italian'),
                                    code=getattr(settings,'LANGUAGE_CODE','it-it'),
                                    alias=getattr(settings,'LANGUAGE_DEFAULT_ALIAS','IT'))
                    language.save()
                self.stdout.write("Creating publication")
                publication = Publication(name=projname,
                                          url="127.0.0.1:8080",
                                          default_language=language,
                                          )
                publication.save()
                publication.languages.add(language)
                self.stdout.write("Creating publication g11n")
                pub_g11n = PublicationG11n(title = projname,
                                           language=language,
                                           publication=publication)
                pub_g11n.save()
                
                if settings.USE_UPY_TREE:
                    self.stdout.write("Creating root node")
                    root = Node(name='root')
                    root.save()
                    self.stdout.write("Creating tree structure")
                    treestruct = TreeStructure(name='base',tree_root=root)
                    treestruct.save()
                    self.stdout.write("Creating publication extended")
                    pub_ext = PublicationExtended(tree_structure=treestruct,publication=publication)
                    pub_ext.save()
        
        if settings.USE_CUSTOM_ADMIN:
            try:
                customadmin = CustomAdmin.objects.get(default=True)
                self.stdout.write("Default CustomAdmin already exists!")
                return
            except:
                self.stdout.write("Creating customadmin")
                customadmin = CustomAdmin(branding=projname,default=True,
                                          view_mode='use_app_and_model_icons')
                customadmin.save()
        self.stdout.write("Done!")