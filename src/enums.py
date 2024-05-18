from enum import StrEnum, auto


class EVENT_TYPE(StrEnum):
    init = auto()
    update = auto()
    delete = auto()

class VIDEO_EVENT(StrEnum):
    start = auto()
    stop = auto()
    new = auto()
    progress = auto()
    
    
class ORIENTATION(StrEnum):
    horizontal = auto()
    vertical = auto()