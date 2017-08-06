function sleep(delay) {
    var start = new Date().getTime();
    while (new Date().getTime() < start + delay);
}

function log(type, msg) {
    $('#log').prepend('<br/>' + $('<div/>').text(new Date() + " : " + type + " : " + msg).html());
}

function consoleMonitorSocket() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/console');
    var command_key = ""
    var keypress_interval;
    
    socket.on('update_console', function(msg) {
	$('#console').append(msg);
	log("CONSOLE", msg);
    });

    socket.on('update_info', function(msg) {
	$('#info').append(msg);
	log("INFO", msg)
    });
    
    socket.on('get_command_key', function(msg) {
	$('#info').append($('<span id="input" class="console_input"/>').text("Press a command key (h for help)"));
	input_interval = window.setInterval(function () {
	    log("GET_COMAND_KEY", "Waiting for input")
	}, 1000);
    });
    
    socket.on('clear', function(msg) {
	$('#console').html('');
	log("CONSOLE", "clear")
    });

    socket.on('log', function(msg) {
	log("LOG", msg)
    });
    
    var ping_pong_times = [];
    var start_time;
    window.setInterval(function() {
      start_time = (new Date).getTime();
      socket.emit('ping');
    }, 1000);

    socket.on('pong', function() {
      var latency = (new Date).getTime() - start_time;
      ping_pong_times.push(latency);
      ping_pong_times = ping_pong_times.slice(-30);
      var sum = 0;
      for (var i = 0; i < ping_pong_times.length; i++)
        sum += ping_pong_times[i];
        $('#ping-pong').text(Math.round(10 * sum / ping_pong_times.length) / 10);
    });

    $(document).keypress(function(event) {
	command_key = String.fromCharCode(event.which)
	window.clearInterval(keypress_interval);
	$('#input').remove()
	log("GET_COMMAND_KEY", "Got '" + command_key + "'")
	socket.emit('command_key', command_key)
    })
    
}
