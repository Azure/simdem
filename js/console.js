function consoleMonitorSocket() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/console');

    socket.on('update', function(msg) {
	$('#console').append('<br/>' + $('<div/>').text(msg).html());
	$('#log').prepend('<br/>' + $('<div/>').text(new Date() + " : " + msg ).html());
    });

    socket.on('log', function(msg) {
	$('#log').prepend('<br/>' + $('<div/>').text(new Date() + " : " + msg ).html());
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
}
