jQuery(function(){
	$('#tabs').tabs();
	$('.g11n-model').on('click',function(){
		var val = $(this).attr('href');
		$('#model-select').val(val);
		$('#inspect-form').submit();
		return false;
	});
	$('.att_source_button').on('click',function(){
		var source = $(this).parent().siblings('.att_source');
		var doc = $(this).parent().siblings('.att_doc');
		if(source.is(':visible')){
			source.slideUp();
			doc.slideDown();
		}
		else{
			source.slideDown();
			doc.slideUp();
		}
		var text = $(this).html();
		$(this).html($(this).data('text'));
		$(this).data('text',text);
		return false;
	});
	
});