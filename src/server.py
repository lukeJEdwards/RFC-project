from config import IP, PORT, PI_COUNT, HEADER_LENGTH, FORMAT
from models import event

import socket
import sys
import threading

server_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.settimeout(1)

 
print_lock = threading.Lock()

PiDict = {}
connections: set[socket.socket] = set()

def print_threadsafe(msg):
    print_lock.acquire()
    print(msg)
    print_lock.release()
    
def send(socket: socket.socket, msg: bytes) -> None:
    msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode(FORMAT)
    socket.send(msg_header + msg)


def connection_handler(client_socket: socket.socket, addr: tuple) -> None:
    print_threadsafe(f"[NEW CONNECTION] {addr} connected")
    connected = True

    try:
        while connected:
            message_header = client_socket.recv(HEADER_LENGTH)

            if not message_header:
                connected = False
                print_threadsafe(f"[DISCONNECTED] {addr} disconnected")
                continue

            message_length = int(message_header.decode(FORMAT).strip())
            data = client_socket.recv(message_length)
            obj = event.deserialize(data)
            print_threadsafe(f"[MESSAGE] {obj}")
            send(client_socket, obj.serialize())

    except socket.error:
        connected = False


def shutdown_server() -> None:
    for conn in list(connections):
        conn.close()
    server_socket.close()


def main() -> None:
    while True:
        try:
            conn, addr = server_socket.accept()
            connections.add(conn)
            threading.Thread(target=connection_handler, args=(conn, addr)).start()
        except socket.timeout:
            pass
        except KeyboardInterrupt:
            print_threadsafe("Stopping Server")
            shutdown_server()
            sys.exit()


if __name__ == "__main__":
    server_socket.bind((IP, PORT))
    server_socket.listen(PI_COUNT)
    print(f"[LISTENING] {IP}:{PORT}")
    
    main()
