$('.contact').click(function(){
    var name = $(this).find('.name').text(),
        photo = $(this).find('.thumb').attr('src');

    sessionStorage.setItem('chanel', $(this).data('ref'));
    sessionStorage.setItem('sender', $('#sender').val());

    $('#chat-name').text(name);
    $('#chat-photo').attr('src', photo);

    loadMessages($(this).data('ref'), $('#sender').val());
});

const formataData = (format, date) => {
        if (!format) { format = 'Y-m-d' }

        if (!date) { date = new Date() }

        const parts = {
            Y: date.getFullYear().toString(),
            y: ('00' + (date.getYear() - 100)).toString().slice(-2),
            m: ('0' + (date.getMonth() + 1)).toString().slice(-2),
            n: (date.getMonth() + 1).toString(),
            d: ('0' + date.getDate()).toString().slice(-2),
            j: date.getDate().toString(),
            H: ('0' + date.getHours()).toString().slice(-2),
            G: date.getHours().toString(),
            i: ('0' + date.getMinutes()).toString().slice(-2),
            s: ('0' + date.getSeconds()).toString().slice(-2)
        }

        const modifiers = Object.keys(parts).join('')
        const reDate = new RegExp('(?<!\\\\)[' + modifiers + ']', 'g')
        const reEscape = new RegExp('\\\\([' + modifiers + '])', 'g')

        return format
            .replace(reDate, $0 => parts[$0])
            .replace(reEscape, ($0, $1) => $1)
}

function loadMessages(chanel, sender){
    var ref = firebase.database().ref('/messages/'+chanel);

    // Attach an asynchronous callback to read the data at our posts reference
    ref.on("value", function(snapshot) {
        $('.messages ul').html("");
        snapshot.forEach((child) => {
            var msg = child.val();
            alert(sender)
            alert(msg.sender)
            if (sender == msg.sender){
               $('<li class="replies"><p>' + msg.message + '</p></li>').appendTo($('.messages ul'));
            }else {
                $('<li class="sent"><p>' + msg.message + '</p></li>').appendTo($('.messages ul'));
            }
        });
    }, function (errorObject) {
        console.log("The read failed: " + errorObject.code);
    });
}

function sendMessage(chanel, message, sender) {
    // get firebase database reference...
    var db_ref = firebase.database().ref('/messages/'+chanel);

    db_ref.push({
        date: formataData('Y-m-d, o\\n H:i:s').toString(),
        message: message,
        sender: sender
    });
}

// Your web app's Firebase configuration
var firebaseConfig = {
    apiKey: "AIzaSyDs03vnohjCQ-SHOX4fKbarG-bpDsrMf1s",
    authDomain: "freelamz.firebaseapp.com",
    databaseURL: "https://freelamz.firebaseio.com",
    projectId: "freelamz",
    storageBucket: "freelamz.appspot.com",
    messagingSenderId: "1098858814662",
    appId: "1:1098858814662:web:e5873122f291ba8c39cbc7",
    measurementId: "G-D32MXKCFHL"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);