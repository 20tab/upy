jQuery(function(){

    function select2_init(){
        $('.select2-init').not('.processed').each(function(){
            var id = $(this).attr('id').replace('select2-init-', '');
            if(id.indexOf("__prefix__") == -1){
                var opts = $(this).data();
                $('#'+id).select2(opts);
                $(this).addClass('processed');
            }
        });
    }

    select2_init();

    $('.add-row a').on('click', function(){
        select2_init();
        return true
    });
/*
    $('.select2-offscreen').bind("DOMSubtreeModified", function(){
        //It capture html change event and it should select the selected item.
        //Doesn't work yet
    });
*/
});