import socket
import os
import crypto
import websocket
import binascii

_server_fd = None
_client_fd = None
ws = None

def handshake_callback(client_fd):
    clr = client_fd
    webkey = None
    while True:
        l = clr.readline()
        if not l:
            raise OSError("ROF in headers")
        if l == b'\r\n':
            break
        try:
            h, v = [x.strip() for x in l.split(b":", 1)]
            if h == b'Sec-WebSocket-Key':
                webkey = v
        except:
            pass

    if not webkey:
        raise OSError("Not a websocket reqiest")

    webkey = webkey + b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    webkey = crypto.sha1(webkey)
    webkey = binascii.b2a_base64(webkey)[:-1]
    resp = b"""\
HTTP/1.1 101 Switching Protocols\r
Upgrade: websocket\r
Connection: Upgrade\r
Sec-WebSocket-Accept: %s\r
\r
""" % webkey
    client_fd.send(resp)
    client_fd.setsockopt(socket.SOL_SOCKET, 20, None)
    os.dupterm(ws)
    _client_fd.setsockopt(socket.SOL_SOCKET, 20 , os.dupterm_notify)

def _accept_conn(server_fd):
    global _client_fd
    global ws
    _client_fd, remote_addr = server_fd.accept()
    print("websocket client from: ", remote_addr)
    _client_fd.setblocking(False)
    _client_fd.setsockopt(socket.SOL_SOCKET, 20, handshake_callback)
    ws = websocket.websocket(_client_fd, True)

def startServer(server_ip):
    global _server_fd
    global _client_fd
    _server_fd = socket.socket()
    _server_fd.bind(server_ip)
    _server_fd.listen(1)
    _server_fd.setsockopt(socket.SOL_SOCKET, 20, _accept_conn)
