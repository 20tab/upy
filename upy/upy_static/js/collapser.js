(function( $ ) {

	$.fn.collapser = function(options){
		
		var defaults = {  
			inline_type			: 'tabular',//one of this: tabular, stacked
			show_msg			: 'show',
			hide_msg			: 'hide',
			collapsed			: true,
			msg_color			: '#5B80B2',
			msg_hover_color		: '#003366'
		};  
		var options = $.extend(defaults, options); 

		$.fn.collapser.tabular = function(selector){
			if(options.collapsed){
				selector.parent().addClass("collapsed");
				selector.append(" (<a class=\"collapse-toggle customcollapser\">"+options.show_msg+"</a>)");
			}
			else{
				selector.append(" (<a class=\"collapse-toggle customcollapser\">"+options.hide_msg+"</a>)");
			}
			$(".customcollapser").css({cursor:'pointer',color:options.msg_color});
			$(".customcollapser").hover(function(){
				$(this).css({color:options.msg_hover_color});
			},function(){
				$(this).css({color:options.msg_color})
			});
			$(".customcollapser").on('click',function() {
			    $(this).parent().parent().toggleClass("collapsed");
			    if($(this).parent().parent().hasClass('collapsed')){
			    	$(this).html(options.show_msg);
			    }
			    else{
			    	$(this).html(options.hide_msg);
			    }
			    return false;
			});
		}
		
		$.fn.collapser.stacked = function(selector){
			if(options.collapsed){
				selector.siblings('.inline-related').find('fieldset').addClass("collapse collapsed");
				selector.append(" (<a class=\"collapse-toggle customcollapser\">"+options.show_msg+"</a>)");
			}
			else{
				selector.append(" (<a class=\"collapse-toggle customcollapser\">"+options.hide_msg+"</a>)");
			}
			
			$(".customcollapser").css({cursor:'pointer',color:options.msg_color});
			$(".customcollapser").hover(function(){
				$(this).css({color:options.msg_hover_color});
			},function(){
				$(this).css({color:options.msg_color})
			});
			$(".customcollapser").on('click',function() {
			    $(this).parent().siblings('.inline-related').find('fieldset').toggleClass("collapse collapsed");
			    if($(this).parent().siblings('.inline-related').find('fieldset').hasClass('collapse collapsed')){
			    	$(this).html(options.show_msg);
			    }
			    else{
			    	$(this).html(options.hide_msg);
			    }
			    return false;
			});
		}
		
		return this.each(function(){
			
			if(options.inline_type == 'tabular'){
				$.fn.collapser.tabular($(this));
			}
			else if(options.inline_type == 'stacked'){
				$.fn.collapser.stacked($(this));
			}

		});	

	}
}( jQuery ) );