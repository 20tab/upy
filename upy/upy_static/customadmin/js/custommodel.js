jQuery(function(){
	
	var models = $('#id_model').html();
		
	$('#id_app').on('change',function(){
		var val = $(this).val();
        var optgroup = $(this).children('option[value="'+val+'"]').text();
		$('#id_model').html(models);
		$('#id_model optgroup').each(function(){
			if($(this).attr('label') == optgroup){
				$(this).addClass('selected');
			}
		});
		
		$('#id_model').children().not('.selected').remove("optgroup");
	});
	
});
