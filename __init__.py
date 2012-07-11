VERSION = (0,11,1)
__version__ = '.'.join(map(str, VERSION))
DATE = "2012-07-11"


"""
MODIFICHE

0.11.1

- cambiata la struttura delle directory

- aggiunto project.custom_urls che permette di inserire url a mano
- corretto il bug di slug unico per le pagine nella stessa struttura
- modificato lo slug di urlajax. adesso accetta anche gli /
- aggiunte le nuove traduzioni in locale
- reinserito il form del cambio lingua nell'admin (base.html)
- riprogrammato upy.py (script per creare i progetti)
- creato manager per g11n che risolve il problema delle query
- cambiato urls.py - adesso setta la lingua di default
- spostate le funzioni getLanguageList e getDefaultLanguage da tree.utility a g11n.utility 

- FATTO: la logica di URLAJAX non va bene quando si usa nell'admin. Le url (in upy.contrib.tree.utility) dovrebbero essere stampate sempre, non solo se legate a un template
- FATTO: nel calendarietto della data il nome del mese viene nascosto dalle freccette
- FATTO: original_image di UPYImage dovrebbe avere un campo per cambiare la label nel form
- FATTO: il clean_image di UPYImage dovrebbe validare tutti i ProcessedImageField aggiuntivi e nn solo original_image
- FATTO: guardare urls.py e tree/utility.py di MensPhrenetica per impostare la lingua di default di g11n e forse le funzioni che stanno in utility relative alle lingue dovrebbero stare nel modulo g11n non in tree
- FATTO: in upy.contrib.tree.menu.Menu alla linea 80 sostituire nodes con list_nodes
- FATTO: se in page inserisco una regex sbagliata (es. due nomi variabili uguali) la posso inserire ma poi l'admin crasha e non se po cambi... SOL. VALIDATION
- FATTO: problema cache menu' cambio lingua

0.10.9
- corretto bug cache menu e breadcrumb con cambio lingua

0.10.8
- corretto bug templates/admin/custom_index.html per stampare verbose_app_name

0.10.7
- aggiunto py-auto-reload = 1 in bin/uwsgi.ini 
- corretto bug inline formset che non passava la validazione quando non inserivo i g11n
- corretto bug dei g11n stacked inline tabs. adesso se metto piu' stacked allora solo i g11n diventano stacked
- aggiunto il campo page_info nell'admin di node


0.10.6
- aggiunto block body per poter aggiungere script al body tipo <body onload="...">

0.10.5
- cambiato resize delle thumbnail di UPYImage da 50px a 25px e SmartResize
- aggiunta class upy_admin_thumb alla thumbnail per poterla pilotare css
- aggiunto template context static per usare static nei template

0.10.4
- cambiata la vista upy.contrib.tree.favicon

0.10.3
- spostato il commento sotto la direttiva python in upython.py
- sostituita la parola file con tempfile in upy.contrib.tree.menu.py
- sostituito SmartCrop con ResizeToFit in upy.contrib.image.models.UPYImage perche' faceva png trasparenti
- tolta la funzione di callback in prettyPhoto-ini.js


0.10.2
- cambiata url di UPYImage in upyimage
- correto bug Position Js e Css: se insert e position=0, la assegna in automatico, se update no.
- imprecisione nota: se modifico una pubblicazione gia' inserita che ha meno lingue di quelle inserite, mi da 
la possibilita' di inserirne inline di piu', anche quelle non associate alla pubblicazione. Questo avviene in tutti
gli oggetti G11n se vado 'a mano' a modificare il campo language, ma deve restare cosi' se esistono piu' pubblicazioni
senno' e' un macello...

0.10.1
- modificato uwsgi.ini con thread-stacksize
- corretto upython.py
- modificato contrib.image, contrib.customadmin per ImageKit 2.0
- corretti template admin upy con i nuovi di django 1.4
- corretto bug admin pubblication (se la inserisci dopo aver inserito le lingue)
- resta ancora bug inline quando inserisci la pubblicazione???
- corretto font upy h1.site-name

0.9.6
- in upy.utils usavo le parole file e str che fanno parte delle parole di python DA NON UTILIZZARE: corretto
- in upy.contrib.tree.utility ho cancellato la funzione deprecata get_currents()
- upy.py adesso chiede se vuoi installare il virtualenv
- cambiato buttonable admin

0.9.5
- aggiunto SubForeignkey field in upy.fields
- aggiunto SubFKWidget in upy.widgets
- aggiunti anche js e css per queto field

0.9.4
-corretto buggettino in tree.middleware.publication: mancava il controllo if page and... ecc riga 15
-corretto buggettino in tree.context_processors: mancava il controllo se esiste la pagina in upy_context. Se non esiste, 
allora non esiste il template da renderizzare e quindi non deve fare nulla.
-cambiato il nome del tag virgolapunto in comma2dot

0.9.3
aggiunto uwsgi_unbit.ini a upy_project_set

0.9.2
-modifichina a customadmin, controllo se esistono customapps
-modificato middleware required_login per MULTIDOMAIN
-modificato il save di tree.models.template: se non esiste l'index lo crea
-modificati login.html e logout.html: adesso estendono index e scrivono nel box main_content e in + hanno un minimo di grafica


0.9.1
-installato django 1.4
-cambiato tree_admin.py, settings, config, uwsgi.ini, buttonableadmin
-al save di customadmin se view_mode == use_app_icons allora inserisce in automatico le appicon (senza le immagini)
-modificato prettyPhoto-init eliminando i social tools, il title e riferendosi a data-rel. Modificato lib/jquery.prettyPhoto.js sostituendo rel con data-rel
-modificato models di image sostituendo rel con data-rel
-aggiunto il file /upy_static/css/reset.css
-aggiunto il link al reset.css in base.html

0.8.2
modificato tree.context_processors. Non leggeva tutti i context_extras.

0.8.1
la property _g11n in G11nBase diventa g11n altrimenti non funziona nei template

0.7.7
Tolto JQUERY_LIB dall'admin perche' faceva conflitto. upy_global_admin.js adesso funziona. Sistemato il context_processors per il global admin js

0.7.6
JQUERY_LIB adesso viene incluso nei template base dell'admin e del web. 

0.7.5
modificato il template base, il context_processor, il middleware per la favicon che non funzionava ancora

0.7.4
tolto il controllo su custoadmin.context_processors relativo al path per controllare se si tratta di admin e assegnare
USE_CUSTOM_ADMIN ecc. Adesso le variabili vengono sempre assegnate. (Fare il controllo sul path se si tratta di admin non funziona 
nel caso in cui admin abbia un url diverso da 'admin')

0.7.3
cambiato config e settings per server_email
aggiunto controllo su context_processor per evitare le chiamate ajax

0.7.2
favicon diventa attributo di publication e non di publicationg11n

0.7.1
tutto cambiato

0.6.12
-reso configurabile il CKEditorWidget e create le variabili per la sua configurazione in StaticPage e StaticElement.
-modificato newsletter con ckeditor. aveva ancora tinymce.

0.6.11
-corretto bug menu render, manca nel context la variabile NODE

0.6.10
-aggiunta in config e setting la variabile LOCALE_PATH che trova in automatico il percorso di locale per upy

0.6.9
-upy.contrib.tree.utility.UrlSitemap: corretto un bug che generava errore

0.6.8
-upy.contrib.tree.template_context.context_processors: risolto il problema delle url non mappate. adesso lancia handler404 come deve essere.
-upy.contrib.tree.views: agginta la vista favicon che restituisce sempre una favicon
-upy.contrib.tree.urls: mappa l'url favicon.ico con la vista relativa

0.6.7
-upy.contrib.tree.template_context.context_processors: risolte svariate cose legate alla cache e ai metacontent tra cui favicon che non la aggiungeva ai metacontent

0.6.6
-upy/templates/base.html: RISOLTO controllare {{MEDIA_URL}} per la favicon (Non risulta coerente tra me e gabbo)

0.6.5
-upy.utils: aggiunta la funzione truncate per troncare le stringhe
-upy.contrib.customadmin.admin: aggiunta validazione per i caratteri esadecimali

"""
