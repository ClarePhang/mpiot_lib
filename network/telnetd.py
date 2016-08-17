import lwip
import os

_server_fd = None
_client_fd = None

def _accept_conn(server_fd):
    global _client_fd
    cl, remote_addr = server_fd.accept()
    print("telnet client from:", remote_addr)
    client_fd = cl
    cl.setblocking(False)
    cl.setsockopt(lwip.SOL_SOCKET, 20, os.dupterm_notify)
    os.dupterm(client_fd)

def startServer(server_ip):
    global _server_fd
    global _client_fd
    server_fd = lwip.socket()
    server_ip = server_ip
    server_fd.bind(server_ip)
    server_fd.listen(5)
    server_fd.setsockopt(lwip.SOL_SOCKET, 20 , _accept_conn)
