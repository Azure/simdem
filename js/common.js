function sleep(delay) {
    var start = new Date().getTime();
    while (new Date().getTime() < start + delay);
}

function log(type, msg) {
    $('#log').prepend('<br/>' + $('<div/>').text(new Date() + " : " + type + " : " + msg).html());
}

