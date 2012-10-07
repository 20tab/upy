$(document).ready(function(){
	if($("#id_page").val() == ""){
		$("#id_protected").attr("disable", true);
	}
	
	$("#id_page").change(function(){
		var value = $("#id_page option:selected").text();
		$("#id_name").attr("value",value);
		if($(this).val() == ""){
			$("#id_protected").attr("disabled","disabled");
		}
		else{
			$("#id_protected").removeAttr("disabled");
		}
	});
	
	$("#id_name").focus(function(){
		var value = $("#id_page option:selected").text();
		
		if(value != "---------"){
			$(this).val(value);
		}
	});
	
	
	$('.page_info_img').hover(function(){
		
		$(this).siblings('.page_info_text').stop().fadeTo(300,1);
	},
	function(){
		$(this).siblings('.page_info_text').stop().fadeTo(100,0);
	});
});