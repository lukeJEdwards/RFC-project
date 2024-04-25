from config import IP, PORT, PI_COUNT, HEADER_LENGTH, FORMAT
from data import socketMsg, msgType

from PiicoDev_RFID import PiicoDev_RFID
from PiicoDev_Unified import sleep_ms

import sys
import dill
import socket
import threading

server_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.settimeout(1)

client_sockets: dict[str, socket.socket] = {

}


def readRFID():
    rfid = PiicoDev_RFID()

    while True: 
        if rfid.tagPresent():
            id = rfid.readID()

            first_client = client_sockets.keys()[0]

            msg_header = f"{len(id):<{HEADER_LENGTH}}".encode(FORMAT)
            client_sockets[first_client].send(msg_header + id)
            sleep_ms(1000)
        sleep_ms(10)




def connection_handler_recive(client_socket: socket.socket, addr: tuple) -> None:
    print(f"[NEW CONNECTION] {addr} connected")
    client_socket[addr[0]] = client_socket
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
            obj: socketMsg = dill.loads(data)

            match obj.msgType:
                case msgType.INIT:
                    return
                case msgType.UPADTE:
                    return
                case msgType.FULL:
                    return
            print(f"[MESSAGE] {obj}")

    except socket.error:
        connected = False


def connection_handler_send(client_sockets: socket.socket, addr: tuple) -> None:
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True

    try:
        while connected:
            pass

    except socket.error:
        connected = False


def shutdown_server() -> None:
    server_socket.close()


def main() -> None:
    while True:
        try:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=connection_handler_recive, args=(conn, addr))
            send_thred = threading.Thread(target=readRFID)
            send_thred.start()
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
    print(f"[SERVER OPEN ON] {IP, PORT}")
    main()
