from dataclasses import dataclass
from enum import Enum, auto

import dill


class ORIENTATION(Enum):
    horizontal = auto()
    vertical = auto()


@dataclass
class VideoInfo:
    fileName: str
    length: int
    currentTime: int
    orientation: ORIENTATION


@dataclass
class PiInfo:
    IP: str
    hostName: str
    currentlyPlaying: bool
    videoInfo: VideoInfo

    def serialise(self):
        return dill.dumps(self)
