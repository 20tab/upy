$(document).ready(function(){
	var str = "";
	$("#id_languages option:selected").each(function(){
		str += "<option value = '"+$(this).val()+"'>"+$(this).text()+"</option>";
	});
	/*$("#id_default_language").html(str);
	*/
	$("#id_languages").change(function(){
		var str = "";
		$("#id_languages option:selected").each(function(){
			str += "<option value = '"+$(this).val()+"'>"+$(this).text()+"</option>";
		});
		$("#id_default_language").html(str);
	});
	
	$("#id_default_language").focus(function(){
		var str = "";
		$("#id_languages option:selected").each(function(){
			str += "<option value = '"+$(this).val()+"'>"+$(this).text()+"</option>";
		});
		$(this).html(str);
	});
	
	
	$("#id_name").change(function(){
		var title = $(this).val();
		$(".dynamic-publicationg11n_set").each(function(){
			var id = $(this).attr("id");
			$("#id_"+id+"-title").val(title);
		});
	});
	
	
	
});