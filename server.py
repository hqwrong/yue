#! /usr/bin/python2

from bottle import request, Bottle, abort, view, static_file, response
import random, string

app = Bottle()

rooms = {}

G = {"rid":1000}
alnums = string.ascii_uppercase + string.digits

def random_color():
    r = lambda: random.randint(10,255)
    return '#%02X%02X%02X' % (r(),r(),r())

def gen_rid():
    G["rid"] += 1
    return "".join(random.choice(alnums) for _ in range(10)) + str(G["rid"])

def new_room(rid):
    rooms[rid] = {"members":[]}
    return rooms[rid]

def handle_ws(wsock, rid):
    room = rooms[rid]
    while True:
        try:
            message = wsock.receive()
	    for w in room["members"]:
            	w.send(message)
        except:
            break

    room["members"].remove(wsock)
    if not room["members"]:
        del rooms[rid]

@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@app.route("/")
@view("index")
def index():
    return {}

@app.route("/static/<path:path>")
def handle_static(path):
    return static_file(path, root="./static/")
    
@app.route("/create")
def create_room():
    return {"rid": gen_rid(), "color":random_color()}

@app.route("/enter_room/<rid>")
def enter_room(rid):
    if rooms.get(rid) == None:
        return {"ok":False}
    else:
        return {"ok":True, "color":random_color()}

@app.route('/websocket/<rid>')
def room_websocket(rid):
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    room = rooms.get(rid) or new_room(rid)
    room["members"].append(wsock)

    handle_ws(wsock, rid)

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
server = WSGIServer(("0.0.0.0", 4000), app,
                    handler_class=WebSocketHandler)

print "listen", 4000
server.serve_forever()
