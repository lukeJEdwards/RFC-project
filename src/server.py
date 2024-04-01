from config import IP, PORT, PI_COUNT, HEADER_LENGTH, FORMAT

import socket
import sys
import threading
import dill

server_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.settimeout(1)

PiDict = {}


def connection_handler(client_socket: socket.socket, addr: tuple) -> None:
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True

    try:
        while connected:
            message_header = client_socket.recv(HEADER_LENGTH)

            if not message_header:
                connected = False
                print(f"[DISCONNECTED] {addr} disconnected")
                continue

            message_length = int(message_header.decode(FORMAT).strip())
            data = client_socket.recv(message_length)
            obj = dill.loads(data)
            print(f"[MESSAGE] {obj}")

    except socket.error:
        connected = False


def shutdown_server() -> None:
    server_socket.close()


def main() -> None:
    while True:
        try:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=connection_handler, args=(conn, addr))
            thread.start()
        except socket.timeout:
            pass
        except KeyboardInterrupt:
            print("Stopping Server")
            shutdown_server()
            sys.exit()


if __name__ == "__main__":
    server_socket.bind((IP, PORT))
    server_socket.listen(PI_COUNT)

    main()
