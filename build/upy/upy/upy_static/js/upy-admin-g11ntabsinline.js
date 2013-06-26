$(document).ready(function(){
	$(".g11n-inline-group .inline-related").hide();
	//$(".tabular").show();
	
	var inline_id = "";
	$(".g11n-inline-group").each(function(){
		inline_id = $(this).attr('id').replace("-group","");
		$("#"+$(this).attr('id')+">h2").after("<div class = 'upy_stacked_tabs' id = 'g11ntabs"+inline_id+"'></div>");
	
		var cont = 0;
		$(".dynamic-"+inline_id).each(function(){
			var publication = $("#id_"+$(this).attr('id')+"-publication option:selected").html();
			var language = $("#id_"+$(this).attr('id')+"-language option:selected").html();
			var label = language;
			if (publication != null){
				label = publication + " ("+language+")";
			}
			var a_id = "button-tab-"+$(this).attr('id')
			var selected = "";
			if (cont == 0){
				$(this).show();
				selected = " selected";
			}
			$("#g11ntabs"+inline_id).append( "<a id = '"+a_id+"' class = 'button-tab"+ selected +"'>"+label+"</a>" );
			cont++;
		});
	
		$(".button-tab").on('click', function(){
			$(".button-tab").removeClass('selected');
			$(this).addClass('selected');
			var id = $(this).attr('id').replace("button-tab-","");
			$(".dynamic-"+inline_id).hide();
			$("#"+id).show();
		});
	});

	
	
	
});
