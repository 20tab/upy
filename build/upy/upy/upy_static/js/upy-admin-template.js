$(document).ready(function(){
	$("#id_name").keyup(function(){
		$("#id_file_name").val($(this).val().replace(/\s+/g,'_').replace(/[^a-zA-Z0-9\_]/g,'').toLowerCase()+".html");
	});
});