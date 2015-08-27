var ws = null;
var mycolor = null;
srv = "116.251.209.204:4000"

vlcCommand = sendCommand

// overriding
sendCommand = function(params, append) {
    console.log("sendCommand", params, append)
    if (!ws) {
        vlcCommand(params, append)
        return
    }

    var data = {op:"command", params:params}
    if (append != undefined)
        data.append = append

    sendws(data)
}

function sendws(data) {
    if (ws.readyState === 1) {
        ws.send(JSON.stringify(data))
    } else {
        console.log("not ready")
    }
}

function init_room(rid) {
    $("#yue-room-buttons").hide()
    $("#yue-room-msgs").show()
    $("#yue-room-banner").html("你的房间号: " + rid)
    $("#chat-input").keydown(function (event){
        if(event.which !== 13) return true;
        sendws({op:"chat", msg:$("#chat-input").val()})
        $("#chat-input").val("")
        return false;
    })
}

function init_ws(rid, color) {
    if (document.room_inited) {
        window.alert("正在初始化你的房间，请稍后")
        return
    }
    document.room_inited = true
    mycolor = color

    ws = new WebSocket("ws://" + srv + "/websocket/" + rid);
    ws.onmessage = function (evt) {
        console.log("ws recv:", evt.data);
        var data = JSON.parse(evt.data);
        if (data.op == "command") {
            vlcCommand(data.params, data.append)
        } else if (data.op == "chat") {
            var entry = $("<p class='msg-content' style='color:" + mycolor +"'>").text(data.msg)
            $("#msgs-holder").prepend(entry)
        }
    }

    ws.onopen = function () {
        init_room(rid)
    }

    ws.onerror = function () {
        window.alert("服务器链接失败")
    }
}

$(document).ready(function() {
    $("#create_room").click(function () {
        console.log("in click")
        $.ajax({
            url: "http://" + srv + "/create",
            success: function (data, status, jqXHR) {
                init_ws(data.rid, data.color)
            }
        })
    });

    $("#enter_room").click(function () {
        var rid = window.prompt("要进入的房间号:")
        $.ajax({
            url: "http://" + srv + "/enter_room/" + rid,
            success: function (data) {
                if (data.ok) {
                    init_ws(rid, data.color)
                } else {
                    window.alert("不存在该房间.")
                }
            }
        })
    })
})


// javascript:(function () {$("body").append('<script src="http://116.251.209.204:4000/static/booklet.js"></script>')}())
