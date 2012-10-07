from django.conf.urls.defaults import *
from django.conf import settings
#import colors

urlpatterns = patterns('',

    url(r'^$', 'django.views.generic.simple.direct_to_template', {
        'template': 'colors-test.html',
        'extra_context': {
            'colors_tests': [
                '000000', # Black
                'ff0000', # Red
                '008000', # Green 
                '008080', # teal
                '808000', # Olive
                '00ff00', # Lime
                '0000ff', # Blue
                'ffff00', # Yellow
                '00ffff', # Aqua / cyan
                'ff00ff', # Fuchsia / magenta
                '808080', # Gray
                'ffffff', # White
                '000080', # Navy
                'C0C0C0', # Silver
                '800080', # Purple
                '800000', # Maroon
            ],
            'lightness_range':  range(0, 101, 10),
            'saturation_range': range(0, 101, 10),
            'hue_range':        range(0, 361, 30),
            'version':          "0.0.2",#colors.get_version(),
            },
    }, name='django-colors-test'),


)

