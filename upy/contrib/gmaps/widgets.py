from django.forms import widgets
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.util import flatatt

class GoogleMapsAddressWidget(widgets.TextInput):
    "a widget that will place a google map right after the #id_address field"
    
    class Media:
        css = {'all': ('/upy_static/gmaps/css/google-maps-admin.css',),}
        js = (
            #'https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js',
            'http://maps.google.com/maps/api/js?sensor=false',
            '/upy_static/gmaps/js/google-maps-admin.js',
        )
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))
        map_id = final_attrs['id'].replace("id_", "")
        map_id = map_id.replace("geoaddress", "")
        return mark_safe(u'<input%s /><div class="map_canvas_wrapper"><div id="map_%s_canvas" class="map_canvas"></div></div>' % (flatatt(final_attrs), map_id))