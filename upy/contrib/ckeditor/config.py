"""
Here there are some configurations for CKEditorWidget
"""

CONFIGURATIONS = {
    'COMPLETE_CONFIG': {
        'skin': 'office2003',
        'toolbar': 'Full',
        'height': 300,
        'width': 800,
        'forcePasteAsPlainText' : True,
        #'contentsCss':'/static/example_layout.css'
    },
    'CKE_CONFIG_EASY': {
        #'contentsCss': '/static/admin/css/ckeditor.css',
        'height': 150,
        'width': 670,
        'forcePasteAsPlainText' : True,
        'toolbar': [['Bold', 'Italic', 'Underline', '-', 'TextColor', '-', 'Link', 'Unlink', '-', 'Source']],
    },
    'CKE_CONFIG_ADVANCED': {
        'height': 250,
        'width': 700,
        'forcePasteAsPlainText' : True,
        'toolbar': [['Bold', 'Italic', 'Underline', 'Subscript', 'Superscript', '-', 'FontSize', 'TextColor', '-', 
                     'JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock', '-', 'NumberedList', 'BulletedList', 
                     '-', 'Outdent', 'Indent', '-', 'Link', 'Unlink', '-', 'Source']],
    }
}
"""
COMPLETE_CONFIG is the complete configuration,
CKE_CONFIG_EASY is a basic configuration with following options: 'Bold', 'Italic', 'Underline', '-', 'TextColor', '-', 'Link', 'Unlink', '-', 'Source',
CKE_CONFIG_ADVANCED has more options to format text
"""
DEFAULT_CONFIG = CONFIGURATIONS['COMPLETE_CONFIG']
CKE_CONFIG_EASY = CONFIGURATIONS['CKE_CONFIG_EASY']
CKE_CONFIG_ADVANCED = CONFIGURATIONS['CKE_CONFIG_ADVANCED']
print "DEFAULT_CONFIG, CKE_CONFIG_EASY, CKE_CONFIG_ADVANCED are deprecated in upy.contrib.ckeditor.config"