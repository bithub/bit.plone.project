

$(document).ready(function() {
    var url = window.location.href.split("&")[0];
    if (url[url.length -1] == '/') {
	url = url.substring(0,url.length-1);
    }
    var parts =url.split('/');
    var pageid = parts[parts.length-1];
    $('.formTabs a[href="#fieldsetlegend-' + pageid + '"]').trigger('click')
})