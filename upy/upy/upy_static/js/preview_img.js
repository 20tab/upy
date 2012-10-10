/* inizializzare la funzione img_preview su ogni select di immagini passando il valore dell'id */
$(document).ready(function(){
	img_preview("id_preview_img");
	img_preview("id_image");
});

/* da qui sotto non toccare niente */
/* **************************** */
function img_preview(string_id){
	/* modificare solo se cambiano i nomi della funzione ajax o del box che contiene la select delle immagini */
	image_preview(string_id, "/img_preview", "div")  
}

function image_preview(string_id, url_func, parent_box){
	var select_img = $("#"+string_id);
	var parent_div = select_img.parent(parent_box);
	parent_div.addClass("preview_img");
	$("#add_"+string_id).after("<div class='box_now' id='div_preview_now_"+string_id+"'></div><div class='box_preview' id='div_preview_"+string_id+"'></div>");

	$("#"+string_id+" > option").mouseover(function(){
		/*$(this).toggleClass("hoverSelectOption");*/
		var str = "";
		var id_img = $(this).attr("value");
		
			$.ajax({
				url: url_func,
				data: "id_img="+id_img,
				dataType: "json",
				type: "POST",
				success: function(result){
					if(result.status == "ok"){
						if(result.url_thumb == ""){
							$("div#div_preview_now_"+string_id).html("<p>preview not available</p>");
						}else{
							str = "<img src='"+result.url_thumb+"' alt='"+result.alt+"' title='"+result.title+"'/>";
							$("div#div_preview_now_"+string_id).html(str);
						}
					}else{
						$("div#div_preview_now_"+string_id).html("");
					}
				} 
			});
		
	}/*, function(){$("div#div_preview_now_"+string_id).html("");}*/);
	
	$("#"+string_id).mouseout(function(){
		/*$(this).toggleClass("hoverSelectOption");*/
		$("div#div_preview_now_"+string_id).html("");
	})
	

	select_img.ready(function(){
		var str = "";
		$("#"+string_id+" option:selected").each(function(){
			var id_img = $(this).attr("value");
			$.ajax({
				url: url_func,
				data: "id_img="+id_img,
				dataType: "json",
				type: "POST",
				success: function(result){
					if(result.status == "ok"){
						if(result.url_thumb == ""){
							$("div#div_preview_"+string_id).html("<p>preview not available</p>");
						}else{
							str = str+"<img src='"+result.url_thumb+"' alt='"+result.alt+"' title='"+result.title+"'/>";
							$("div#div_preview_"+string_id).html(str);
						}
					}else{
						$("div#div_preview_"+string_id).html("");
					}
				} 
			});
		});
	});

	
	select_img.change(function(){
		var str = "";
		$("#"+string_id+" option:selected").each(function(){
			var id_img = $(this).attr("value");
			$.ajax({
				url: url_func,
				data: "id_img="+id_img,
				dataType: "json",
				type: "POST",
				success: function(result){
					if(result.status == "ok"){
						if(result.url_thumb == ""){
							$("div#div_preview_"+string_id).html("<p>preview not available</p>");
						}else{
							str = str+"<img src='"+result.url_thumb+"' alt='"+result.alt+"' title='"+result.title+"'/>";
							$("div#div_preview_"+string_id).html(str);
						}
					}else{
						$("div#div_preview_"+string_id).html("");
					}
				} 
			});
		});
		if($("#"+string_id+" option:selected").length == 0){
			$("div#div_preview_"+string_id).html("");
		}
	});
}
/* ***************************** */