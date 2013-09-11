jQuery(function(){
	
	var orderables = []
	var count = 0;
	
	
	$('.inline-related').each(function(){
		if($(this).hasClass('tabular')){
			if($(this).find('.field-position').length > 0){
				$(this).attr('id','inline-related-'+count);
			}
			orderables.push('#inline-related-'+count);
			$(this).find('.field-position').addClass('inline-sortable-item');
			count++;
		}
	});
	
	$('.inline-group').each(function(){
		if($(this).find('.inline-related fieldset.module .field-position').length > 0){
			orderables.push("#"+$(this).attr('id'));
		}
		$(this).find('.inline-related').addClass('inline-sortable-item');
	});
	
	var temp_html_top = "";
	var temp_html_bottom = "";
	
	for(i in orderables){
		if($(orderables[i]).hasClass('tabular')){
			$(orderables[i]).find('tbody').sortable({
				cancel:".add-row",
				axis: 'y',
				delay: '150',
				start: function(event,ui){
					temp_html_bottom = $(this).find('.add-row');
					$(this).find('.add-row').remove();
				},
				stop: function(event,ui){
					$(this).append(temp_html_bottom);
					$(orderables[i]).find("input,textarea,select")
     					.bind('mousedown.ui-disableSelection selectstart.ui-disableSelection', function(e) {
      					e.stopImmediatePropagation();
    				});
				},
				update: function(event, ui) {
		            item = ui.item
		            items = $(this).find('tr').get()
		            $(items).each(function(index) {
		            	input = $(this).find('.field-position').children('input');
                		input.attr('value', index);
		            });
		            $(this).find('tr').removeClass('row1').removeClass('row2');
		            $(this).find('tr:even').addClass('row1');
		            $(this).find('tr:odd').addClass('row2');
				}
				
			});
			
		}
		else{
			$(orderables[i]).sortable({
				cancel:".add-row,h2",
				axis: 'y',
				delay: '150',
				items: '.inline-related',
				start: function(event,ui){
					temp_html_top = $(this).find('h2');
					temp_html_bottom = $(this).find('.add-row');
					$(this).find('.add-row,h2').remove();
				},
				stop: function(event,ui){
					$(this).prepend(temp_html_top);
					$(this).append(temp_html_bottom);
					$(orderables[i]).find("input,textarea,select")
     					.bind('mousedown.ui-disableSelection selectstart.ui-disableSelection', function(e) {
      					e.stopImmediatePropagation();
    				});
				},
				update: function(event, ui) {
		            item = ui.item
		            items = $(this).find('.inline-related').get()
		            $(items).each(function(index) {
		            	input = $(this).find('.field-position').find('input');
                		input.attr('value', index);
		            });
		            $(this).find('tr').removeClass('row1').removeClass('row2');
		            $(this).find('tr:even').addClass('row1');
		            $(this).find('tr:odd').addClass('row2');
				}
				
			});
		}


		$(orderables[i]).find("input,textarea,select")
			.bind('mousedown.ui-disableSelection selectstart.ui-disableSelection', function(e) {
      		e.stopImmediatePropagation();
    	});

		
	}
	
	$('.add-row a').on('click',function(){
		$(this).parents('.ui-sortable').find("input,textarea,select")
			.bind('mousedown.ui-disableSelection selectstart.ui-disableSelection', function(e) {
      		e.stopImmediatePropagation();
    	});	
	});

});