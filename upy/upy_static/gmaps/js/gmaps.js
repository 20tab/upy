jQuery(function(){
	
	//append the 'on' event to all the country select boxes (live)
	$('body').on('change', '[id^="id_"][id$="country"]', function(){
		//detect the continent of the selected country
		var new_continent = $(this).find(':selected').parent().attr('class');
		//detect the central part of the id (to consider inline fields as well)
		var id_center = this.id.replace('id_','').replace('country','');
		//select the detected continent in the corresponding object
		$('#id_'+id_center+'continent [value="'+new_continent+'"]').attr('selected',true);
	});

	//saves the complete countries list for restoring
	var all_countries_html = $('[id^="id_"][id$="country"]').html();

	//append the 'on' event to all the continent select boxes (live)
	$('body').on('change', '[id^="id_"][id$="continent"]', function(){
		//detect the selected continent
		var new_continent = $(this).val();
		//detect the central part of the id (to consider inline fields as well)
		var id_center = this.id.replace('id_','').replace('continent','');
		//restore the original contries list
		$('#id_'+id_center+'country').html(all_countries_html);
		//remove all the continent and countries other than the detected one
		if(new_continent != ""){
			$('#id_'+id_center+'country').children().not('.'+new_continent).remove('optgroup');		
		}
	});

});

