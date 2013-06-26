$(document).ready(function(){
    $.fn.geopopulate = function(dependencies, maxLength) {
        /*
            Depends on urlify.js
            Populates a selected field with the values of the dependent fields,
            URLifies and shortens the string. 
            dependencies - array of dependent fields id's 
            maxLength - maximum length of the URLify'd string 
        */
        return this.each(function() {
            var field = $(this);
            field.data('_changed', false);
            field.change(function() {
                field.data('_changed', true);
            });

            var populate = function () {
                // Bail if the fields value has changed
                if (field.data('_changed') == true) return;
 
                var values = [];
                $.each(dependencies, function(i, field) {
                  if ($(field).val().length > 0) {
                  	  if ($(field).attr("id") == "id_country"){
                  	  	  values.push($("#id_country option:selected").text());	
                  	  }else{
                      values.push($(field).val());
                     }
                  }
                })
                field.val(values.join(', '), maxLength);
            };

            $(dependencies.join(',')).keyup(populate).change(populate).focus(populate);
        });
    };
	
	
	
    var field;


    field = {
        id: '#id_geoaddress',
        dependency_ids: [],
        dependency_list: [],
        maxLength: 200
    };

    
    field['dependency_ids'].push('#id_address');
    field['dependency_list'].push('address');
    
    field['dependency_ids'].push('#id_zip_code');
    field['dependency_list'].push('zip_code');
    
    field['dependency_ids'].push('#id_city');
    field['dependency_list'].push('city');
    
    field['dependency_ids'].push('#id_country');
    field['dependency_list'].push('country');
    
    
    $('.empty-form .form-row .field-geoaddress, .empty-form.form-row .field-geoaddress').addClass('prepopulated_field');
    $(field.id).data('dependency_list', field['dependency_list'])
               .geopopulate(field['dependency_ids'], field.maxLength);

});