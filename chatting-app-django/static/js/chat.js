var text_box = '<div class="card-panel right" style="width: 75%; position: relative">' +
    '<div style="position: absolute; top: 0; left:3px; font-weight: bolder" class="title">{sender}</div>' +
    '{message}' +
    '<div style="position: relative;float: right;bottom: 20px;">{{timestamp}}</div></div>';

function scrolltoend() {
    $('#board').stop().animate({
        scrollTop: $('#board')[0].scrollHeight
    }, 8);
}

function send(sender, receiver, message, full_name_send, full_name_receiver) {
    $.post('/api/messages/', JSON.stringify({"sender": sender, "receiver": receiver,"message": message,"full_name_send":full_name_send,"full_name_receiver": full_name_receiver }), function (data) {
        var box = text_box.replace('{sender}', sender);
        box = box.replace('{message}', message);
        box = box.replace('{{timestamp}}', data.timestamp.slice(0, 16).replace('T', ' '))
        $('#board').append(box);
        scrolltoend();
    })
}

function receive() {
    $.get('/api/messages/' + sender_id + '/' + receiver_id + '/', function (data) {
        console.log(data[0].sender);
        for (var i = 0; i < data.length; i++) {
            var box = text_box.replace('{sender}', data[i].sender);
            box = box.replace('{message}', data[i].message);
            box = box.replace('right', 'left blue lighten-5');
            box = box.replace('{{timestamp}}', data[i].timestamp.slice(0, 16).replace('T', ' '))
            $('#board').append(box);
            scrolltoend();
        }
    })
}