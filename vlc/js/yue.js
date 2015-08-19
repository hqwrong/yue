var ws = null;


function rawsendCommand(params, append) {
    if (current_que == 'stream') {
        $.ajax({
            url: 'requests/status.xml',
            data: params,
            success: function (data, status, jqXHR) {
                if (append != undefined) {
                    eval(append);
                }
                updateStatus();
            }
        });
    } else {
        if (params.plreload === false) {
            $.ajax({
                url: 'requests/status.xml',
                data: params,
                success: function (data, status, jqXHR) {
                    if (append != undefined) {
                        eval(append);
                    }
                }
            });
        } else {
            $.ajax({
                url: 'requests/status.xml',
                data: params,
                success: function (data, status, jqXHR) {
                    if (append != undefined) {
                        eval(append);
                    }
                }
            });
        }
    }
}

function yue_command(url, params, append) { 
    if (ws.readyState === 1) {
        var data = {params:params}
        if (append != undefined)
            data.append = append
        ws.send(JSON.stringify(data))
    } else {
        console.log("not ready")
    }
}

// overriding
function sendCommand(params, append) {
    yue_command("requests/status.xml", params, append)
}

function yue_connect() {
    if (ws != null) return;
    ws = new WebSocket("ws://116.251.209.204:8000/websocket");
    ws.onmessage = function (evt) {
        console.log("ws recv:", evt.data);
        var data = JSON.parse(evt.data);
        rawsendCommand(data.params, data.append)
    }
}

yue_connect()
