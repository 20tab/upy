/*
 * Modificato 12 maggio 2012 per aggiungere lente e chiamare campo geoaddress 
 * 
 */
/*
Integration for Google Maps in the django admin.

How it works:

You have an address field on the page.
Enter an address and an on change event will update the map
with the address. A marker will be placed at the address.
If the user needs to move the marker, they can and the geolocation
field will be updated.

Only one marker will remain present on the map at a time.

This script expects:

<input type="text" name="geoaddress" id="id_geoaddress" />
<input type="text" name="geolocation" id="id_geolocation" />

<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>

*/

function googleMapAdmin() {

    var geocoder = new google.maps.Geocoder();
    var map;
    var marker;

    var self = {
        initialize: function() {
            var lat = 41; //0
            var lng = 12; //0
            var zoom = 4; //2
            // set up initial map to be world view. also, add change
            // event so changing address will update the map
            existinglocation = self.getExistingLocation();
            if (existinglocation) {
                lat = existinglocation[0];
                lng = existinglocation[1];
                zoom = 6;
            }

            var latlng = new google.maps.LatLng(lat,lng);
            var myOptions = {
              zoom: zoom,
              center: latlng,
              mapTypeId: google.maps.MapTypeId.HYBRID
            };
            map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
            if (existinglocation) {
                self.setMarker(latlng);
            }

			// ho scollegato l'evento onchange e l'ho lasciato esplicito sul tasto search
			// altrimenti con l'autocomplete arrivavano troppe richieste e si rompeva
            //$("#id_geoaddress").change(function() {self.codeAddress();});
            
            // niente, se c'e' l'autocomplete, il change si rompe
            /*$("#id_geoaddress").change(function() {
            	$("#gmap_search").css("border", "4px green solid");
            	alert("change");
            });*/
            $("#gmap_search").click(function() {
            	self.codeAddress();
            });
        },

        getExistingLocation: function() {
            var geolocation = $("#id_geolocation").val();
            if (geolocation) {
                return geolocation.split(',');
            }
        },

        codeAddress: function() {
            var address = $("#id_geoaddress").val();
            geocoder.geocode({'address': address}, function(results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    var latlng = results[0].geometry.location;
                    map.setCenter(latlng);
                    map.setZoom(6);

                    self.setMarker(latlng);
                    self.updateGeolocation(latlng);
                } else {
                    alert("Geocode was not successful for the following reason: " + status);
                }
            });
        },

        setMarker: function(latlng) {
            if (marker) {
                self.updateMarker(latlng);
            } else {
                self.addMarker({'latlng': latlng, 'draggable': true});
            }
        },

        addMarker: function(Options) {
            marker = new google.maps.Marker({
                map: map,
                position: Options.latlng
            });

            var draggable = Options.draggable || false;
            if (draggable) {
                self.addMarkerDrag(marker);
            }
        },

        addMarkerDrag: function() {
            marker.setDraggable(true);
            google.maps.event.addListener(marker, 'dragend', function(new_location) {
                self.updateGeolocation(new_location.latLng);
            });
        },

        updateMarker: function(latlng) {
            marker.setPosition(latlng);
        },

        updateGeolocation: function(latlng) {
            $("#id_geolocation").val(latlng.lat() + "," + latlng.lng());
        }
    }

    return self;
}
jQuery(function() {
    var init_upy_map = function(){
        if($("#id_geoaddress").siblings('#gmap_search').attr('id') == undefined){
            $("#id_geoaddress").css("width","400px");
            $("#id_geoaddress").after("<img id='gmap_search' src='/static/admin/img/icon_searchbox.png' alt='Search' style='cursor:pointer;'>");
            var googlemap = googleMapAdmin();
            googlemap.initialize();
        }
    }

    if($("#id_geoaddress").parents('fieldset').find('h2>a').length > 0){
        $("#id_geoaddress").parents('fieldset').find('h2>a').on('click',function(){
            init_upy_map();
        });
    }
    else{
        init_upy_map();
    }
});