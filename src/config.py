import socket

HEADER_LENGTH: int = 10
PI_COUNT: int = 4
FORMAT: str = 'utf-8'
IP: str = socket.gethostbyname(socket.gethostname())
PORT: int = 2555