jQuery(function(){
	
	var country = $('#id_country').html();
		
	$('#id_continent').on('change',function(){
		var val = $(this).val();
		$('#id_country').html(country);
		$('#id_country').children().not('.'+val).remove("optgroup");
	});
	
});
