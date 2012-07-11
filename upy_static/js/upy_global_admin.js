var django;
if(window.django !== undefined){
	(function($) {
	    $(document).ready(function($) {
			$('#changelist-filter h2').click(function() {
		        $(this).parent().children('h3, ul').toggle('slow');
		    });
		    $('#changelist-filter h2').trigger('click');
		});
	})(django.jQuery);
}