function sleep(delay) {
    var start = new Date().getTime();
    while (new Date().getTime() < start + delay);
}

function log(type, msg) {
    $('#log').prepend('<br/>' + $('<div/>').text(new Date() + " : " + type + " : " + msg).html());
}

function open_tab(url) {
    var win = window.open(url, '_blank');
    if (win) {
	//Browser has allowed it to be opened
	win.focus();
    } else {
	//Browser has blocked it
	alert('Please allow popups for this website');
    }
}
