from config import IP, PORT, HEADER_LENGTH, FORMAT
from data import PiInfo, VideoInfo, ORIENTATION

import socket
import sys
import errno
import dill

host_name = socket.gethostname()
ip_address = socket.gethostbyname(host_name)

video_info = VideoInfo(
    fileName="",
    length=0,
    currentTime=0,
    orientation=ORIENTATION.horizontal
)

system_info = PiInfo(
    IP=ip_address,
    hostName=host_name,
    currentlyPlaying=False,
    videoInfo=video_info
)

client_socket = socket.socket()


def send(msg: bytes) -> None:
    msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode(FORMAT)
    client_socket.send(msg_header + msg)


def receive() -> None:
    while True:
        try:
            while True:
                message_header = client_socket.recv(HEADER_LENGTH)

                if not len(message_header):
                    print('Connection closed by the server')
                    sys.exit()

                message_length = int(message_header.decode(FORMAT).strip())
                massage = client_socket.recv(message_length).decode(FORMAT)
                handel_orders(massage)

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()
            continue
        except Exception as e:
            # Any other exception - something happened, exit
            print('Reading error: '.format(str(e)))
            sys.exit()


def handel_orders(msg: str) -> None:
    order = dill.loads(msg)
    print(order)


if __name__ == "__main__":
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)
    send(system_info.serialise())
    receive()
