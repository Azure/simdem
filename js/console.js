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
	keypress_interval = window.setInterval(function () {
	    log("GET_COMAND_KEY", "Waiting for input")
	}, 1000);
    });

    socket.on('input_string', function(msg) {
	in_str = ""
	$('#input_string_wrap').remove()
	textarea = $('<div class="twrap" id="input_string_wrap">').append($('<textarea id="input_string" contenteditable="true" class="console_input"/>').text("FIXME: Need to get a string from the user"));
	$('#info').append(textarea);
	$("#input_string" ).on('change', function() {
	    in_str = $('#input_string').val()
	    log("GET_INPUT", "Got '" + in_str + "'")
	    socket.emit('input_string', in_str)
	});
    });
    
    socket.on('clear', function(msg) {
	$('#info').html('');
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
