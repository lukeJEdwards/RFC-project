from config import IP, PORT, HEADER_LENGTH, FORMAT
from enums import ORIENTATION, EVENT_TYPE, VIDEO_EVENT
from models import piInfo, videoInfo, videoEvent

import socket
import sys
import errno
import dill
import threading

host_name = socket.gethostname()
ip_address = socket.gethostbyname(host_name)

video_info = videoInfo(
    fileName="test.mp4",
    length=67,
    currentTime=3,
    orientation=ORIENTATION.horizontal
)

system_info = piInfo(
    ip=ip_address,
    hostName=host_name,
    currentlyPlaying=video_info,
    isPlaying=False,
)

event = videoEvent(
    type=EVENT_TYPE.init,
    videoState=VIDEO_EVENT.start,
    data=system_info
)

client_socket = socket.socket()
print_lock = threading.Lock()

def print_threadsafe(msg):
    print_lock.acquire()
    print(msg)
    print_lock.release()

def send(msg: bytes) -> None:
    msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode(FORMAT)
    client_socket.send(msg_header + msg)
    
def reciver_handler():
    while True:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            print('Connection closed by the server')
            sys.exit()

        message_length = int(message_header.decode(FORMAT).strip())
        massage = client_socket.recv(message_length)
        order = event.deserialize(massage)
        print(order)


def receive() -> None:
    while True:
        try:
            print("[CONNECTED]")
            while True:
                reciver_handler()

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()
            continue
        except Exception as e:
            # Any other exception - something happened, exit
            print(e)
            sys.exit()


def handel_orders(msg: str) -> None:
    order = dill.loads(msg)
    print(order)


if __name__ == "__main__":
    client_socket.connect((IP, PORT))
    send(event.serialize())
    receive()
