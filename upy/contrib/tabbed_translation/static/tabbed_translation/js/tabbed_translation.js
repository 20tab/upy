jQuery(function(){
    var tabs = "<ul class='translatable_tab'>";

    $('fieldset.translatable h2').hide();

    $('fieldset.translatable').not('.inline-group fieldset.translatable').each(function(){
        tabs += "<li><a href='#tab_"+$(this).find('h2').text()+"'>"+$(this).find('h2').text()+"</a></li>";
        $(this).attr('id',"tab_"+$(this).find('h2').text());
    });
    tabs += "</ul>";



    $(".translatable:first").not('.inline-group fieldset.translatable').before(tabs);
	
    $('.translatable_tab, fieldset.translatable').not('.inline-group fieldset.translatable').wrapAll('<div class="translatable_container"></div>');
    

    //$('.mt').parents('.form-row').tabs();
    
    
    
    //$('fieldset.translatable h2').hide();
	
    
    function do_tab(){
        $(".inline-group .inline-related").not('.empty-form,.tabular').each(function(index){
            if($(this).attr('data-tabbed') === undefined){
                var inline_tabs = "<ul class='translatable_tab'>";
                var index_counter = $(this).attr('id').split('-');
                var id_dom = index_counter[0];
                $(this).children('fieldset.translatable').each(function(){
                    inline_tabs += "<li><a href='#tab_"+$(this).find('h2').text()+id_dom+"-"+index+"'>"+$(this).find('h2').text()+"</a></li>";
                    $(this).attr('id',"tab_"+$(this).find('h2').text()+id_dom+"-"+index);
                });

                inline_tabs += "</ul>";
                $(this).find('.translatable:first').before(inline_tabs);

                $(this).find('.translatable_tab, fieldset.translatable').wrapAll('<div class="translatable_container_inline"></div>');
                $(this).attr('data-tabbed','1');
                $(this).find('.translatable_container_inline').tabs();
            }
        });
    }
    do_tab();
    
    $('.translatable_container').tabs();


    $(".add-row a").click(function(){
		do_tab();
        return true;
	});
    
});