#! /usr/bin/python2

from bottle import request, Bottle, abort, view
import random, string

app = Bottle()

rooms = {}

RID = 1000
alnums = string.ascii_uppercase + string.digits
def gen_rid():
    RID += 1
    return "".join(random.choice(alnums) for _ in range(10)) + RID

def new_room(rid):
    rooms[rid] = {"members":[]}
    return rooms[rid]

def handle_ws(wsock, room):
    while True:
        try:
            message = wsock.receive()
            print "recv:", message
            wsock.send(message)
        except WebSocketError:
            break
        finally:
            room["members"].remove(wsock)
            if not room["members"]:
                del rooms["rid"]

@app.route("/")
@view("index")
def index():
    return {}

@app.route("/test")
@view("room")
def test_room():
    return {"rid":123, "nmember":3}

@app.route("/create")
@view("room")
def create_room():
    return {"rid": gen_rid(), "nmember": 1}

@app.route("/room/<rid>")
@view("room")
def enter_room():
    if rid not in rooms:
        abort(400, "room doesn't existed.")
    return {"rid":rid, "nmember":len(rooms["members"])+1}

@app.route('/websocket/<rid>')
def room_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    room = rooms.get(rid) or new_room(rid)
    room["members"].append(wsock)

    handle_ws(wsock, room)

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
server = WSGIServer(("0.0.0.0", 8000), app,
                    handler_class=WebSocketHandler)
server.serve_forever()
