#! /usr/bin/python2

from bottle import request, Bottle, abort
app = Bottle()

@app.route("/")
def index():
    pass
    
@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = wsock.receive()
            print "recv:", message
            wsock.send(message)
        except WebSocketError:
            break

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
server = WSGIServer(("0.0.0.0", 8000), app,
                    handler_class=WebSocketHandler)
server.serve_forever()
