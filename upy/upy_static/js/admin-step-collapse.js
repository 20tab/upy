(function($) {
/* funzione ajax per update note assegnazione */
	$(document).ready(function() {
		$('div.descr').css("display","none");
		$('div.descr').css("width","300px");
		$('div.descr_butt').css("cursor","pointer");
		
		$('div.descr_butt').click(function() {
			id_str = $(this).attr("id");
			id = id_str.replace("descr_butt_", "");

			if($("#descr_"+id).css("display") == "none"){
				$("#descr_"+id).fadeIn('slow');
			}else{
				$("#descr_"+id).fadeOut('slow');
			}
		})
	});
	
})(jQuery);