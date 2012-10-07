$(document).ready(function(){
	$("#id_name").keyup(function(){
		$("#id_file_name").val($(this).val()+".html");
	});
});