function init_console() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/console');

    socket.on('update_console', function(msg) {
	$('#console').append(msg);
	$('#console').animate({
	    scrollTop: $('#console')[0].scrollHeight}, 500)
	log("CONSOLE", msg);
    });
    
    socket.on('clear', function(msg) {
	$('#console').html('');
	log("CONSOLE", "clear")
    });
}


