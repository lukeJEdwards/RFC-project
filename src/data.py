from dataclasses import dataclass
from enum import Enum, auto

import dill


class orientation(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()

class msgType(Enum):
    INIT = auto()
    UPADTE = auto()
    FULL = auto()

@dataclass
class VideoInfo:
    fileName: str
    length: int
    currentTime: int
    orientation: orientation


@dataclass
class PiInfo:
    hostName: str
    currentlyPlaying: bool
    videoInfo: VideoInfo

@dataclass
class socketMsg:
    IP: str
    msgType: msgType
    mgs: PiInfo | VideoInfo

    def serialise(self):
        return dill.dumps(self)
