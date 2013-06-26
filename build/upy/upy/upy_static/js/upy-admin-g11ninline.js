$(document).ready(function(){
	var id_group = $(".inline-group").attr("id").replace("group","");
	var id_label = id_group.replace("id_","");
	var inline_len = parseInt($("#id_"+id_group+"TOTAL_FORMS").val());
	var button_save = "input[name='_save']";
	var button_another = "input[name='_addanother']";
	var button_continue = "input[name='_continue']";
	
	$(button_save).on('click',function(){
		return checkG11nCompiled(inline_len,id_group);
	});
	$(button_another).on('click',function(){
		return checkG11nCompiled(inline_len,id_group);
	});
	$(button_continue).on('click',function(){
		return checkG11nCompiled(inline_len,id_group);
	});
	
	
});

function checkG11nCompiled(inline_len,id_group){
	/* QUI DEVO CONTROLLARE SOLO GLI INPUT CHE SONO TEXT PERCHÈ:
	 * 1: SE IL CAMPO È RADIO 0 SELECT ED È OBBLIGATORIO ALLORA HA UN VALORE INITIAL QUINDI
	 * 		IL FORM DEVE ESSERE VALIDATO
	 * 2: SE IL CAMPO È CHECKBOX OBBLIGATORIO NON VUOL DIRE NIENTE PERCHÈ O È True O È False  
	 */
	for(var i = 0; i < inline_len; i++){
		var chech = true;
		$("#"+id_group+i+" input[type=text]").each(function(){//per ogni input
			//controllo se il value è diverso da ""
			if($(this).val() != ""){
				chech = false;								  //dico che almeno un campo è stato compilato
			}
		});
		$("#"+id_group+i+" textarea").each(function(){
			//controllo se il value è diverso da ""
			if($(this).siblings('#cke_'+$(this).attr('id')).attr('id') != undefined){
				//Sono in un CKEditor
				if($(this).siblings('#cke_'+$(this).attr('id')).find('iframe').contents().find('body').html() != ""){
					chech = false;
				}
			}
			else{
				//Sono in una textarea normale
				if($(this).val() != ""){
					chech = false;
				}
			}						
		});
		if(chech){//se nessun campo è stato compilato allora disabilito publication e language
			$("#id_"+id_group+i+"-publication").val("");
			$("#id_"+id_group+i+"-language").val("");
		}
	}	
	return true;
}
