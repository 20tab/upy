var django;
if(window.django !== undefined){
	(function($) {
	    $(document).ready(function($) {
			$('select').each(function(){
				if($(this).attr('id').indexOf('view_mode') >= 0){
					$(this).css("width","150px");
				}
			});
		});
	})(django.jQuery);
}