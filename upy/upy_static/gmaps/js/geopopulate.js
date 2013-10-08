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
                  	  if ($(field).attr("id").search('country') != -1){
                  	  	  values.push($(field +" option:selected").text());
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
	
	
	$("[id^='id_'][id$='geoaddress']").each(function(){
		if ($(this).attr('id').search('__prefix__') == -1){
            var thisid = $(this).attr('id').replace('id_','').replace('geoaddress','');
            var field;
            field = {
                id: '#id_'+thisid+'geoaddress',
                dependency_ids: [],
                dependency_list: [],
                maxLength: 200
            };


            field['dependency_ids'].push('#id_'+thisid+'address');
            field['dependency_list'].push('address');

            field['dependency_ids'].push('#id_'+thisid+'zip_code');
            field['dependency_list'].push('zip_code');

            field['dependency_ids'].push('#id_'+thisid+'city');
            field['dependency_list'].push('city');

            field['dependency_ids'].push('#id_'+thisid+'country');
            field['dependency_list'].push('country');


            $('.empty-form .form-row .field-geoaddress, .empty-form.form-row .field-geoaddress').addClass('prepopulated_field');
            $(field.id).data('dependency_list', field['dependency_list'])
                       .geopopulate(field['dependency_ids'], field.maxLength);

    	}
    });
    $(".add-row a").click(function(){
    	var total = $("[id^='id_'][id$='geoaddress']").length;
    	$("[id^='id_'][id$='geoaddress']").each(function(index){
			if (index === total - 2) {
                var thisid = $(this).attr('id').replace('id_','').replace('geoaddress','');
                var field;
                field = {
                    id: '#id_'+thisid+'geoaddress',
                    dependency_ids: [],
                    dependency_list: [],
                    maxLength: 200
                };


                field['dependency_ids'].push('#id_'+thisid+'address');
                field['dependency_list'].push('address');

                field['dependency_ids'].push('#id_'+thisid+'zip_code');
                field['dependency_list'].push('zip_code');

                field['dependency_ids'].push('#id_'+thisid+'city');
                field['dependency_list'].push('city');

                field['dependency_ids'].push('#id_'+thisid+'country');
                field['dependency_list'].push('country');


                $('.empty-form .form-row .field-geoaddress, .empty-form.form-row .field-geoaddress').addClass('prepopulated_field');
                $(field.id).data('dependency_list', field['dependency_list'])
                           .geopopulate(field['dependency_ids'], field.maxLength);
                }
    	});
    });

});