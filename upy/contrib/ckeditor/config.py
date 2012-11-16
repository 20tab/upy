"""
Here there are some configurations for CKEditorWidget
"""
CKE_CONFIG_EASY = {
    #'contentsCss': '/static/admin/css/ckeditor.css',
    'height': 150,
    'width': 670,
    'forcePasteAsPlainText' : True,
    'toolbar': [['Bold', 'Italic', 'Underline', '-', 'TextColor', '-', 'Link', 'Unlink', '-', 'Source']],
}
"""
CKE_CONFIG_EASY is a basic configuration with following options: 'Bold', 'Italic', 'Underline', '-', 'TextColor', '-', 'Link', 'Unlink', '-', 'Source'
"""
CKE_CONFIG_ADVANCED = {
    'height': 250,
    'width': 670,
    'forcePasteAsPlainText' : True,
    'toolbar': [['Bold', 'Italic', 'Underline', 'Subscript', 'Superscript', '-', 'FontSize', 'TextColor', '-', 
                 'JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock', '-', 'NumberedList', 'BulletedList', 
                 '-', 'Outdent', 'Indent', '-', 'Link', 'Unlink', '-', 'Source']],
}
"""
CKE_CONFIG_ADVANCED has more options to format text
"""