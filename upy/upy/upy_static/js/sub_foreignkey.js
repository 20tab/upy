/*
 * This function creates add button for the application's object passed in parameters
 * and returns the html string that represents it
 * application: application's name
 * object: object's name
 * html_linkable: represents the html that you want insert in the popup's link
 * refer_id: represents css id of object needs add button
 * calling: represents object that calls createAddButton
 */
function createAddButton(application,object,html_linkable, refer_id,calling){
	var string = '<span class = "add_custom_button"><a href="/admin/'+application+'/'+object+'/add/" class="add-another" id="add_'+refer_id+'" onclick="return showAddAnotherPopupCustom(this,\''+calling+'\');">'+html_linkable+'</a></span>';
	return string;
}

function showAddAnotherPopupCustom(triggeringLink,calling) {
    var name = triggeringLink.id.replace(/^add_/, '');
    name = id_to_windowname(name);
    href = triggeringLink.href
    if (calling == ""){
	    if (href.indexOf('?') == -1) {
	        href += '?_popup=1';
	    } else {
	        href  += '&_popup=1';
	    }
	}
	else{
		if (href.indexOf('?') == -1) {
	        href += '?_popup=1&_calling='+calling;
	    } else {
	        href  += '&_popup=1&_calling='+calling;
	    }
	}
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

function getQueryParams(qs) {
    qs = qs.split("+").join(" ");
    var params = {},
        tokens,
        re = /[?&]?([^=]+)=([^&]*)/g;

    while (tokens = re.exec(qs)) {
        params[decodeURIComponent(tokens[1])]
            = decodeURIComponent(tokens[2]);
    }

    return params;
}
